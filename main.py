import json
from langchain.chat_models import ChatOpenAI
from src.tools.extractor.base import init_extract_chain
from src.tools.neo4j.base import Neo4jManager

llm = ChatOpenAI(temperature=0.3)
extract_chain = init_extract_chain(llm)

db_manager = Neo4jManager()
# print(db_manager.graph_schema)

def extract_entities_from_paper(doi):
    summary = db_manager.graph.query(
        "MATCH (n:Paper) WHERE n.doi=$doi RETURN n.summary as summary",
        params={"doi": doi}
    )
    res = extract_chain({"topic":"network science", "summary":summary}, verbose=False)
    cypher_instruction = """
    MATCH (n:Paper) WHERE n.doi='10.1016/j.physleta.2014.02.010'
    MERGE (x:)
    RETURN n
    """
    # TODO: the instruction above need to be completed.
    return res

res = extract_chain({"topic":"network science", "summary":summary_2}, verbose=False)
print(res)