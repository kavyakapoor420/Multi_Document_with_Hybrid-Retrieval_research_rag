import fitz  # PyMuPDF
from typing import List,Dict
import os 

class PDFLoader:

    def __init__(self):
        pass 

    def extract_text_from_pdf(self,pdf_path:str,original_filename:str=None)->List[Dict]:
        """
           Extract text from pdf page by page 
           Returns: list of {page_number,text,source_file}

        """

        doc=fitz.open(pdf_path)
        pages_data=[]

        # use original filename if provided otherwise fall back to path basename
        source_filename=original_filename if original_filename else os.path.basename(pdf_path)

        for page_num in range(len(doc)):
            page=doc.load_page(page_num)
            text=page.get_text() 

            if text.strip(): # only add pages with content 
                pages_data.append({
                    "page_number":page_num+1,
                    "text":text,
                    "source_file":source_filename
                })

        doc.close() 

        return pages_data 
    
    def process_multiple_pdfs(self,pdf_paths:List[str])->List[Dict]:
        """
           process multiple pdfs and return combined page data
        """
        all_pages=[]

        for pdf_path in pdf_paths:
            try:
                pages=self.extract_text_from_pdf(pdf_path)
                all_pages.extend(pages)
                
            except Exception as e:
                print(f"error prcessing {path_path}:{str(e)}")
                continue 

        return all_pages 
