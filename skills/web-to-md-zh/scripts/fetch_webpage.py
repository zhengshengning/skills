import sys
import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import subprocess

def fetch_url(url):
    """
    Fetches content from a URL with a browser-like User-Agent.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # Proxy configuration provided by user for fallback
    proxies = {
        "http": "http://agent.baidu.com:8891",
        "https": "http://agent.baidu.com:8891"
    }
    
    # Method 1: requests (Direct)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Direct requests failed: {e}. Trying requests with proxy...", file=sys.stderr)

    # Method 2: requests (With Proxy)
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Proxy requests failed: {e}. Trying curl...", file=sys.stderr)
        
    # Method 3: curl fallback (Direct)
    try:
        # -L follows redirects, -s silent, -A user-agent
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", headers["User-Agent"], url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception as e:
        print(f"Direct curl failed: {e}", file=sys.stderr)

    # Method 4: curl fallback (With Proxy)
    try:
        print("Trying curl with proxy...", file=sys.stderr)
        env = os.environ.copy()
        env["http_proxy"] = proxies["http"]
        env["https_proxy"] = proxies["https"]
        env["no_proxy"] = "localhost,bj.bcebos.com,su.bcebos.com,pypi.tuna.tsinghua.edu.cn,paddle-ci.gz.bcebos.com,0.0.0.0,baidu-int.com,aliyun.com,127.0.0.1,.baidu.com,.bcebos.com"
        
        result = subprocess.run(
            ["curl", "-s", "-L", "-A", headers["User-Agent"], url],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
        else:
            print(f"Proxy curl failed with return code {result.returncode}", file=sys.stderr)
            return None
    except Exception as e:
        print(f"Proxy curl fallback failed: {e}", file=sys.stderr)
        return None

def html_to_markdown(html_content):
    """
    Converts HTML content to Markdown.
    Uses BeautifulSoup to extract text and basic formatting.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "footer", "iframe", "noscript"]):
        script.extract()
        
    # Attempt to find the main content
    # Priority:
    # 1. <main> tag or role="main"
    # 2. <article> tag
    # 3. Specific classes often used for documentation content
    
    content_root = None
    
    # Try finding main content container
    potential_roots = [
        soup.find('main'),
        soup.find(role='main'),
        soup.find('article'),
        soup.find('div', class_=re.compile(r'markdown|content|article|post|documentation|docs', re.I)),
        soup.find('div', id=re.compile(r'content|main', re.I))
    ]
    
    for root in potential_roots:
        if root:
            content_root = root
            break
            
    # If still not found, use the body
    if not content_root:
        content_root = soup.body
    
    if not content_root:
        return ""

    markdown_lines = []
    
    # Simple recursive function to traverse and convert
    def traverse(element):
        if element.name is None:
            text = element.string
            if text and text.strip():
                return text.strip()
            return ""
            
        text_content = ""
        
        # Handle headings
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            text = element.get_text().strip()
            if text:
                return f"\n{'#' * level} {text}\n\n"
        
        # Handle paragraphs
        elif element.name == 'p':
            for child in element.children:
                text_content += traverse(child) + " "
            return f"{text_content.strip()}\n\n"
            
        # Handle lists
        elif element.name == 'ul':
            for li in element.find_all('li', recursive=False):
                # Recursive traversal for list items to handle nested elements like links/bold
                li_text = traverse(li).strip()
                text_content += f"* {li_text}\n"
            return f"{text_content}\n"
        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li', recursive=False)):
                # Recursive traversal for list items
                li_text = traverse(li).strip()
                text_content += f"{i+1}. {li_text}\n"
            return f"{text_content}\n"
            
        # Handle code blocks
        elif element.name == 'pre':
            code = element.get_text()
            return f"\n```\n{code}\n```\n\n"
        elif element.name == 'code':
            # Inline code usually
            return f"`{element.get_text()}`"
            
        # Handle links
        elif element.name == 'a' and element.get('href'):
            link_text = element.get_text().strip()
            if not link_text:
                link_text = element.get('href')
            return f"[{link_text}]({element['href']}) "
            
        # Handle images
        elif element.name == 'img' and element.get('src'):
            alt = element.get('alt', 'image')
            return f"![{alt}]({element['src']})\n"
            
        # Default traversal for other tags
        else:
            for child in element.children:
                result = traverse(child)
                if result:
                    text_content += result + " "
            
            # Add newlines for block elements
            if element.name in ['div', 'section', 'header']:
                text_content += "\n"
                
            return text_content

    return traverse(content_root)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_webpage.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    html = fetch_url(url)
    
    if html:
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "No Title"
        
        # Generate Front Matter
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("---")
        print(f"title: {title}")
        print(f"date: {current_date}")
        print("categories: Web Translation")
        print("tags: [Translation, Web, Auto-Generated]")
        print("---")
        print()
        print(f"Source: {url}\n")
        
        markdown = html_to_markdown(html)
        print(markdown)

if __name__ == "__main__":
    main()