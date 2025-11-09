from rank_bm25 import BM250kapi 
import pickle
import os 
from typing import List,Dict,Tuple
import json


class BM25Index:
    

    def __init__(self,index_path:str='./bm25_index.pkl'):
        self.index_path=index_path
        self.corpus=[]
        self.bm25=None 
        self.chunk_metadata=[]

    def build_index(self,chunks:List[Dict]): 
        """
           Build bm25 index from text chunks
        """
        corpus=[]
        self.chunk_metadata=[]

        for chunk in chunks:
            #simple tokenization 
            tokens=chunk["text"].lower().split() 
            corpus.append(tokens)
            self.chunk_metadata.append(chunk["metadata"])

        self.corpus=corpus
        self.bm25=BM250kapi(corpus)

        #save index
        self.save_index() 

    def save_index(self):
        """
          save bm25 index to disk 
        """

        index_data={
            "courpus":self.corpus,
            "chunk_metadata":self.chunk_metadat 
        }

        with open(self.index_path,'w') as f:
            pickle.dump(index_data,f)
        
       #also save metadata seperately for easier access 
        metadata_path=self.index_path('.pkl',"_metadata.json")

        with open(metadata_path,'w') as f:
            json.dump(self.chunk_metadata,f,indent=2)
    
    def load_index(self):
        """
          load Bm25 index from disk
        """

        if not os.path.exists(self.index_path):
           return False 