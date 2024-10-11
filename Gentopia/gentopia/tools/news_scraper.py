from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator
import requests
from pypdf import PdfReader
from io import BytesIO

class ScrapeHeadlines(BaseTool):
    name = "parse_pdf"
    description: str = ("parses a pdf and returns a page."
                   "input a url to a pdf you found on the internet."
                    "the url MUST end in \".pdf\". You can find links to pdfs via an internet search"
                   "also input the \"page_number\" that you want. Default is 0 (the first page)"
                   )
    args_schema: Optional[Type[BaseModel]] = PdfArg

    def _run(self) -> AnyStr:

        
        headlines = {}

        # Define the URLs to scrape from
        news_sites = {
            "BBC News": "https://www.bbc.com/news",
            "ABC News": "https://abcnews.go.com",
            "CNN": "https://edition.cnn.com",
            "Fox News": "https://www.foxnews.com"
        }

        # Loop through each site and scrape the headlines
        for site, url in news_sites.items():
            try:
                response = requests.get(url)
                response.raise_for_status()  # Check if the request was successful
                soup = BeautifulSoup(response.content, 'html.parser')
            
                # Scrape headlines based on each site's structure
                if site == "BBC News":
                    headlines[site] = [h3.get_text(strip=True) for h3 in soup.select("h3")]
            
                elif site == "ABC News":
                    headlines[site] = [a.get_text(strip=True) for a in soup.select("a[href*='/story']")]
            
                elif site == "CNN":
                    headlines[site] = [span.get_text(strip=True) for span in soup.select(".cd__headline-text")]
            
                elif site == "Fox News":
                    headlines[site] = [h2.get_text(strip=True) for h2 in soup.select(".title a")]

            except Exception as e:
                headlines[site] = f"Error fetching headlines: {e}"

        return headlines.join("\n\n")



    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchNewsArgs(BaseModel):
    url: str = Field(..., description="A url that points to a .pdf file. MUST END WITH \".pdf\"")
    page_num: int = Field(..., description="The page number you want, defaults to 0 (the first page)")


class SearchNews(BaseTool):
    name = "pdf_metadata"
    description: str = ("returns the author or any pdf metadata if availible."
                        "this might not give useful information."
                        "the url MUST end in \".pdf\". You can find links to pdfs via an internet search"
                        )
    args_schema: Optional[Type[BaseModel]] = PdfArg

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
    ans = ParsePdf()._run("https://eprint.iacr.org/2022/368.pdf")
    print("output")
    print(ans)

    ans = ParsePdfMetadata()._run("https://eprint.iacr.org/2022/368.pdf")
    print("output")
    print(ans)
