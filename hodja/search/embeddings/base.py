"""Interface for embedding models."""
from abc import ABC, abstractmethod
import numpy as np

class Embeddings(ABC):
    """Interface for embeddings."""

    @abstractmethod
    def embed(self, documents, **kwargs):
        """Embed documents."""