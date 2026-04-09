import requests
import time
import xml.etree.ElementTree as ET
import urllib.parse
import base64
import re
from config import KEYWORDS

class SearchService:
    def __init__(self):
        self.results = []

    def extract_real_url(self, google_news_url):
        """Extract the exact target URL from Google News base64 protobuf string."""
        try:
            # Google news URLs: https://news.google.com/rss/articles/CBMi...
            if "articles/" in google_news_url:
                b64_str = google_news_url.split("articles/")[1].split("?")[0]
                # Fix padding and characters
                b64_str = b64_str.replace("-", "+").replace("_", "/")
                b64_str += "==" 
                decoded = base64.b64decode(b64_str).decode("latin1", errors="ignore")
                urls = re.findall(r'(https?://[^\x00-\x1f\"\']+)', decoded)
                return urls[0] if urls else google_news_url
            return google_news_url
        except Exception:
            return google_news_url

    def perform_search(self):
        """Perform searches using Google News RSS to bypass API blocks."""
        print("Starting market research (Google News RSS)...")
        all_results = {}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        for query in KEYWORDS:
            print(f"Searching for: {query}")
            query_results = []
            try:
                # Use Google News RSS to guarantee results without anti-bot blocks
                encoded_query = urllib.parse.quote(query + " when:14d")
                rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=es-ES&gl=ES&ceid=ES:es"
                
                res = requests.get(rss_url, headers=headers, timeout=10)
                res.raise_for_status()
                
                root = ET.fromstring(res.text)
                
                # Extract Top 4 news items
                for item in root.findall('.//item')[:4]:
                    title = item.find('title').text if item.find('title') is not None else ''
                    link = item.find('link').text if item.find('link') is not None else ''
                    pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
                    
                    real_link = self.extract_real_url(link)
                    
                    data = f"Noticia: {title}\nFecha: {pub_date}\nEnlace: {real_link}"
                    query_results.append({
                        "url": real_link,
                        "content": data
                    })
                    print(f"Found: {title}")
                time.sleep(2) # Pausa amigable
            except Exception as e:
                print(f"Error searching for {query} via RSS: {e}")
            
            all_results[query] = query_results
            
        return all_results

if __name__ == "__main__":
    # Test search
    service = SearchService()
    results = service.perform_search()
    for q, res in results.items():
        print(f"\nQuery: {q}")
        for r in res:
            print(f" - {r}")
