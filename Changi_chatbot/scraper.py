import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited = set()

def scrape_page(url, domain, max_depth=2, current_depth=0):
    texts = []
    if url in visited or current_depth > max_depth:
        return texts
    visited.add(url)

    try:
        print(f"Scraping: {url}")
        res = requests.get(url, timeout=10)
        if "text/html" not in res.headers.get("Content-Type", ""):
            return texts

        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract meaningful content
        tags = soup.find_all(['p', 'li', 'h1', 'h2', 'h3'])
        cleaned = [tag.get_text(strip=True) for tag in tags if tag.get_text(strip=True)]
        texts.extend(cleaned)

        # Recursively follow internal links
        for link in soup.find_all("a", href=True):
            href = link['href']
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            if domain in parsed.netloc and full_url not in visited:
                texts += scrape_page(full_url, domain, max_depth, current_depth + 1)
                time.sleep(0.5)  # Be polite

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

    return texts

def start_scraping(start_urls, max_depth=2):
    all_texts = []
    for start_url in start_urls:
        domain = urlparse(start_url).netloc
        texts = scrape_page(start_url, domain, max_depth=max_depth)
        all_texts.extend(texts)
    return all_texts

# Usage
if __name__ == "__main__":
    start_urls = [
        "https://www.jewelchangiairport.com/en.html",
        "https://www.changiairport.com/en.html"
    ]
    scraped_data = start_scraping(start_urls, max_depth=2)

    with open("scraped_data.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(scraped_data))
