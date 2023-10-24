import uuid
from typing import Tuple

from DescKGC.tools.chroma.base import ChromaVectorStore
from DescKGC.tools.neo4j.base import Neo4jGraph
from .utils import validate_keys


class DBManager:
    def __init__(
        self,
        url,
        username,
        password,
        chroma_db_impl,
        persist_directory,
        collection_name,
        **kwargs,
    ):
        self.graph_db = self.init_graph_db(url, username, password, kwargs)
        self.vector_db = self.init_vector_db(chroma_db_impl, persist_directory, collection_name, kwargs)
        self.update_schema()

    def init_vector_db(self, chroma_db_impl: str, persist_directory: str, collection_name: str, kwargs) -> ChromaVectorStore:
        """Initialize the vector database.
        :param chroma_db_impl: the implementation of the vector database.
        :type chroma_db_impl: str
        :param persist_directory: the directory to store the vector database.
        :type persist_directory: str
        :param collection_name: the name of the collection.
        :type collection_name: str
        :param kwargs: the keyword arguments for the vector database.
        :type kwargs: dict
        :return: the vector database.
        :rtype: ChromaVectorStore
        """
        vector_db = ChromaVectorStore(
            chroma_db_impl=chroma_db_impl,
            persist_directory=persist_directory,
            collection_name=collection_name,
            **kwargs,
        )
        return vector_db

    def init_graph_db(self, url: str, username: str, password: str, kwargs) -> Neo4jGraph:
        """Initialize the graph database.
        :param url: the url of the graph database.
        :type url: str
        :param username: the username of the graph database.
        :type username: str
        :param password: the password of the graph database.
        :type password: str
        :param kwargs: the keyword arguments for the graph database.
        :type kwargs: dict
        :return: the graph database.
        :rtype: Neo4jGraph
        """
        graph_db = Neo4jGraph(url=url, username=username, password=password, **kwargs)
        return graph_db

    def close_driver(self):
        self.graph_db._driver.close()

    def add_from_arxiv(self, arxiv_papers, arxiv_prefix, vs_key_info):
        embedding_key = vs_key_info["embedding_key"]
        metadata_keys = vs_key_info["metadata_keys"]
        paper_keys = arxiv_papers[0].keys()
        expected_keys = [embedding_key, *metadata_keys]
        validate_keys(expected_keys, paper_keys)
        cypher_insturction_and_uuid_list = [self._arxiv_paper_to_cypher(paper, arxiv_prefix) for paper in arxiv_papers]

        for (cypher_insturction, uuid_), paper in zip(cypher_insturction_and_uuid_list, arxiv_papers):
            try:
                self.graph_db.query(cypher_insturction)
                metadata = {metadata_key: paper[metadata_key] for metadata_key in metadata_keys}
                metadata["embedding_source"] = embedding_key
                metadata["doc_source_type"] = "provided"
                metadata["type"] = "arxiv"
                self.vector_db.add(
                    documents=[paper[embedding_key]],
                    metadatas=[metadata],
                    ids=[uuid_],
                )
            except Exception as e:
                # TODO: make this Exception more specific
                print(f"arxiv paper insert error: {str(e)}")
        self._devide_author_from_arxiv_nodes()
        # self.update_schema()

    def _devide_author_from_arxiv_nodes(self) -> None:
        """extract author nodes from arxiv nodes in neo4j database"""
        self.graph_db._devide_author_from_arxiv_nodes()
        self.update_schema()

    def _arxiv_paper_to_cypher(self, arxiv_dict: dict, arxiv_prefix: str) -> Tuple[str, str]:
        """
        input: an arxiv res dict return from response_to_json
        output: a cypher CREATE instruction
        """
        uuid_ = f"{arxiv_prefix}-{uuid.uuid4()}"
        cypher_insturction = self.graph_db._get_arxiv_paper_insert_instruction(arxiv_dict, uuid_)
        return cypher_insturction, uuid_

    def show_schema(self) -> None:
        import json

        self.graph_db.refresh_schema()
        # print(self.graph_schema)
        print("Node properties are the following:")
        for node in self.node_properties:
            print(json.dumps(node, indent=4))

        print("\nRelationship properties are the following:")
        for relationship in self.rel_properties:
            print(json.dumps(relationship, indent=4))

        print("\nThe relationships are the following:")
        for rel in self.relationships:
            print(rel)

    def update_schema(self) -> None:
        self.graph_db.refresh_schema()
        self.graph_schema = self.graph_db.get_schema
        self.node_properties = self.graph_db.get_node_properties
        self.rel_properties = self.graph_db.get_rel_properties
        self.relationships = self.graph_db.get_relationships

    def delete_by_type(self, type: str) -> None:
        """
        delete all nodes of a type.
        TODO: implement delete by attribute
        """
        self.graph_db._delete_by_type(type)
        self.update_schema()

    def _get_entity_types_with_unique_prop(self, prop_name: str) -> list:
        """return a list of entity types that have unique prop_name"""
        SEARCH_INSTURCTION = f"""MATCH (n)
        WHERE n.{prop_name} is not NULL
        RETURN DISTINCT labels(n) AS labels"""
        entity_types = self.graph_db.query(SEARCH_INSTURCTION)
        entity_types = [entity_type["labels"][0] for entity_type in entity_types]
        return entity_types

    def get_node_labels(self):
        cypher_insturction = """CALL apoc.meta.data()
        YIELD label, other, elementType, type, property
        WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
        WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
        RETURN {labels: nodeLabels} AS output"""
        res = self.graph_db.query(cypher_insturction)
        return [label["output"]["labels"] for label in res]
