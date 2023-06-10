from .cypher_template import (
    ARXIV_PAPER_INSERT_INSTRUCTION,
    DELETE_NODES_INSTRUCTION,
    DETACH_AUTHOR_FROM_PAPER_INSTRUCTION
)
from .utils import response_to_json, join_if_list
from .neo4j_graph import Neo4jGraph

from tqdm import tqdm

class Neo4jManager():
    def __init__(self):
        self.graph = Neo4jGraph(
            url="bolt://localhost:7687",
            username="neo4j",
            password="123./\.abc"
        )
        self.update_schema()
    
    def add_from_arxiv(self, arxiv_res):
        cypher_insturction_list = [
            self._arxiv_res_to_cypher(res)
            for res in arxiv_res
        ]
        for cypher_insturction in cypher_insturction_list:
            try:
                self.graph.query(cypher_insturction)
            except Exception as e:
                print(f"arxiv paper insert error: {str(e)}")
        self._devide_author_from_arxiv_nodes()
        self.update_schema()

    def _devide_author_from_arxiv_nodes(self) -> None:
        """ extract author nodes from arxiv nodes in neo4j database """
        cypher_insturction = DETACH_AUTHOR_FROM_PAPER_INSTRUCTION
        self.graph.query(cypher_insturction)
        self.update_schema()
    
    def _arxiv_res_to_cypher(self, arxiv_dict: dict) -> str:
        """ input: an arxiv res dict return from response_to_json
            output: a cypher CREATE instruction
        """
        cypher_insturction = ARXIV_PAPER_INSERT_INSTRUCTION.format(
            title=join_if_list(arxiv_dict["title"]),
            authors=join_if_list(arxiv_dict["authors"]),
            published=join_if_list(arxiv_dict["published"]),
            updatedDate=join_if_list(arxiv_dict["updatedDate"]),
            summary=join_if_list(arxiv_dict["summary"].replace('\n', ' ')),
            doi=join_if_list(arxiv_dict["doi"]),
            primary_category=join_if_list(arxiv_dict["primary_category"]),
            categories=join_if_list(arxiv_dict["categories"]),
            pdf_url=join_if_list(arxiv_dict["pdf_url"])
        )
        return cypher_insturction
        
    def update_schema(self) -> None:
        self.graph.refresh_schema()
        self.graph_schema = self.graph.get_schema

    def delete_by_type(self, type: str) -> None:
        """ 
        delete all nodes of a type.
        TODO: implement delete by attribute
        """
        cypher_insturction = DELETE_NODES_INSTRUCTION.format(
            type=type
        )
        self.graph.query(cypher_insturction)
        self.update_schema()