import uuid
from typing import Tuple

from ..chroma.base import ChromaVectorStore
from ..neo4j.base import Neo4jGraph
from ..neo4j.cypher_template import (ARXIV_PAPER_INSERT_INSTRUCTION,
                                     DELETE_NODES_INSTRUCTION,
                                     DETACH_AUTHOR_FROM_PAPER_INSTRUCTION)
from ..neo4j.utils import join_if_list


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
        self.graph_db = Neo4jGraph(url=url, username=username, password=password, **kwargs)
        self.vector_db = ChromaVectorStore(
            chroma_db_impl=chroma_db_impl,
            persist_directory=persist_directory,
            collection_name=collection_name,
            **kwargs,
        )
        self.update_schema()

    def close_driver(self):
        self.graph_db._driver.close()

    def add_from_arxiv(self, arxiv_papers, arxiv_prefix, vs_key_info):
        embedding_key = vs_key_info["embedding_key"]
        metadata_keys = vs_key_info["metadata_keys"]
        paper_keys = arxiv_papers[0].keys()
        assert all(
            key in paper_keys for key in [embedding_key, *metadata_keys]
        ), """KeyError: some keys are not in the paper dict.
        Please check the vs_key_info in config.yaml"""
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
        # self._devide_author_from_arxiv_nodes()
        # self.update_schema()

    def _devide_author_from_arxiv_nodes(self) -> None:
        """extract author nodes from arxiv nodes in neo4j database"""
        cypher_insturction = DETACH_AUTHOR_FROM_PAPER_INSTRUCTION
        self.graph_db.query(cypher_insturction)
        self.update_schema()

    def _arxiv_paper_to_cypher(self, arxiv_dict: dict, arxiv_prefix: str) -> Tuple[str, str]:
        """
        input: an arxiv res dict return from response_to_json
        output: a cypher CREATE instruction
        """
        uuid_ = f"{arxiv_prefix}-{uuid.uuid4()}"
        cypher_insturction = ARXIV_PAPER_INSERT_INSTRUCTION.format(
            title=join_if_list(arxiv_dict["title"]),
            authors=join_if_list(arxiv_dict["authors"]),
            published=join_if_list(arxiv_dict["published"]),
            updated_date=join_if_list(arxiv_dict["updated_date"]),
            summary=join_if_list(arxiv_dict["summary"].replace("\n", " ")),
            doi=join_if_list(arxiv_dict["doi"]),
            primary_category=join_if_list(arxiv_dict["primary_category"]),
            categories=join_if_list(arxiv_dict["categories"]),
            pdf_url=join_if_list(arxiv_dict["pdf_url"]),
            uuid=uuid_,
        )
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
        cypher_insturction = DELETE_NODES_INSTRUCTION.format(type=type)
        self.graph_db.query(cypher_insturction)
        self.update_schema()

    def _get_entity_types_with_unique_prop(self, prop_name: str) -> list:
        """return a list of entity types that have unique prop_name"""
        SEARCH_INSTURCTION = f"""MATCH (n)
        WHERE n.{prop_name} is not NULL
        RETURN DISTINCT labels(n) AS labels"""
        entity_types = self.graph_db.query(SEARCH_INSTURCTION)
        entity_types = [entity_type["labels"][0] for entity_type in entity_types]
        return entity_types

    def _show_current_index(self) -> list:
        """return a list of index names"""
        cypher_insturction = """SHOW INDEXES"""
        index_list = self.graph_db.query(cypher_insturction)
        index_list = [index["name"] for index in index_list]
        return index_list

    def create_or_update_index_on_unique_property(self, property_name: str) -> None:
        """update index for a given attribute"""
        if f"{property_name}_index" in self._show_current_index():
            cypher_drop_insturction = f"""DROP INDEX {property_name}_index"""
            self.graph_db.query(cypher_drop_insturction)
        entity_types = self._get_entity_types_with_unique_prop(property_name)
        str_entity_types = " | ".join(entity_types)
        cypher_insturction = f"""CREATE FULLTEXT INDEX {property_name}_index
        FOR (n:{str_entity_types})
        ON EACH [n.{property_name}]"""
        self.graph_db.query(cypher_insturction)

    def search_by_index(self, property_name: str, search_string: str) -> list:
        """search by index"""
        cypher_insturction = f"""CALL db.index.fulltext.queryNodes("{property_name}_index", "{search_string}")
        YIELD node, score
        RETURN node.title, score"""
        res = self.graph_db.query(cypher_insturction)
        # convert to list of pairs
        res = [(pair["node.title"], pair["score"]) for pair in res]
        print(res)
        return res

    def get_node_labels(self):
        cypher_insturction = """CALL apoc.meta.data()
        YIELD label, other, elementType, type, property
        WHERE NOT type = "RELATIONSHIP" AND elementType = "node"
        WITH label AS nodeLabels, collect({property:property, type:type}) AS properties
        RETURN {labels: nodeLabels} AS output"""
        res = self.graph_db.query(cypher_insturction)
        return [label["output"]["labels"] for label in res]
