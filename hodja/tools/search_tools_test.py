"""Unit tests for search_tools.py"""

import unittest
from hodja.search.docstores import FAISS
from hodja.tools.search_tools import SearchTool
from hodja.search.docstores_test import dummy_embeding_function
from hodja.search.documents import Document

class TestSearchTool(unittest.TestCase):

    def test_init(self):
        """Test the init method."""
        docstore = FAISS(dummy_embeding_function)
        search_tool = SearchTool(docstore)
        self.assertEqual(search_tool.docstore, docstore)

    def test_run(self):
        """Test the run method."""
        docstore = FAISS(dummy_embeding_function)
        search_tool = SearchTool(docstore)
        document = Document(text="test", id=1)
        search_tool.add_docs([document])
        self.assertEqual(search_tool.run("test"), [document])

    def test_add_docs(self):
        """Test the add_docs method."""
        docstore = FAISS(dummy_embeding_function)
        search_tool = SearchTool(docstore)
        document = Document(text="test", id=1)
        search_tool.add_docs([document])
        self.assertEqual(search_tool.docstore.documents, [document])


if __name__ == "__main__":
    unittest.main()