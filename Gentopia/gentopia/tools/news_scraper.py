from typing import AnyStr
from gentopia.tools.basetool import *
from gentopia.tools.utils.document_loaders.text_loader import TextLoader
from gentopia.tools.utils.vector_store import VectorstoreIndexCreator
import requests
from pypdf import PdfReader
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from selenium import webdriver
import time
from playwright.sync_api import sync_playwright

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


    def _run(self, query):
        # Replace spaces with '+' for the query string
        query = query.replace(' ', '+')
        url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US:en"


        num_articles = 1
        response = requests.get(url)
    
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
        
            # Find articles
            articles = soup.find_all('article', limit=num_articles)
            article_content = []
            for article in articles:
                # Extract the title and link
                title = article.find('h3').text if article.find('h3') else "No title found"
                link = article.find('a')['href'] if article.find('a') else "No link found"
                link = f"https://news.google.com{link[1:]}"  # Append the base URL
                article_content.append(get_article_content(link))
            return '\n\n'.join(article_content)
        else:
            return "Failed to retrieve news articles"

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError




def get_article_content(url):
    try:
        # Start Playwright and open a browser in headless mode
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Set a user-agent to mimic a real browser
            page.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
            
            # Navigate to the URL
            page.goto(url)
            
            # Wait for content to load; you can adjust the time or use other wait conditions if needed
            page.wait_for_timeout(5000)  # Wait for 5 seconds

            # Get the page content after JavaScript has loaded
            html = page.content()
            
            # Parse the HTML with BeautifulSoup
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            paragraphs = soup.find_all('p')
            content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
            
            print("Extracted content:")
            print(content)
            
            # Close the browser
            browser.close()
            
            return content
    except Exception as e:
        print(f"Error getting content: {e}")
        return None
    
if __name__ == "__main__":
    # ans = ScrapeHeadlines()._run()
    # print("output")
    # print(ans)

    ans = SearchNews()._run("james")
    print("output")
    print(ans)
