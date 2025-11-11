import chromadb
from chromadb.config import Settings
import numpy as np
import os 
from typing import List,Dict,Tuple,Optional
import uuid 
from ..utils.config import config 


class ChromaStore:

       def __init__(self,db_path:str=None):
            self.db_path=db_path or config.CHROMA_DB_PATH 
            self.client=None
            self.collection=None
            self.collection_name="pdf_chunks"
            self._intialize_client() 

       def _initialize_client(self):
            """
              initilize chroma client and collection
            """

            #create directpry if it doesnt exits 
            os.makedirs(self.db_path,exist_ok=True)

            #intialize chroma client with persistent storage 
            self.client=chromadb.PersistentClient(
                  
                  path=self.db_path,
                  settings=Settings(
                        anonymized_telemetry=False,
                        allow_reset=True 
                  )
            )

            # get or create collection 
            try:
                  self.collection=self.client.get_collection(name=self.collection_name)

            except Exception:
                  #collection doesnt exists create it 
                  name=self.collection_name
                  metadata={
                        "desription":"PDF document chunk for Q&A"
                  }
       
       def add_chunks(self,chunks:List[Dict],embeddings:Optional[np.ndarray]=None):
             """
                add chunks to chroma collection
             """