"""Wrapper around OpenAI embedding models."""
import os
import numpy as np
from hodja.search.embeddings.base import Embeddings
import openai

class OpenAIEmbeddings(Embeddings):
    """Wrapper around OpenAI embedding models."""

    def __init__(self, model_name="text-embedding-ada-002", openai_api_key=None):
        """Initialize OpenAIEmbeddings.

        Args:
            model_name: The name of the model to use. The default is
                ``text-embedding-ada-002``. See
                https://beta.openai.com/docs/engines for a list of available
                models.
            openai_api_key: The API key to use. If not provided, will look for
                the environment variable ``OPENAI_API_KEY``.
        """
        self.model_name = model_name
        if openai_api_key is None:
            openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.client = openai.Embedding

    def embed(self, texts, batch_size=1000):
        """Call out to OpenAI's embedding endpoint for embedding search docs.

        Args:
            texts (List[str]): The texts to embed.
            batch_size (int): The maximum number of documents to send to OpenAI at once.

        Returns:
            List of embeddings, one for each document.
        """
        results = []
        for i in range(0, len(texts), batch_size):
            response = self.client.create(
                input=texts[i : i + batch_size], engine=self.model_name
            )
            results += [r["embedding"] for r in response["data"]]
        return results
