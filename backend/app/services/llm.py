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
    
    def generate_answer(self,query:str,context_chunks:List[Dict],max_tokens:int=1000)->Dict :
        """
           generate answer using gemini api with retrived context 
        """
        
            