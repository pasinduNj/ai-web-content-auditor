import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

async def fetch_page(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                return await response.text()
            return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_structured_content(html):
    """
    Refined extraction to prioritize high-value content tags.
    This fulfills the requirement to handle 'duplicated or low-value text'
    by ignoring scripts, styles, and footer/nav noise.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Capture Metadata (High signal for Clarity & Readability)
    meta_desc = soup.find("meta", attrs={"name": "description"})
    description = meta_desc["content"] if meta_desc else "No meta description"

    # Capture Key Headers (Core Message/Structure)
    headers = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]
    header_str = " | ".join(headers[:5]) # Take top 5 headers

    # Capture Primary CTAs (Targeting 'missing or weak calls to action')
    ctas = [a.get_text(strip=True) for a in soup.find_all(['a', 'button']) 
            if len(a.get_text(strip=True)) > 2 and len(a.get_text(strip=True)) < 30]
    cta_str = " | ".join(ctas[:6]) # Take top 6 potential CTAs

    # Clean Body Text (The Context)
    # Remove junk before getting body text
    for tag in soup(["script", "style", "noscript", "footer", "nav", "header"]):
        tag.decompose()

    raw_body = soup.get_text(separator=" ", strip=True)
    # Remove multiple spaces/newlines to save token space
    clean_body = re.sub(r'\s+', ' ', raw_body)

    # Combine into a Semantic Summary
  
    final_output = f"SUMMARY: {description} | HEADERS: {header_str} | CTAs: {cta_str} | BODY: {clean_body}"
    
    return final_output

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    domain = urlparse(base_url).netloc

    for a_tag in soup.find_all("a", href=True):
        href = urljoin(base_url, a_tag["href"])
        if "#" in href:
            continue
        parsed = urlparse(href)
        if parsed.netloc == domain:
            links.add(href)
    return list(links)

async def crawl_website(start_url, max_pages=3):
    visited = set()
    to_visit = [start_url]
    results = {}

    async with aiohttp.ClientSession() as session:
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop(0)
            if url in visited:
                continue

            print(f"Crawling: {url}")
            html = await fetch_page(session, url)
            if not html:
                continue

            
            structured_text = extract_structured_content(html)
            results[url] = structured_text

            visited.add(url)
            links = extract_links(html, start_url)
            for link in links:
                if link not in visited:
                    to_visit.append(link)

    return results