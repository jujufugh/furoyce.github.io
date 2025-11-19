#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import os
import hashlib
from urllib.parse import urljoin, urlparse

def sanitize_filename(title):
    """Convert title to a URL-safe filename"""
    filename = title.lower()
    filename = re.sub(r'[^a-z0-9\s-]', '', filename)
    filename = re.sub(r'\s+', '-', filename)
    filename = re.sub(r'-+', '-', filename)
    filename = filename.strip('-')
    return filename

async def download_image(page, img_url, post_date, base_path='images/posts'):
    """Download an image using playwright"""
    try:
        # Create directory based on date
        date_obj = datetime.fromisoformat(post_date) if isinstance(post_date, str) else post_date
        year_month = date_obj.strftime('%Y-%m')
        img_dir = os.path.join(base_path, year_month)
        os.makedirs(img_dir, exist_ok=True)

        # Generate filename from URL
        parsed_url = urlparse(img_url)
        img_filename = os.path.basename(parsed_url.path)

        if not img_filename or '.' not in img_filename:
            img_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            img_filename = f'image_{img_hash}.jpg'

        img_path = os.path.join(img_dir, img_filename)

        # Download using playwright
        async with page.context.expect_page() as _:
            response = await page.request.get(img_url)
            if response.ok:
                body = await response.body()
                with open(img_path, 'wb') as f:
                    f.write(body)
                return f'/images/posts/{year_month}/{img_filename}'

        return img_url

    except Exception as e:
        print(f"  Error downloading image {img_url}: {e}")
        return img_url

async def download_blog_post(page, url):
    """Download and parse a blog post using Playwright"""
    try:
        print(f"  Navigating to: {url}")

        # Go to page and wait for content to load
        await page.goto(url, wait_until='networkidle', timeout=60000)
        await page.wait_for_timeout(3000)  # Wait for dynamic content

        # Get the page content
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # Extract title
        title_tag = soup.find('h1', class_=re.compile('title|heading', re.I)) or soup.find('h1') or soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'Untitled'

        # Clean up title
        title = re.sub(r'\s*\|\s*.*$', '', title)
        title = title.strip()

        print(f"  Title: {title}")

        # Extract date
        date = None
        date_selectors = [
            'time',
            'meta[property="article:published_time"]',
            'span[class*="date"]',
            'div[class*="date"]',
        ]

        for selector in date_selectors:
            elem = await page.query_selector(selector)
            if elem:
                date_str = await elem.get_attribute('datetime') or await elem.get_attribute('content') or await elem.inner_text()
                if date_str:
                    try:
                        if 'T' in date_str:
                            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            date = datetime.strptime(date_str, '%B %d, %Y')
                        break
                    except:
                        continue

        if not date:
            date = datetime.now()

        print(f"  Date: {date.strftime('%Y-%m-%d')}")

        # Extract main content
        content_selectors = [
            'article',
            'div[class*="content"]',
            'div[class*="post-content"]',
            'div[class*="entry-content"]',
            'main',
        ]

        content_elem = None
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                break

        if not content_elem:
            print(f"  Warning: Could not find main content")
            return None

        # Convert to markdown (simplified)
        markdown_content = ''

        # Process headings, paragraphs, lists, code blocks
        for elem in content_elem.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'blockquote']):
            # Skip nested elements
            if elem.find_parent(['p', 'li', 'blockquote']):
                continue

            if elem.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(elem.name[1])
                text = elem.get_text().strip()
                # Skip if it's the title
                if text == title:
                    continue
                markdown_content += '#' * level + ' ' + text + '\n\n'

            elif elem.name == 'p':
                text = elem.get_text().strip()
                if text:
                    markdown_content += text + '\n\n'

            elif elem.name == 'ul':
                for li in elem.find_all('li', recursive=False):
                    markdown_content += '- ' + li.get_text().strip() + '\n'
                markdown_content += '\n'

            elif elem.name == 'ol':
                for i, li in enumerate(elem.find_all('li', recursive=False), 1):
                    markdown_content += f'{i}. ' + li.get_text().strip() + '\n'
                markdown_content += '\n'

            elif elem.name == 'pre':
                code = elem.get_text()
                markdown_content += f'```\n{code}\n```\n\n'

            elif elem.name == 'blockquote':
                lines = elem.get_text().strip().split('\n')
                markdown_content += '\n'.join(['> ' + line for line in lines]) + '\n\n'

        # Process images
        for img in content_elem.find_all('img'):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                full_url = urljoin(url, src)
                local_path = await download_image(page, full_url, date)
                markdown_content += f'![{alt}]({local_path}){{: .align-center}}\n\n'

        # Clean up markdown
        markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)

        # Create filename
        date_str = date.strftime('%Y-%m-%d')
        title_slug = sanitize_filename(title)
        filename = f"{date_str}-{title_slug}.md"

        # Create front matter
        front_matter = f"""---
title: "{title}"
date: {date.strftime('%Y-%m-%d')}
last_modified_at: {datetime.now().strftime('%Y-%m-%dT%H:%M:%S-05:00')}
categories:
  - Blog
tags:
  - OCI Observability and Management
---

"""

        full_content = front_matter + markdown_content

        return {
            'filename': filename,
            'content': full_content,
            'title': title,
            'date': date_str,
            'url': url
        }

    except Exception as e:
        print(f"  Error: {e}")
        import traceback
        traceback.print_exc()
        return None

async def main():
    # Load blog links
    with open('blog_links.json', 'r') as f:
        blog_links = json.load(f)

    print(f"Found {len(blog_links)} blog posts to download\n")

    successful = []
    failed = []

    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ignore_https_errors=True
        )
        page = await context.new_page()

        for i, url in enumerate(blog_links, 1):
            print(f"\n[{i}/{len(blog_links)}] Processing: {url}")

            post_data = await download_blog_post(page, url)

            if post_data:
                # Save to _posts directory
                output_path = os.path.join('_posts', post_data['filename'])
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(post_data['content'])

                print(f"  ✓ Saved to: {output_path}")
                successful.append({
                    'url': url,
                    'filename': post_data['filename'],
                    'title': post_data['title']
                })
            else:
                print(f"  ✗ Failed to process")
                failed.append(url)

            # Wait between requests
            await page.wait_for_timeout(2000)

        await browser.close()

    # Print summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if successful:
        print(f"\nSuccessfully downloaded:")
        for item in successful:
            print(f"  - {item['title']}")
            print(f"    {item['filename']}")

    if failed:
        print(f"\nFailed to download:")
        for url in failed:
            print(f"  - {url}")

if __name__ == '__main__':
    asyncio.run(main())
