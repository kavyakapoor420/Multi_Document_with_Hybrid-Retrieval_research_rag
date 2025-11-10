import requests 
import json 
from typing import List,Dict,Optinal 
from ..utils.config import config 

api_url="https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent"

class GeminiLLMService:

    def __init__(self):
        self.api_key=config.GEMINI_API_KEY 
        self.base_url=api_url

        if not self.api_key:
            raise ValueError("Gemini api key is required")
    
    def generate_answer(self,query:str,context_chunks:List[Dict],max_tokens:int=1000)->Dict:
        """
          generate answer using gemini api with retreived context 

          Args:
              query: users question
              context_chunks: List of relevant chunks from retrieval
              max_tokens:Maximum tokens in response 

          Returns:
              Dict with answer and metadata 
        """
# first prepare the context from chunks then create prompt(means augment the query prompt with relevant chunks  )
        try:
            #prepare context from chunks 
            context=self._prepare_context(context_chunks)

            #create prompt 
            prompt=self._create_prompt(query,context)

            #call gemini api 
            response=self._call_gemini_api(prompt,max_tokens)

            #process response 
            answer=self._extract_answer(response)

            #prepare sources 
            sources=self._prepare_sources(context_chunks)

        except Exception as e:
            return{
                "answer":f"I appologoize but i encountered while processing your question:{str(e)}",
                "sources":[],
                "context_used":0,
                "sucess":False,
                "error":str(e)
            }
        
    def _prepare_context(self,chunks:List[Dict])->str:
        """
           prepare context string from retreived chunks
        """

        if not chunks:
            return "no relevant chunks found"
        
        context_parts=[]

        for i,chunk in enumerate(chunks,1):
            metadata=chunk.get("metadata",{})
            source_files=metadata.get('source_file',"Unknown")
            page_number=metadata.get("page_number","Unknwon")

            context_part=f"""
                Context {i} (Source :{source_files},Pages:{page_number}) :
                                                {chunk.get("text","")}

            """

            context_part.append(context_part)

        return '\n'.join(context_parts)