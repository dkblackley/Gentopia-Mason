from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator
import requests
from pypdf import PdfReader
from io import BytesIO


class ParsePdf(BaseTool):
    name = "parse_pdf"
    description: str = ("parses a pdf and returns a page."
                   "input a url to a pdf you found on the internet."
                   "also input the \"page_number\" that you want."
                   )

    def _run(self, url: AnyStr, page_number: int = 0) -> AnyStr:

        response = requests.get(url)
        response.raise_for_status()
        content_dump = BytesIO(response.content)
        reader = PdfReader(content_dump)
        page = reader.pages[page_number]
        page_text = page.extract_text()

        return page_text


    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

class ParsePdfMetadata(BaseTool):
    name = "pdf_metadata"
    description: str = ("returns the author or any pdf metadata if availible."
                        "this might not give useful information."
                        "input a url to a pdf you found on the internet."
                        )

    def _run(self, url: AnyStr) -> AnyStr:
        response = requests.get(url)
        response.raise_for_status()
        pdf_stream = BytesIO(response.content)
    
        reader = PdfReader(pdf_stream)
        metadata = reader.metadata
        metadata_str = "\n\n".join(f"{key}: {value}" for key, value in metadata.items())
        
        return metadata_str

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
    
if __name__ == "__main__":
    ans = ParsePdf()._run("https://crypto.stanford.edu/~dabo/courses/cs355_fall07/pir.pdf")
    print("output")
    print(ans)

    ans = ParsePdfMetadata()._run("https://crypto.stanford.edu/~dabo/courses/cs355_fall07/pir.pdf")
    print("output")
    print(ans)
