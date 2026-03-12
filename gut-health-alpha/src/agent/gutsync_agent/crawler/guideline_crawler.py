import requests
from bs4 import BeautifulSoup

class GuidelineCrawler:
    def fetch_guidelines(self, url: str) -> str:
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                return soup.get_text()[:1000] # Cap output
        except Exception:
            return ""
        return ""
