import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .template import ENTITY_EXTRACT_TEMPLATE, RELATION_EXTRACT_TEMPLATE
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

def init_extract_chain(llm):
    entity_human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=ENTITY_EXTRACT_TEMPLATE,
                input_variables=["topic", "summary"],
            )
        )
    entity_chat_prompt_template = ChatPromptTemplate.from_messages([entity_human_message_prompt])

    relation_human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=RELATION_EXTRACT_TEMPLATE,
                input_variables=["summary", 'entities'],
            )
        )
    relation_chat_prompt_template = ChatPromptTemplate.from_messages([relation_human_message_prompt])

    entity_extract_chain = LLMChain(llm=llm, prompt=entity_chat_prompt_template, output_key="entities")
    relation_extract_chain = LLMChain(llm=llm, prompt=relation_chat_prompt_template, output_key="relations")

    extract_chain = SequentialChain(
        chains=[entity_extract_chain, relation_extract_chain],
        input_variables=["topic", "summary"],
        output_variables=["entities", "relations"],
        verbose=True
    )
    return extract_chain

if __name__ == '__main__':
    from template import ENTITY_EXTRACT_TEMPLATE
    llm = OpenAI()
    prompt = PromptTemplate(
        input_variables=['summary'],
        template=ENTITY_EXTRACT_TEMPLATE
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    print(chain.run())