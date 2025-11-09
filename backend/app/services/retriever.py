from typing import List,Dict, Tuple 
import numpy as np 
from .bm25_index import BM25Index 
from .embeddings import EmbeddingService
from ..database.chroma_store import ChromaStore 
from ..utils.config import config 

class HybridRetriever:

    def __init__(self,bm25_index_path:str='./bm25_index.pkl',chorma_db_path:str=None):
        self.bm25_index=BM25Index(bm25_index_path)
        self.chroma_store=ChromaStore(chorma_db_path)
        self.embedding_service=EmbeddingService() 

        # load exisitng indices 
        self.bm25_index.load_index() 

    def add_documents(self,chunks:List[Dict]):

        """
          add documents to both BM25 and chroma indices

        """

        if not chunks:
            return 
        
        # add to BM25 index
        self.bm25_index.add_chunks(chunks)

        # generate embedding and add to chroma store 
        texts=[chunk["text"] for chunk in chunks]
        embeddings=self.embedding_service.generate_embeddings(texts)
        self.chroma_store.add_chunks(chunks,embeddings)

    def build_indices(self,chunks:List[Dict]):
        """
           Build both BM25 index and chroma index fromm scracth
         """
        
        if not chunks :
            return 
        
        # build bm25index 
        self.bm25_index.build_index(chunks)
        #reset and build chroma collection 
        self.chroma_store.reset_collection() 

        texts=[chunk["text"] for chunk in chunks]
        embeddings=self.embedding_service.generate_embeddings(texts)
        self.chroma_store.add_chunks(chunks,EmbeddingService)


    def hybrid_search(self,query:str,top_k:int=5,bm25_weight:float=0.5,embedding_weight:float=0.5,filter_criteria:Dict=None)->List[Dict]:

        """
          perform hybrid search combing BM25 and embedding similarity

          Args:
              query:Search Query
              top_k:number of results to return 
              bm25_weight:weight for Bm25 scores(0-1)
              embedding_weight:weight for embedding scores(0-1)
              filter_creteria:Optional filter criterai for search 

          Returns :
              List of ranked results with combined score 
        """

        #get bm25 results  -> get more to ensure diversity
        bm25_results=self.bm25_index.search(query,top_k=top_k*2,filter_criteria=filter_criteria) 

        # get embeddings results 
        query_embedding=self.embedding_service.generate_single_embedding(query)
        embedding_results=self.chroma_store.search(query,top_k=top_k*2,query_embedding=query_embedding,filter_criteria=filter_criteria)

        # combine and score results 
        combined_results=self._combine_result(bm25_results,embedding_results,bm25_weight,embedding_weight)


        # return top results 
        return combined_results[:top_k]
    
    
