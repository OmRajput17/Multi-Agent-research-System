from tavily import TavilyClient
import arxiv
from ddgs import DDGS
import requests
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class HelperTools:
    def __init__(self):
        self.tavily_client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )
        self.arxiv_client = arxiv.Client()
        self.ddgs = DDGS()

    def tavily_search(self, query: str, max_results: int = 5) -> List[dict]:
        """Search the web using Tavily API Key"""
        try:
            response = self.tavily_client.search(
                query=query,
                max_results=max_results
            )

            results = []
            for article in response['results']:
                results.append({
                    "title": article['title'],
                    "content": article['content'],
                    "url": article['url'],
                    "source": "tavily"
                })
            return results
        except Exception as e:
            print(f"Error searching Tavily: {e}")
            return []

    def arxiv_search(self, query: str, max_results: int = 5) -> List[dict]:
        """Search Arxiv for Research Papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = []
            for result in self.arxiv_client.results(search):
                results.append({
                    "title": result.title,
                    "content": result.summary,
                    "url": result.entry_id,
                    "source": "arxiv"
                })
            return results
        except Exception as e:
            print(f"Error searching Arxiv: {e}")
            return []

    def ddgs_search(self, query: str, max_results: int = 5) -> List[dict]:
        """Search the web using DuckDuckGo Search"""
        try:
            results = []
            for result in self.ddgs.text(
                query,
                max_results=max_results
            ):
                results.append({
                    "title": result['title'],
                    "content": result['body'],
                    "url": result['href'],
                    "source": "duckduckgo"
                })
            return results
        except Exception as e:
            print(f"Error searching DuckDuckGo: {e}")
            return []

    def semantic_scholar_search(self, query: str, max_results: int = 5) -> List[dict]:
        """Search Semantic Scholar for Academic Papers"""
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": max_results,
                "fields": "title,abstract,year,url"
            }
            headers = {
                "Accept": "application/json"
            }
            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            if "data" not in data:
                print(f"No results found for query: {query}")
                return []

            results = []
            for paper in data['data']:
                results.append({
                    "title": paper.get('title', 'N/A'),
                    "content": paper.get('abstract', 'N/A'),
                    "url": paper.get('url', 'N/A'),
                    "source": "semantic_scholar"
                })
            return results
        except Exception as e:
            print(f"Error searching Semantic Scholar: {e}")
            return []