from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator
import requests
from pypdf import PdfReader
from io import BytesIO

class PdfArg(BaseModel):
    url: str = Field(..., description="A url that points to a .pdf file. URL MUST END WITH \".pdf\"")
    page_num: int = Field(..., description="The page number you want, defaults to 0 (the first page)")

class ParsePdf(BaseTool):
    name = "parse_pdf"
    description: str = ("parses a pdf and returns a page."
                   "input a url to a pdf you found on the internet."
                    "the url MUST end in \".pdf\". You can find links to pdfs via an internet search"
                   "also input the \"page_number\" that you want. Default is 0 (the first page)"
                   )
    args_schema: Optional[Type[BaseModel]] = PdfArg

    def _run(self, url: AnyStr, page_num: int = 0) -> AnyStr:

        try:
        
            response = requests.get(url)
            response.raise_for_status()
            content_dump = BytesIO(response.content)
            reader = PdfReader(content_dump)
            page = reader.pages[page_num]
            page_text = page.extract_text()

            return page_text
        except Exception:
            return "Error reading pdf! Double check the url ends with .pdf and try to search for a different link if it doesn't"


    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class PdfMetadataArgs(BaseModel):
    url: str = Field(..., description="A url that points to a .pdf file")
   
    
class ParsePdfMetadata(BaseTool):
    name = "pdf_metadata"
    description: str = ("returns the author or any pdf metadata if availible."
                        "this might not give useful information."
                        "the url MUST end in \".pdf\". You can find links to pdfs via an internet search"
                        )
    args_schema: Optional[Type[BaseModel]] = PdfArg

    def _run(self, url: AnyStr) -> AnyStr:
        try:
            response = requests.get(url)
            response.raise_for_status()
            pdf_stream = BytesIO(response.content)
    
            reader = PdfReader(pdf_stream)
            metadata = reader.metadata
            metadata_str = "\n\n".join(f"{key}: {value}" for key, value in metadata.items())
        
            return metadata_str
        except Exception:
            return "Error extracting metadata!"
            

        

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
if __name__ == "__main__":
    ans = ParsePdf()._run("https://eprint.iacr.org/2022/368.pdf")
    print("output")
    print(ans)

    ans = ParsePdfMetadata()._run("https://eprint.iacr.org/2022/368.pdf")
    print("output")
    print(ans)
