from typing import Type

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


class ChromaVectorStore:
    def __init__(self, chroma_db_impl, persist_directory, collection_name, distance_function, **kwargs) -> None:
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl=chroma_db_impl,
                persist_directory=persist_directory,
            )
        )
        self.collection_name = collection_name
        assert distance_function in [
            "cosine",
            "l2",
            "ip",
        ], """
        distance function should be one of cosine, l2, ip"""
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
            metadata={"hnsw:space": distance_function},
        )
        # hnsw doc can be seen at
        # https://github.com/nmslib/hnswlib/tree/master#python-bindings.
        self.client.persist()

    def clear_collection(self):
        self.client.delete_collection(name=self.collection_name)
        self.client.persist()

    def add(self, documents, metadatas, ids):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        self.client.persist()

    def get_by_uuid(self, uuid):
        return self.collection.get(
            ids=uuid,
        )

    def get_name_description_by_uuid(self, uuid):
        results = self.collection.get(
            ids=uuid,
        )
        names = [metadata["name"] for metadata in results["metadatas"]]
        descriptions = results["documents"]
        assert len(names) == len(descriptions)
        pairs = list(zip(names, descriptions))
        return pairs

    def get_from_specific_source(self, source):
        if source == "provided":
            embedding_source = "summary"
        elif source == "generated":
            embedding_source = "description"
        else:
            raise ValueError("embedding source should be either provided or generated")
        return self.collection.get(where={"embedding_source": embedding_source})

    def get_specific_type_nodes_uuid(self, node_type):
        nodes = self.collection.get(where={"type": node_type})
        return nodes["ids"]

    def query(self, query_texts, n_results, **kwargs):
        results = self.collection.query(query_texts=query_texts, n_results=n_results, **kwargs)
        # TODO: return ids and others necessary
        return results

    def query_from_specific_source(self, source, query_texts, n_results, **kwargs):
        if source == "provided":
            embedding_source = "summary"
        elif source == "generated":
            embedding_source = "description"
        else:
            raise ValueError("embedding source should be either provided or generated")
        results = self.collection.query(
            query_texts=query_texts, n_results=n_results, where={"embedding_source": embedding_source}, **kwargs
        )
        return results

    def query_from_specific_type(self, entity_type, query_texts, n_results, **kwargs):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where={"type": entity_type[0]},
            # TODO: make this `where` clause able to receive a list
            # by `or` operation.
            **kwargs
        )
        return results


ChromaVectorStoreType = Type[ChromaVectorStore]
