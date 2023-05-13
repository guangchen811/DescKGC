import json

# data/train.json

with open('data/train.json', encoding='utf-8') as f:
    lines = f.readlines()
records = [json.loads(line) for line in lines]
print(records[0])

from kor.extraction import create_extraction_chain
from kor.nodes import Object, Text, Number
from langchain.chat_models import ChatOpenAI


schema = Object(
    id="person",
    description="Personal information",
    examples=[
        ("Alice and Bob are friends", [{"first_name": "Alice"}, {"first_name": "Bob"}])
    ],
    attributes=[
        Text(
            id="first_name",
            description="The first name of a person.",
        )
    ],
    many=True,
)