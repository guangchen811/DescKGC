from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from .template import (
    ALIGN_TASK_FORMAT_TEMPLATE,
    ALIGN_INPUT_TEMPLATE
)

def init_align_chain(llm):
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
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt
        ]
    )
    align_chain = LLMChain(
        llm=llm,
        prompt=chat_prompt_template,
        output_key="entities"
    )
    return align_chain

if __name__ == '__main__':
    from langchain.chat_models import ChatOpenAI
    from src.tools.align.utils import candidate_entities_warpper
    llm = ChatOpenAI(temperature=0.3)
    align_chain = init_align_chain(llm)
    src_entity = "Complex networks: have attracted a great deal of research interest in the last two decades."
    candidate_entities = [
        ("network science", "the study of complex networks"),
        ("network theory", "the study of graphs as a representation of either symmetric relations or asymmetric relations between discrete objects")]
    candidate_entities_fmt = candidate_entities_warpper(candidate_entities)
    res = align_chain({
        "topic": "network science",
        "source_entity": src_entity,
        "candidate_entities": candidate_entities_fmt
    })
    print(res)