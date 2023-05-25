from langchain.graphs import Neo4jGraph
from .cypher_template import (
    ARXIV_PAPER_INSERT_INSTRUCTION
)
from tqdm import tqdm
def response_to_json(search_res):
    res = []
    for result in search_res.results():
        res.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "published": str(result.published),
            "updatedDate": str(result.updated),
            "summary": result.summary,
            "doi": result.doi,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "pdf_url": result.pdf_url,
        })
    return res

class Neo4jManager():
    def __init__(self):
        self.graph = Neo4jGraph(
            url="bolt://localhost:7687",
            username="neo4j",
            password="123./\.abc"
        )
        self.graph_schema = self.graph.get_schema
        self.arxiv_paper_insert_instruction = ARXIV_PAPER_INSERT_INSTRUCTION
    def add_from_arxiv(self, arxiv_res):
        cypher_insturction_list = [
            self._arxiv_res_to_cypher(res)
            for res in arxiv_res
        ]
        for cypher_insturction in cypher_insturction_list:
            try:
                self.graph.query(cypher_insturction)
            except Exception:
                print(f"arxiv paper insert error: {Exception}")
        self.update_schema()
    
    def _arxiv_res_to_cypher(self, arxiv_dict):
        """ input: an arxiv res dict return from response_to_json
            output: a cypher CREATE instruction
        """
        cypher_insturction = self.arxiv_paper_insert_instruction.format(
            title=self._join_if_list(arxiv_dict["title"]),
            authors=self._join_if_list(arxiv_dict["authors"]),
            published=self._join_if_list(arxiv_dict["published"]),
            updatedDate=self._join_if_list(arxiv_dict["updatedDate"]),
            summary=self._join_if_list(arxiv_dict["summary"].replace('\n', ' ')),
            doi=self._join_if_list(arxiv_dict["doi"]),
            primary_category=self._join_if_list(arxiv_dict["primary_category"]),
            categories=self._join_if_list(arxiv_dict["categories"]),
            pdf_url=self._join_if_list(arxiv_dict["pdf_url"])
        )
        return cypher_insturction
    def _join_if_list(self, input):
        if isinstance(input, list):
            return "||".join(input)
        else:
            return str(input)
        
    def update_schema(self):
        self.graph.refresh_schema()
        self.graph_schema = self.graph.get_schema