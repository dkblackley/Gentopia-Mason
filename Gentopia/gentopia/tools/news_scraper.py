from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator
import requests
from pypdf import PdfReader
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

class ScrapeHeadlines(BaseTool):
    name = "get_headlines"
    description: str = ("parses a pdf and returns a page."
                   "input a url to a pdf you found on the internet."
                    "the url MUST end in \".pdf\". You can find links to pdfs via an internet search"
                   "also input the \"page_number\" that you want. Default is 0 (the first page)"
                   )

    def _run(self) -> AnyStr:
        
        headlines = {}

        # These are the potential options I chose, but I suppose I could even let the LLM decide for me.
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
                response.raise_for_status() 
                soup = BeautifulSoup(response.content, 'html.parser')
            
                # Scrape headlines based on each site's HTML tags (Unfortunately will need constant updating with time)
                if site == "BBC News":
                    headlines[site] = [h.text.strip() for h in soup.select('h2[data-testid="card-headline"]')]
            
                elif site == "ABC News":
                    headlines[site] = [a.get_text(strip=True) for a in soup.select("a[href*='/story']")]
            
                elif site == "CNN":
                    headlines[site] = [h.text.strip() for h in soup.select('span.container__headline-text')]
            
                elif site == "Fox News":
                    headlines[site] = [h.text.strip() for h in soup.select('h3.title a')]

            except Exception as e:
                headlines[site] = f"Error fetching headlines: {e}"

        return "\n\n".join(f"{key}: {value}" for key, value in headlines.items())



    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


class SearchNewsArgs(BaseModel):
    query: str = Field(..., description="A phrase or word that you want to input into a news sites search box")


class SearchNews(BaseTool):
    name = "get_headlines"
    description: str = ("Returns 6 most recent headlines and articles for a given search term or keyword"
                        "Websites used are CNN and ABC News"
                        "This function can be useful if someone wants to know what's happening in a specific area"
                        "Can also be insightful if someone just asks a general question about something or someplace")
    args_schema: Optional[Type[BaseModel]] = SearchNewsArgs

    def _run(self, query: AnyStr) -> AnyStr:
        news_sites = {
        "ABC News": f"https://abcnews.go.com/search?searchtext={quote_plus(query)}",
        "CNN": f"https://www.cnn.com/search?q=&{quote_plus(query)}&from=0&size=10&page=1&sort=newest&types=all&section="
            
        }

        print(news_sites)

        results = {}
        # Set headers to mimic a browser
        headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        for site, url in news_sites.items():
            try:
                response = requests.get(url, headers=headers)
                print(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = []

                print(response.content)

                if site == "ABC News":
                    for article in soup.select('h2 a.AnchorLink')[:3]:
                        anchor_tag = soup.find('a', class_='AnchorLink')
                        headline = article.text.strip()
                        link = article['href']
                        if link == "/":
                            continue
                        content = get_article_content(link, site)
                        articles.append({"headline": headline, "link": link, "content": content})

                elif site == "CNN":
                    for article in soup.select('span.container__headline-text')[:3]:
                        headline = article.text.strip()
                        link = article.find_parent('a')['href']
                        content = get_article_content(link, site)
                        articles.append({"headline": headline, "link": link, "content": content})

                results[site] = articles

            except Exception as e:
                print(f"Error scraping {site}: {str(e)}")

        return results
        
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    

def get_article_content(url, site):
    try:
        response = requests.get(url)
        print(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        
        if site == "ABC News":
            paragraphs = soup.select('p.EkqkG')
        elif site == "CNN":
            paragraphs = soup.select('p.paragraph')
        
        content = ' '.join([p.text.strip() for p in paragraphs])
        return content
    except Exception as e:
        print(f"Error getting content from {url}: {str(e)}")
        return ""
    
if __name__ == "__main__":
    # ans = ScrapeHeadlines()._run()
    # print("output")
    # print(ans)

    ans = SearchNews()._run("Florida")
    print("output")
    print(ans)

