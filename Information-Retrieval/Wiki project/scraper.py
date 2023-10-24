import requests
from bs4 import BeautifulSoup
from config import BASE_URL, SLEEP_TIME
import time

VISITED_LINKS = set()
articles = []

def fetch_robots_txt():
    url = f"{BASE_URL}/robots.txt"
    response = requests.get(url)
    return response.text

def parse_robots_txt():
    rules = {"Allow": [], "Disallow": []}
    try:
        robots_txt = fetch_robots_txt().split("\n")
        user_agent = None
        for line in robots_txt:
            if line.startswith("User-agent:"):
                user_agent = line.split(":")[1].strip()
            elif user_agent == "*" or user_agent == "MyBotName":  # Adjust "MyBotName" to the name of your bot (if it has one)
                if line.startswith("Allow:"):
                    rules["Allow"].append(line.split(":")[1].strip())
                elif line.startswith("Disallow:"):
                    rules["Disallow"].append(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error parsing robots.txt: {e}")
    return rules  # Moved this return statement out of the try block.


def can_visit_url(url, rules):
    for rule in rules["Disallow"]:
        if rule in url:
            return False
    for rule in rules["Allow"]:
        if rule in url:
            return True
    return True


def get_links_from_url(url, rules=None):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    links = []
    for link in soup.find_all('a', href=True):
        full_link = BASE_URL + link['href']
        if full_link.startswith(BASE_URL) and link['href'].startswith("/wiki/") and not link['href'].startswith("/wiki/Special:") and can_visit_url(full_link, rules):
            links.append(full_link)
    return list(set(links))

def scrape_content_from_link(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # We assume the main content is in a <div> with class "mw-parser-output"
        content_div = soup.find('div', class_='mw-parser-output')

        if content_div:
            return content_div.get_text()
        else:
            return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def dfs_crawl(url, visited_links, articles, depth=0, rules=None):
    from config import MAX_DEPTH, MAX_ARTICLES

    if depth == MAX_DEPTH or len(articles) >= MAX_ARTICLES:
        return
    
    if url in visited_links or (rules and not can_visit_url(url, rules)):
        return
    
    visited_links.add(url)

    print(f"Visiting {url} at depth {depth}")

    content = scrape_content_from_link(url)
    if content:
        articles.append({
            'link': url,
            'content': content
        })

    for link in get_links_from_url(url, rules):
        dfs_crawl(link, visited_links, articles, depth + 1, rules=rules)
        if len(articles) >= MAX_ARTICLES:
            break
    time.sleep(SLEEP_TIME)

def scrape():
    from config import START_URL
    visited_links = set()
    articles = []
    rules = parse_robots_txt()
    dfs_crawl(START_URL, visited_links, articles, rules=rules)
    return articles


if __name__ == "__main__":
    articles = scrape()
    print(f"Scraped {len(articles)} articles")
    print(articles[0])