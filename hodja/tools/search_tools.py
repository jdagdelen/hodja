from hodja.search.docstores import FAISS
from hodja.tools.base import Tool


class SearchTool(Tool):
    """Tool for wrapping a DocStore so an Agent can search for relevant documents."""
    def __init__(
        self,
        docstore,
        name="Search", 
        description="Search for documents based on a query. Returns a list of documents that best match the query.", 
        instructions="Provide query as text."):
        super().__init__(name, description, instructions)
        self.docstore = docstore

    def run(self, query, top_k=10):
        """Search for documents similar to a query.

        Args:
            query: Query to search for.
            top_k: Number of top documents to return.

        Returns:
            List of top documents.
        """
        results = self.docstore.search(query, min(top_k, len(self.docstore)))
        return results

    def add_docs(self, docs):
        """Add documents to the docstore."""
        # TODO: update so that you don't have to add one doc at a time
        for doc in docs:
            self.docstore.add(doc)


