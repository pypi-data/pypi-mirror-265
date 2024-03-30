import requests
from bs4 import BeautifulSoup
import time

class ImageSearch:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def _output_url_google(self, query: str, page=1):
        return f"https://www.google.com/search?q={query}&sclient=img&tbm=isch&start={page * 100}"

    def _output_url_yandex(self, query: str, page=1):
        return f"https://yandex.com/images/search?text={query}&p={page}"

    def search_images(self, query: str, provider="google", max_pages=5):
        s = requests.Session()
        image_urls = []
        output_url_func = self._output_url_google if provider == "google" else self._output_url_yandex
        for page in range(max_pages):
            req = s.get(output_url_func(query, page), headers=self.headers)
            soup = BeautifulSoup(req.text, "html.parser")
            if provider == "google":
                for img_tag in soup.find_all(name="img"):
                    src = img_tag.get('src')
                    if src and "googlelogo" not in src:  # Check if "googlelogo" is not in the URL
                        image_urls.append(src)
            elif provider == "yandex":
                for img_tag in soup.find_all("img", class_="serp-item__thumb"):
                    src = img_tag.get("src")
                    if src:
                        image_urls.append(src)
            time.sleep(2)  # Add a delay to avoid hitting rate limits
        return image_urls
