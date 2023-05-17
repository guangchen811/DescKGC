import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
from template import ENTITY_EXTRACT_TEMPLATE, RELATION_EXTRACT_TEMPLATE, ONLY_RELATION_EXTRACT_TEMPLATE

two_stage_mode = False

chat = ChatOpenAI(temperature=0.3)

if two_stage_mode == True:
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

    entity_extract_chain = LLMChain(llm=chat, prompt=entity_chat_prompt_template, output_key="entities")
    relation_extract_chain = LLMChain(llm=chat, prompt=relation_chat_prompt_template, output_key="triples")
    extract_chain = SequentialChain(
        chains=[entity_extract_chain, relation_extract_chain],
        input_variables=["cate", "description", "required_relations"],
        output_variables=["entities", "triples"],
        verbose=True)
else:
    relation_human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=ONLY_RELATION_EXTRACT_TEMPLATE,
                input_variables=["description", 'required_relations', 'example_input', 'example_output', 'example_required_relations'],
            )
        )
    relation_chat_prompt_template = ChatPromptTemplate.from_messages([relation_human_message_prompt])
    extract_chain = LLMChain(llm=chat, prompt=relation_chat_prompt_template, output_key="triples")

with open('../../data/train.json', 'r', encoding='utf-8') as f:
    train_lines = [json.loads(line) for line in f.readlines()]
with open('../../data/valid1.json', 'r', encoding='utf-8') as f:
    valid1_lines = [json.loads(line) for line in f.readlines()]
with get_openai_callback() as cb:
    for idx, aline in enumerate(train_lines):
        if idx ==2235:
            example_input = train_lines[2236]['input']
            example_required_relations = train_lines[2236]['instruction'].split('：')[1].split('，')[0]
            example_output = train_lines[2236]['output']
            cate = aline['cate']
            description = aline['input']
            required_relations = aline['instruction'].split('：')[1].split('，')[0]
            
            print("summary:", ">"*10)
            print(description)
            input = {"description": description, "required_relations": required_relations, "example_input": example_input, "example_output": example_output, "example_required_relations": example_required_relations}
            res = extract_chain(input)
            print("required_relations", "-"*10)
            print(required_relations)
            print("triples", "-"*10)
            print(res['triples'])
            print(aline['output'])

    print("="*10, 'end', "="*10)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")