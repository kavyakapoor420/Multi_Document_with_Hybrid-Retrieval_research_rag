from sentence_transformer import SentenceTransformer
import numpy as np 
from typing import List,Dict 
from ..utils.config import config 

class EmbeddingService:

    def __init__(self):
        self.model=SentenceTransformer(config.EMBEDDING_MODEL)

    def generate_embeddings(self,texts:str)->np.ndarray:
        """
           generate embeddings for a single text
        """
        embeddings=self.model.encode(texts,show_progess_bar=True)
        return embeddings
    
    
    def generate_single_embedding(self,text:str)->np.ndarray:
        """
           generate embedding for a single text
        """
        embedding=self.model.encode(text)
        return embedding[0]
    
    def process_chunks_to_embeddings(self,chunks:List[Dict])->tuple:

        """
           process chunks and return embeddings with metadata
           returns : (embeddings_array,chunk_data_list)

        """

        texts=[chunk["text"]  for chunk in chunks]

        embeddings=self.generate_embeddings(texts)

        #prepare chunk data with embeddings 
        chunk_data=[]
        for i, chunk in enumerate(chunks):
            chunk_data.append({
                "text":chunk["text"],
                "metadata":chunk["metadata"],
                "embedding":embeddings[i]
            })

        return embeddings,chunk_data
