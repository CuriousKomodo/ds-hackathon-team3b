from dotenv import load_dotenv
from tqdm import tqdm
import numpy as np
from bertopic.backend import BaseEmbedder
load_dotenv()
class WiseLLMEmbedder(BaseEmbedder):
    def __init__(self, embedding_model):
        super().__init__()
        self.embedding_model = embedding_model

    def embed(self, documents, verbose=False):
        embeddings = []
        for document in tqdm(documents):
            embedding = self.embedding_model.embed_query(document)
            embeddings.append(np.array(embedding))
        return np.vstack(embeddings)
