from typing import Any, Dict, List

node_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {labels: nodeLabels, properties: properties} AS output
"""

rel_properties_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE NOT type = "RELATIONSHIP" AND elementType = "relationship"
WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
RETURN {type: nodeLabels, properties: properties} AS output
"""

relationships_query = """
CALL apoc.meta.data()
YIELD label, other, elementType, type, property
WHERE type = "RELATIONSHIP" AND elementType = "node"
RETURN "(:" + label + ")-[:" + property + "]->(:" + toString(other[0]) + ")"
AS output
"""


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

    def query(self, query: str, params: dict = {}) -> List[Dict[str, Any]]:
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
