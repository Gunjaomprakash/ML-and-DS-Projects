import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import json
import sys

# Set of visited URLs to avoid revisiting
visited = set()
# List to store crawled datas s
crawled_data = []

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_limit_reached(soup):
    title = soup.find('title')
    if title and "Your activity has been limited" in title.get_text():
        
        return True
    return False

def crawl(url, depth): 
    if depth == 0:
        return
    if url in visited:
        return
    visited.add(url)
    print(f"Crawling: {url} at depth {depth}")
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if we hit the limit
        if is_limit_reached(soup):
            print("Crawling limit reached! Saving data and exiting...")
            with open("crawled_data.json", "w", encoding="utf-8") as jsonfile:
                json.dump(crawled_data, jsonfile, ensure_ascii=False, indent=4)
            sys.exit(0)
            
        # Extract the title of the page
        title = soup.find('title').get_text() if soup.find('title') else 'No Title'
        content = soup.get_text()
        
        print(f"Title: {title}")
        # Append to the list
        crawled_data.append({'URL': url, 'Title': title, 'Content': content})
        # Find all links on the page
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            next_url = urljoin(url, href)
            if is_valid(next_url):
                crawl(next_url, depth - 1)
                time.sleep(1)
    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {url}: {e}")

if __name__ == "__main__":
    start_url = "https://www.datacentermap.com/usa/california/santa-clara/"
    crawl(start_url, depth=2)
    # Save to JSON file in case we didn't hit the limit
    with open("crawled_data.json", "w", encoding="utf-8") as jsonfile:
        json.dump(crawled_data, jsonfile, ensure_ascii=False, indent=4)
