#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
import re
from datetime import datetime
import os
import hashlib
from urllib.parse import urlparse, urljoin

def sanitize_filename(title):
    """Convert title to a URL-safe filename"""
    # Convert to lowercase and replace spaces with dashes
    filename = title.lower()
    # Remove special characters
    filename = re.sub(r'[^a-z0-9\s-]', '', filename)
    # Replace spaces with dashes
    filename = re.sub(r'\s+', '-', filename)
    # Remove multiple consecutive dashes
    filename = re.sub(r'-+', '-', filename)
    # Remove leading/trailing dashes
    filename = filename.strip('-')
    return filename

def download_image(img_url, post_date, base_path='images/posts'):
    """Download an image and return the local path"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(img_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Create directory based on date (YYYY-MM format)
        date_obj = datetime.fromisoformat(post_date) if isinstance(post_date, str) else post_date
        year_month = date_obj.strftime('%Y-%m')
        img_dir = os.path.join(base_path, year_month)
        os.makedirs(img_dir, exist_ok=True)

        # Generate filename from URL
        parsed_url = urlparse(img_url)
        img_filename = os.path.basename(parsed_url.path)

        # If no extension, try to get from content-type
        if '.' not in img_filename:
            content_type = response.headers.get('content-type', '')
            if 'jpeg' in content_type or 'jpg' in content_type:
                img_filename += '.jpg'
            elif 'png' in content_type:
                img_filename += '.png'
            elif 'gif' in content_type:
                img_filename += '.gif'

        # If still no good filename, use hash
        if not img_filename or img_filename == '':
            img_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            img_filename = f'image_{img_hash}.jpg'

        img_path = os.path.join(img_dir, img_filename)

        # Save the image
        with open(img_path, 'wb') as f:
            f.write(response.content)

        # Return the relative path for markdown
        return f'/images/posts/{year_month}/{img_filename}'

    except Exception as e:
        print(f"  Error downloading image {img_url}: {e}")
        return img_url  # Return original URL if download fails

def html_to_markdown(element, base_url, post_date, img_map):
    """Convert HTML element to markdown"""
    if element.name == 'p':
        return convert_inline_elements(element, base_url, post_date, img_map) + '\n\n'
    elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level = int(element.name[1])
        return '#' * level + ' ' + element.get_text().strip() + '\n\n'
    elif element.name == 'ul':
        result = ''
        for li in element.find_all('li', recursive=False):
            result += '- ' + convert_inline_elements(li, base_url, post_date, img_map).strip() + '\n'
        return result + '\n'
    elif element.name == 'ol':
        result = ''
        for i, li in enumerate(element.find_all('li', recursive=False), 1):
            result += f'{i}. ' + convert_inline_elements(li, base_url, post_date, img_map).strip() + '\n'
        return result + '\n'
    elif element.name == 'pre':
        code = element.get_text()
        return f'```\n{code}\n```\n\n'
    elif element.name == 'blockquote':
        lines = element.get_text().strip().split('\n')
        return '\n'.join(['> ' + line for line in lines]) + '\n\n'
    elif element.name == 'img':
        src = element.get('src', '')
        alt = element.get('alt', '')
        if src:
            full_url = urljoin(base_url, src)
            # Download image and get local path
            if full_url not in img_map:
                local_path = download_image(full_url, post_date)
                img_map[full_url] = local_path
            else:
                local_path = img_map[full_url]
            return f'![{alt}]({local_path}){{: .align-center}}\n\n'
    elif element.name == 'a':
        href = element.get('href', '')
        text = element.get_text().strip()
        return f'[{text}]({href})'
    else:
        return element.get_text() + '\n\n'

def convert_inline_elements(element, base_url, post_date, img_map):
    """Convert inline HTML elements to markdown"""
    result = ''
    for child in element.children:
        if isinstance(child, str):
            result += child
        elif child.name == 'a':
            href = child.get('href', '')
            text = child.get_text().strip()
            result += f'[{text}]({href})'
        elif child.name == 'strong' or child.name == 'b':
            result += '**' + child.get_text() + '**'
        elif child.name == 'em' or child.name == 'i':
            result += '*' + child.get_text() + '*'
        elif child.name == 'code':
            result += '`' + child.get_text() + '`'
        elif child.name == 'img':
            src = child.get('src', '')
            alt = child.get('alt', '')
            if src:
                full_url = urljoin(base_url, src)
                if full_url not in img_map:
                    local_path = download_image(full_url, post_date)
                    img_map[full_url] = local_path
                else:
                    local_path = img_map[full_url]
                result += f'![{alt}]({local_path})'
        else:
            result += child.get_text()
    return result

def download_blog_post(url):
    """Download and parse a blog post"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract title
        title_tag = soup.find('h1') or soup.find('title')
        title = title_tag.get_text().strip() if title_tag else 'Untitled'

        # Clean up title (remove site name if present)
        title = re.sub(r'\s*\|\s*.*$', '', title)
        title = title.strip()

        # Extract date - try multiple selectors
        date = None
        date_patterns = [
            soup.find('time'),
            soup.find('meta', {'property': 'article:published_time'}),
            soup.find('span', class_=re.compile('date|time', re.I)),
        ]

        for pattern in date_patterns:
            if pattern:
                if pattern.name == 'meta':
                    date_str = pattern.get('content', '')
                elif pattern.name == 'time':
                    date_str = pattern.get('datetime', '') or pattern.get_text()
                else:
                    date_str = pattern.get_text()

                if date_str:
                    try:
                        # Try to parse various date formats
                        if 'T' in date_str:
                            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        else:
                            date = datetime.strptime(date_str, '%B %d, %Y')
                        break
                    except:
                        continue

        # If no date found, use today
        if not date:
            date = datetime.now()

        # Extract main content
        content_selectors = [
            soup.find('article'),
            soup.find('div', class_=re.compile('content|post-content|entry-content|article-body', re.I)),
            soup.find('main'),
        ]

        content_elem = None
        for selector in content_selectors:
            if selector:
                content_elem = selector
                break

        if not content_elem:
            print(f"  Warning: Could not find main content for {url}")
            return None

        # Convert content to markdown
        img_map = {}  # Track downloaded images
        markdown_content = ''

        # Process content elements
        for elem in content_elem.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'pre', 'blockquote', 'img']):
            # Skip if element is inside another processed element
            if elem.find_parent(['p', 'li', 'blockquote']):
                continue
            markdown_content += html_to_markdown(elem, url, date, img_map)

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

        # Combine front matter and content
        full_content = front_matter + markdown_content

        return {
            'filename': filename,
            'content': full_content,
            'title': title,
            'date': date_str,
            'url': url
        }

    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Load blog links
    with open('blog_links.json', 'r') as f:
        blog_links = json.load(f)

    print(f"Found {len(blog_links)} blog posts to download\n")

    successful = []
    failed = []

    for i, url in enumerate(blog_links, 1):
        print(f"\n[{i}/{len(blog_links)}] Processing: {url}")

        post_data = download_blog_post(url)

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

        # Be polite - wait between requests
        time.sleep(3)

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
    main()
