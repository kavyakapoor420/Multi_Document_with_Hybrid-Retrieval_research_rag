import tiktoken
from typing import List,Dict
from ..utils.preprocessing import TextPreprocessor 
from ..utils.config import config 

class TextSplitter:
    def __init__(self):
        self.preprocessor=TextPreprocessor
        self.encoding=tiktoken.get_encoding('cl100k_base')
        self.chunk_size=config.CHUNK_SIZE
        self.chunk_overlap=config.CHUNK_OVERLAP

    def count_tokens(self,text:str)->int:
        """count tokens in text"""
        return len(self.encoding.encode(text))
    
    #clean the text first 
    #split text into sentences for better chunks boundaries
    #iterate through sentences and create chunks based on token count-> if adding this sentence would exceed chunks size, save current chunk 
    #start new chunk with overlap from previous chunk

    def split_text_into_chunks(self,text:str,metadata:Dict)->List[Dict]:
        """split text into chunks with metadata"""

        cleaned_text=self.preprocessor.clean_text(text)

        sentences=self.preprocessor.split_into_sentences(cleaned_text)

        chunks=[]
        current_chunks=''
        current_token=0

        for sentence in sentences:
            sentence_tokens=self.count_tokens(sentence)

            if current_token+sentence_token>self.chunk_size and current_chunk:
                chunks.append({
                    "text":current.chunk.strip() ,
                    "tokens":current_token,
                    "metadata":metadata.copy() 
                })

                overlap_text=self._get_overlap_text(current_chunk)
                current_chunk=overlap_text+' '+sentence
                current_tokens=self.count_tokens(current_chunk)
            else:
                current_chunk+=' '+sentence
                current_token+=sentence_tokens

         # add the last chunk
        if current_chunk.strip():
            chunks.append({
                "text":current_chunks.strip(),
                "tokens":current_tokens,
                "metadata":metadata.copy() 
            })


        return chunks 

    def _get_overlap_text(self,text:str)->str:
        """get overlap text from ed of current chunk"""
        words=text.split() 
        overlap_words=words[-self.chunk_overlap:] if len(words)>self.chunk_overlap else words

        return ' '.join(overlap_words)
    
    def process_pages_to_chunks(self,pages_data:List[Dict])->List[Dict]:
        """convert page data to chunks"""
        all_chunks=[]

        chunk_id=0

        for page_dta in pages_data:
            metadata={
                "source_file":page_data["source_file"],
                "page_number":page_data["page_number"],
                "chunk_id":chunks_id 
            }

            chunks=self.split_text_into_chunks(page_data['text'],metadata)

            for chunk in chunks:
                chunk['metadata']['chunk_id']=chunk_id 
                all_chunks.append(chunk)
                chunk_id+=1

            return all_chunks 