#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time

def get_blog_links(url):
    """Fetch blog post links from an Oracle author page"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all blog post links
        blog_links = []

        # Look for article links (common pattern in Oracle blogs)
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Filter for blog post URLs
            if '/post/' in href or 'blogs.oracle.com' in href:
                # Make sure it's a full URL
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = 'https://blogs.oracle.com' + href
                else:
                    continue

                # Avoid duplicates
                if full_url not in blog_links and '/post/' in full_url:
                    blog_links.append(full_url)

        return blog_links

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    urls = [
        'https://blogs.oracle.com/authors/roycefu',
        'https://blogs.oracle.com/authors/royce-fu'
    ]

    all_links = []

    for url in urls:
        print(f"Fetching links from: {url}")
        links = get_blog_links(url)
        all_links.extend(links)
        print(f"Found {len(links)} links")
        time.sleep(2)  # Be polite

    # Remove duplicates
    all_links = list(set(all_links))

    print(f"\nTotal unique blog posts found: {len(all_links)}")

    # Save to file
    with open('blog_links.json', 'w') as f:
        json.dump(all_links, f, indent=2)

    print("Links saved to blog_links.json")

    # Also print them
    for link in sorted(all_links):
        print(link)

if __name__ == '__main__':
    main()
