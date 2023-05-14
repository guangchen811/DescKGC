import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


if __name__ == '__main__':
    from template import ENTITY_EXTRACT_TEMPLATE
    llm = OpenAI()
    prompt = PromptTemplate(
        input_variables=['summary'],
        template=ENTITY_EXTRACT_TEMPLATE
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    print(chain.run())