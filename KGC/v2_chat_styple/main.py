import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain.callbacks import get_openai_callback
from template import (
    SystemInstructionTemplate,
    HumanExampleTemplate,
    AIExampleTemplate,
    HumanInputTemplate
)
from utils import load_json

train_path = '../../data/train.json'
valid1_path = '../../data/valid1.json'

system_instruction_prompt = SystemMessagePromptTemplate.from_template(
    SystemInstructionTemplate
)
human_example_prompt = HumanMessagePromptTemplate.from_template(
    HumanExampleTemplate
)
ai_example_prompt = AIMessagePromptTemplate.from_template(
    AIExampleTemplate
)
human_input_prompt = HumanMessagePromptTemplate.from_template(
    HumanInputTemplate
)

train_lines, idx_type_dict, type_idx_dict = load_json(train_path)
valid1_lines, idx_type_dict, type_idx_dict = load_json(valid1_path)



with get_openai_callback() as cb:
    example_idxs = [0, 1]
    input_idx = 10

    few_shot_human_example_prompt = [
        human_example_prompt.format(
            example_description=train_lines[idx]['input'],
            example_required_relations=train_lines[idx]['required_relations']
        )
        for idx in example_idxs
    ]

    few_shot_ai_example_prompt = [
        ai_example_prompt.format(
            example_triples=train_lines[idx]['output']
        )
        for idx in example_idxs
    ]

    _few_shot_prompt = [[few_shot_human_example_prompt[idx],few_shot_ai_example_prompt[idx]] for idx, _ in enumerate(few_shot_ai_example_prompt)]
    few_shot_prompt = [elem for sublist in _few_shot_prompt for elem in sublist]
    
    chat_prompt = ChatPromptTemplate.from_messages([
        system_instruction_prompt,
        *few_shot_prompt,
        human_input_prompt
    ])

    chat = ChatOpenAI(temperature=0)
    chain = LLMChain(llm=chat, prompt=chat_prompt, output_key="output")
    response = chain.run(
        description = train_lines[input_idx]['input'],
        required_relations = train_lines[input_idx]['required_relations'],
    )
    print("predict triples:\n", response)
    print("real triples:\n", train_lines[input_idx]['output'])

    print("="*10, 'end', "="*10)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")