from typing import Any, Dict, List

from neo4j import Query

from .cypher_template import (ARXIV_PAPER_INSERT_INSTRUCTION,
                              DELETE_NODES_INSTRUCTION,
                              DETACH_AUTHOR_FROM_PAPER_INSTRUCTION)
from .utils import join_if_list

node_properties_query = Query("""
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output
""")

rel_properties_query = Query("""
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
""")

relationships_query = Query("""
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN "(:" + label + ")-[:" + property + "]->(:" + toString(other[0]) + ")"
AS output
""")


class Neo4jGraph:
    """Neo4j wrapper for graph operations."""

    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        database: str = "neo4j",
        **kwargs,
    ) -> None:
        """Create a new Neo4j graph wrapper instance."""
        try:
            import neo4j
        except ImportError:
            raise ValueError(
                "Could not import neo4j python package. "
                "Please install it with `pip install neo4j`."
            )

        self._driver = neo4j.GraphDatabase.driver(
            url, auth=(username, password)
        )
        self._database = database
        self.schema = ""
        self.node_properties = {}
        self.rel_properties = {}
        self.relationships = []
        try:
            self.refresh_schema()
        except neo4j.exceptions.ClientError:
            raise ValueError(
                "Could not use APOC procedures. "
                "Please install the APOC plugin in Neo4j."
            )

    @property
    def get_schema(self) -> str:
        """Returns the schema of the Neo4j database"""
        return self.schema

    @property
    def get_node_properties(self) -> List[Dict[str, Any]]:
        """Returns the node properties of the Neo4j database"""
        return self.node_properties

    @property
    def get_rel_properties(self) -> List[Dict[str, Any]]:
        """Returns the relationship properties of the Neo4j database"""
        return self.rel_properties

    @property
    def get_relationships(self) -> List[str]:
        """Returns the relationships of the Neo4j database"""
        return self.relationships

    def query(self, query: Query, params: dict = {}) -> List[Dict[str, Any]]:
        """Query Neo4j database."""
        from neo4j.exceptions import CypherSyntaxError

        with self._driver.session(database=self._database) as session:
            try:
                data = session.run(query, params)
                return [r.data() for r in data]
            except CypherSyntaxError as e:
                raise ValueError(
                    "Generated Cypher Statement is not valid\n" f"{e}"
                )

    def refresh_schema(self) -> None:
        """
        Refreshes the Neo4j graph schema information.
        """
        node_properties = self.query(node_properties_query)
        relationships_properties = self.query(rel_properties_query)
        relationships = self.query(relationships_query)

        self.schema = f"""
        Node properties are the following:
        {[el['output'] for el in node_properties]}
        Relationship properties are the following:
        {[el['output'] for el in relationships_properties]}
        The relationships are the following:
        {[el['output'] for el in relationships]}
        """
        self.node_properties = [el["output"] for el in node_properties]
        self.rel_properties = [el["output"] for el in relationships_properties]
        self.relationships = [el["output"] for el in relationships]

    def _devide_author_from_arxiv_nodes(self) -> None:
        cypher_insturction = DETACH_AUTHOR_FROM_PAPER_INSTRUCTION
        self.query(cypher_insturction)

    def _delete_by_type(self, type: str) -> None:
        cypher_insturction = DELETE_NODES_INSTRUCTION.format(type=type)
        self.query(cypher_insturction)

    def _get_arxiv_paper_insert_instruction(self, arxiv_dict, uuid_):
        return ARXIV_PAPER_INSERT_INSTRUCTION.format(
            title=join_if_list(arxiv_dict["title"]),
            authors=join_if_list(arxiv_dict["authors"]),
            published=join_if_list(arxiv_dict["published"]),
            updated_date=join_if_list(arxiv_dict["updated_date"]),
            summary=join_if_list(arxiv_dict["summary"].replace("\n", " ")).replace('"', '`'),
            doi=join_if_list(arxiv_dict["doi"]),
            primary_category=join_if_list(arxiv_dict["primary_category"]),
            categories=join_if_list(arxiv_dict["categories"]),
            pdf_url=join_if_list(arxiv_dict["pdf_url"]),
            uuid=uuid_,
        )

    def _show_current_index(self) -> list:
        """return a list of index names"""
        cypher_insturction = """SHOW INDEXES"""
        index_list = self.query(cypher_insturction)
        index_list = [index["name"] for index in index_list]
        return index_list

    def create_or_update_index_on_unique_property(self, property_name: str) -> None:
        """update index for a given attribute"""
        if f"{property_name}_index" in self._show_current_index():
            cypher_drop_insturction = f"""DROP INDEX {property_name}_index"""
            self.query(cypher_drop_insturction)
        entity_types = self._get_entity_types_with_unique_prop(property_name)
        str_entity_types = " | ".join(entity_types)
        cypher_insturction = f"""CREATE FULLTEXT INDEX {property_name}_index
        FOR (n:{str_entity_types})
        ON EACH [n.{property_name}]"""
        self.query(cypher_insturction)

    def search_by_index(self, property_name: str, search_string: str) -> list:
        """search by index"""
        cypher_insturction = f"""CALL db.index.fulltext.queryNodes("{property_name}_index", "{search_string}")
        YIELD node, score
        RETURN node.title, score"""
        res = self.query(cypher_insturction)
        # convert to list of pairs
        res = [(pair["node.title"], pair["score"]) for pair in res]
        print(res)
        return res
