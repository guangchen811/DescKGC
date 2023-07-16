import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List


class ChromaVectorStore:
    def __init__(
        self,
        chroma_db_impl,
        persist_directory,
        collection_name,
        **kwargs
    ) -> None:
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl=chroma_db_impl,
                persist_directory=persist_directory
            )
        )
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction())
        self.client.persist()

    def clear_collection(self):
        self.client.delete_collection(name=self.collection_name)
        self.client.persist()

    def add(self, documents, metadatas, ids):
        self.collection.add(documents=documents, metadatas=metadatas, ids=ids)
        self.client.persist()

    def get_from_specific_source(self, source):
        if source == "provided":
            embedding_source = "summary" 
        elif source == "generated":
            embedding_source = "description"
        else:
            raise ValueError("embedding source should be either provided or generated")
        return self.collection.get(where={'embedding_source': embedding_source})

    def query(self, query_texts, n_results, **kwargs):
        results = self.collection.query(
            query_texts=query_texts,
            n_results=n_results,
            **kwargs
        )
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
            query_texts=query_texts,
            n_results=n_results,
            where={'embedding_source': embedding_source},
            **kwargs
        )
        return results