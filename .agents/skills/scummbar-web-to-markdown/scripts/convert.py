#!/usr/bin/env python3
"""
Convert a Web Page URL to a Markdown File using BeautifulSoup 4 & html2text.

Features:
- Standardized source URL header at the top of every generated markdown file: > Source: [URL](URL).
- Auto-Update mode (--update / -u <FILE.md>): Reads the source URL header from an existing markdown file and re-downloads/overwrites it.
- Overwrite protection: Requires --force (-f) or --update (-u) to overwrite existing files.
- Relative URL resolution (a href & img src converted to absolute URLs).
- Clean DOM decomposition (script, style, nav, footer, iframe, etc.).
- External image references preserved without local downloads.
"""

import os
import re
import sys
import urllib.parse
import urllib.request

import html2text
from bs4 import BeautifulSoup


def extract_source_url_from_file(file_path: str) -> str:
    """Read the top header of a markdown file and extract the source URL."""
    if not os.path.exists(file_path):
        print(f"❌ ERROR: File '{file_path}' does not exist.")
        sys.exit(1)

    with open(file_path, encoding="utf-8") as f:
        # Read the first 25 lines
        lines = [f.readline() for _ in range(25)]

    content = "".join(lines)

    # Match standardized header patterns:
    # > Source: [URL](URL)
    # > **Source Page**: [URL](URL)
    match = re.search(r'>\s*(?:\*\*Source Page\*\*|Source):\s*\[([^\]]+)\]\((https?://[^\)]+)\)', content)
    if match:
        return match.group(2)

    # Fallback: search for any standalone HTTP/HTTPS URL in the header lines
    match_fallback = re.search(r'https?://[^\s\)\>\]]+', content)
    if match_fallback:
        url = match_fallback.group(0).rstrip(">.]")
        return url

    return None

def fetch_and_convert(url: str, output_folder: str, filename: str = None, force: bool = False) -> str:
    # Ensure URL has protocol
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    # Determine expected output filename early to check existence
    if not filename:
        parsed = urllib.parse.urlparse(url)
        slug = parsed.path.strip("/").replace("/", "_").replace(".", "_")
        if not slug:
            slug = parsed.netloc.replace(".", "_")
        filename = f"{slug}.md"
    if not filename.endswith(".md"):
        filename += ".md"

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, filename)

    # Check file existence
    if os.path.exists(file_path) and not force:
        print(f"⚠️ FILE_EXISTS: File already exists at '{file_path}'. Ask user for confirmation or specify --force / --update to overwrite.")
        sys.exit(2)

    print(f"🌐 Fetching URL: {url}...")
    try:
        try:
            import httpx
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            res = httpx.get(url, follow_redirects=True, headers=headers, timeout=30.0)
            res.raise_for_status()
            raw_bytes = res.content
            charset = res.encoding
        except ImportError:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/120.0.0.0 Safari/537.36"
                    )
                }
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                raw_bytes = response.read()
                charset = response.headers.get_content_charset()
    except Exception as e:
        print(f"❌ Error fetching URL: {e}")
        sys.exit(1)

    # Parse with BeautifulSoup passing detected charset to from_encoding
    soup = BeautifulSoup(raw_bytes, "html.parser", from_encoding=charset)

    # Extract title cleanly
    if soup.title and soup.title.string:
        page_title = soup.title.get_text(strip=True)
    elif soup.h1:
        page_title = soup.h1.get_text(strip=True)
    else:
        page_title = "Web Page"

    # Convert all relative image and anchor links to absolute URLs
    for tag in soup.find_all(["a", "img", "source"]):
        if tag.name == "a" and tag.has_attr("href"):
            tag["href"] = urllib.parse.urljoin(url, tag["href"])
        elif tag.name in ("img", "source") and tag.has_attr("src"):
            tag["src"] = urllib.parse.urljoin(url, tag["src"])

    # Decompose non-content and noisy elements
    for noise in soup(["script", "style", "nav", "footer", "iframe", "noscript", "svg", "form", "aside"]):
        noise.decompose()

    # Configure html2text based on official documentation
    h = html2text.HTML2Text()
    h.unicode_snob = True  # Use UTF-8 unicode throughout instead of ASCII
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.ignore_tables = False
    h.body_width = 0  # Do not wrap lines
    h.protect_links = True
    h.default_image_alt = "Image"  # Fallback alt text for images missing alt attribute

    # Convert the cleaned soup to Markdown
    markdown_body = h.handle(str(soup))

    # Clean consecutive empty lines
    cleaned_lines = []
    prev_empty = False
    for line in markdown_body.splitlines():
        is_empty = not line.strip()
        if is_empty and prev_empty:
            continue
        cleaned_lines.append(line)
        prev_empty = is_empty

    # Standardized source URL header
    final_markdown = f"# {page_title}\n\n> Source: [{url}]({url})\n\n" + "\n".join(cleaned_lines)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_markdown)

    print(f"✅ Markdown saved successfully to: {file_path}")
    return file_path

def update_file(file_path: str) -> str:
    """Extract source URL from an existing markdown file and update it."""
    print(f"🔍 Searching for source URL in '{file_path}'...")
    url = extract_source_url_from_file(file_path)
    if not url:
        print(f"🛑 NO_SOURCE_URL: Could not find source URL in header of '{file_path}'. Cannot auto-update.")
        print("Please verify if the file has a header like: '> Source: [URL](URL)' or supply the URL manually.")
        sys.exit(3)

    folder = os.path.dirname(file_path) or "."
    filename = os.path.basename(file_path)
    print(f"🔄 Found source URL: {url}. Re-downloading and updating '{file_path}'...")
    return fetch_and_convert(url, folder, filename, force=True)

if __name__ == "__main__":
    args = sys.argv[1:]

    # Check for update mode
    if "--update" in args or "-u" in args:
        target_file = None
        if "--update" in args:
            idx = args.index("--update")
            if idx + 1 < len(args):
                target_file = args[idx + 1]
        elif "-u" in args:
            idx = args.index("-u")
            if idx + 1 < len(args):
                target_file = args[idx + 1]

        if not target_file:
            print("Usage for update mode: convert.py --update <PATH_TO_MARKDOWN.md>")
            sys.exit(1)

        update_file(target_file)
        sys.exit(0)

    # Regular conversion mode
    force_flag = False
    if "--force" in args:
        force_flag = True
        args.remove("--force")
    if "-f" in args:
        force_flag = True
        args.remove("-f")

    if len(args) < 2:
        print("Usage: convert.py <URL> <OUTPUT_FOLDER> [FILENAME] [--force]")
        print("   or: convert.py --update <FILE.md>")
        sys.exit(1)

    url_arg = args[0]
    folder_arg = args[1]
    filename_arg = args[2] if len(args) > 2 else None

    fetch_and_convert(url_arg, folder_arg, filename_arg, force=force_flag)
