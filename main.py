import json
from langchain.chat_models import ChatOpenAI
from src.tools.extractor.base import init_extract_chain

with open('./data/network_science.json', 'r') as f:
    res = json.load(f)

llm = ChatOpenAI(temperature=0.3)
extract_chain = init_extract_chain(llm)

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