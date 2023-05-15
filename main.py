import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.tools.extractor.template import ENTITY_EXTRACT_TEMPLATE, RELATION_EXTRACT_TEMPLATE

with open('./data/arxiv_network_science.json', 'r') as f:
    res = json.load(f)

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

chat = ChatOpenAI(temperature=0.3)
entity_extract_chain = LLMChain(llm=chat, prompt=entity_chat_prompt_template, output_key="entities")
relation_extract_chain = LLMChain(llm=chat, prompt=relation_chat_prompt_template, output_key="relations")

extract_chain = SequentialChain(
    chains=[entity_extract_chain, relation_extract_chain],
    input_variables=["topic", "summary"],
    output_variables=["entities", "relations"],
    verbose=True)

for idx, a_res in enumerate(res):
    if idx >=1:
        break
    summary = a_res['summary']
    print("summary:", ">"*10)
    print(summary)
    res = extract_chain({"summary":summary, "topic": "network science"})
    print("entities", "-"*10)
    print(res['entities'])
    print("relations", "-"*10)
    print(res['relations'])