import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.tools.extractor.template import ENTITY_EXTRACT_TEMPLATE, RELATION_EXTRACT_TEMPLATE

with open('./data/arxiv_network_science.json', 'r') as f:
    res = json.load(f)

llm = OpenAI(temperature=0.3)
entity_extract_prompt = PromptTemplate(
    input_variables=['summary'],
    template=ENTITY_EXTRACT_TEMPLATE
)
relation_extract_prompt = PromptTemplate(
    input_variables=['summary', 'entities'],
    template=RELATION_EXTRACT_TEMPLATE
)
entity_extract_chain = LLMChain(llm=llm, prompt=entity_extract_prompt, output_key="entities")
relation_extract_chain = LLMChain(llm=llm, prompt=relation_extract_prompt, output_key="relations")

extract_chain = SequentialChain(
    chains=[entity_extract_chain, relation_extract_chain],
    input_variables=["summary"],
    output_variables=["entities", "relations"],
    verbose=True)

for idx, a_res in enumerate(res):
    if idx >= 1:
        break
    summary = a_res['summary']
    print("summary:", ">"*10)
    print(summary)
    res = extract_chain({"summary":summary})
    print("entities", "-"*10)
    print(res['entities'])
    print("relations", "-"*10)
    print(res['relations'])