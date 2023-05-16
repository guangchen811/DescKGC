import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from template import ENTITY_EXTRACT_TEMPLATE, RELATION_EXTRACT_TEMPLATE



entity_human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=ENTITY_EXTRACT_TEMPLATE,
            input_variables=["cate", "description", "required_relations"],
        )
    )
entity_chat_prompt_template = ChatPromptTemplate.from_messages([entity_human_message_prompt])

relation_human_message_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            template=RELATION_EXTRACT_TEMPLATE,
            input_variables=["cate", "description", 'entities', 'required_relations'],
        )
    )
relation_chat_prompt_template = ChatPromptTemplate.from_messages([relation_human_message_prompt])

chat = ChatOpenAI(temperature=0.3)
entity_extract_chain = LLMChain(llm=chat, prompt=entity_chat_prompt_template, output_key="entities")
relation_extract_chain = LLMChain(llm=chat, prompt=relation_chat_prompt_template, output_key="triples")

extract_chain = SequentialChain(
    chains=[entity_extract_chain, relation_extract_chain],
    input_variables=["cate", "description", "required_relations"],
    output_variables=["entities", "triples"],
    verbose=True)

with open('../data/train.json', 'r', encoding='utf-8') as f:
    lines = [json.loads(line) for line in f.readlines()]

for idx, aline in enumerate(lines):
    if idx ==7:
        cate = aline['cate']
        description = aline['input']
        required_relations = aline['instruction'].split('：')[1].split('，')[0]
        
        print("summary:", ">"*10)
        print(description)
        res = extract_chain({"cate":cate, "description": description, "required_relations": required_relations})
        print("entities", "-"*10)
        print(res['entities'])
        print("triples", "-"*10)
        print(res['triples'])
        print(aline['output'])