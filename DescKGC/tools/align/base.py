from typing import Type

from langchain.chains import LLMChain
from langchain.llms.base import BaseLLM
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate

from .template import ALIGN_INPUT_TEMPLATE, ALIGN_TASK_FORMAT_TEMPLATE, MERGE_INPUT_TEMPLATE, MERGE_TASK_FORMAT_TEMPLATE


def init_align_chain(llm: Type[BaseLLM]) -> Type[LLMChain]:
    """Initialize the entity alignment chain.
    the entity alignment chain is used to align the entities with the same meaning.
    :param llm: the language model
    :type llm: Type[BaseLLM]
    :return: the entity alignment chain
    :rtype: Type[LLMChain]
    """
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=ALIGN_TASK_FORMAT_TEMPLATE,
            input_variables=["topic"],
        )
    )
    human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=ALIGN_INPUT_TEMPLATE,
            input_variables=["source_entity", "candidate_entities"],
        )
    )
    chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    align_chain = LLMChain(llm=llm, prompt=chat_prompt_template, output_key="entities")
    return align_chain


def init_entity_merge_chain(llm: Type[BaseLLM]) -> Type[LLMChain]:
    """Initialize the entity merge chain.
    the entity merge chain is used to merge the entities with the same meaning filtered by the entity alignment chain.

    :param llm: the language model
    :type llm: Type[BaseLLM]
    :return: the entity merge chain
    :rtype: Type[LLMChain]
    """
    system_message_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            template=MERGE_TASK_FORMAT_TEMPLATE,
            input_variables=["topic"],
        )
    )
    human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=MERGE_INPUT_TEMPLATE,
            input_variables=["entities"],
        )
    )
    chat_prompt_template = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    merge_chain = LLMChain(llm=llm, prompt=chat_prompt_template, output_key="new_entity")
    return merge_chain


if __name__ == "__main__":
    from langchain.chat_models import ChatOpenAI

    from DescKGC.tools.align.utils import entities_nd_pair_warpper
    from DescKGC.tools.align.parser import EntityMergeOutputParser

    llm = ChatOpenAI(temperature=0.3)
    align_chain = init_align_chain(llm)
    merge_chain = init_entity_merge_chain(llm)
    merge_parser = EntityMergeOutputParser()
    src_entity = """Complex networks: have attracted a
    "great deal of research interest in the last two decades."""
    candidate_entities = [
        ("network science", "the study of complex networks"),
        (
            "network theory",
            "the study of graphs as a representation of either "
            "symmetric relations or asymmetric relations between"
            " discrete objects",
        ),
        (
            "Complex network",
            "a type of graph with non-trivial topological "
            "features—features that do not occur in simple "
            "networks such as lattices or random graphs but "
            "often occur in graphs modelling of real systems.",
        ),
    ]
    candidate_entities_fmt = entities_nd_pair_warpper(candidate_entities)
    res = align_chain(
        {
            "topic": "network science",
            "source_entity": src_entity,
            "candidate_entities": candidate_entities_fmt,
        }
    )
    print(res["entities"])
    new_entity = merge_chain({"topic": "network science", "entities": res["entities"]})
    print(merge_parser.parse(new_entity["new_entity"]))
