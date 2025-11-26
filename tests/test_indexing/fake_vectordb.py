# tests/test_indexing/fake_vectordb.py

class FakeVectorDB:
    """
    Simple fake vector database storing documents in memory.
    """

    def __init__(self):
        self.docs = []
        self.added = 0

    def add_documents(self, docs):
        self.docs.extend(docs)
        self.added += len(docs)

    def save_local(self, path):
        # no-op
        pass

    @classmethod
    def from_documents(cls, docs, embeddings):
        instance = cls()
        instance.add_documents(docs)
        return instance

    @classmethod
    def load_local(cls, path, embeddings, allow_dangerous_deserialization=False):
        # simulate empty load
        return cls()

    def as_retriever(self, search_kwargs=None):
        """
        Return a fake retriever that returns the first k docs.
        """
        k = search_kwargs.get("k", 3)

        class FakeRetriever:
            def __init__(self, docs, k):
                self.docs = docs
                self.k = k

            def get_relevant_documents(self, query):
                return self.docs[: self.k]

        return FakeRetriever(self.docs, k)
