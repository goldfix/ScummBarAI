#!/usr/bin/env python3
"""
Kroki Diagram Generator & URL Encoder for Pi-Agent & Scummbar.

Encodes plain text diagram sources (Excalidraw, Mermaid, PlantUML, Graphviz, D2, etc.)
using deflate (zlib level 9) + URL-safe Base64 into Kroki URLs.
Default diagram type: excalidraw
Default format: svg
"""

import argparse
import base64
import json
import sys
import urllib.request
import zlib
from pathlib import Path
from typing import Any


def encode_kroki_payload(source_text: str) -> str:
    """
    Compresses text using zlib deflate (level 9) and encodes with URL-safe base64.
    Matches Kroki GET request payload requirement.
    """
    if not source_text or not source_text.strip():
        raise ValueError("Source text for diagram cannot be empty.")
    
    compressed = zlib.compress(source_text.encode("utf-8"), level=9)
    return base64.urlsafe_b64encode(compressed).decode("ascii")


def generate_kroki_url(
    source_text: str,
    diagram_type: str = "excalidraw",
    output_format: str = "svg",
    base_url: str = "https://kroki.io",
    params: dict[str, str] | None = None,
) -> str:
    """
    Generates a Kroki GET request URL for a given diagram source.
    If diagram_type is omitted or empty, defaults to 'excalidraw'.
    """
    if not diagram_type or not str(diagram_type).strip():
        diagram_type = "excalidraw"
    diagram_type = str(diagram_type).lower().strip()

    if not output_format or not str(output_format).strip():
        output_format = "svg"
    output_format = str(output_format).lower().strip()

    # If excalidraw is given as simple dict/text without full JSON wrapper, try building basic valid JSON
    if diagram_type == "excalidraw" and not source_text.strip().startswith("{"):
        source_text = build_simple_excalidraw_json(source_text)

    payload = encode_kroki_payload(source_text)
    url = f"{base_url.rstrip('/')}/{diagram_type}/{output_format}/{payload}"

    if params:
        query_str = "&".join(f"{k}={v}" for k, v in params.items())
        url = f"{url}?{query_str}"

    return url


def build_simple_excalidraw_json(label_text: str) -> str:
    """
    Helper to construct a valid Excalidraw JSON structure from plain text labels/nodes.
    """
    lines = [line.strip() for line in label_text.strip().splitlines() if line.strip()]
    elements: list[dict[str, Any]] = []
    
    y_offset = 50
    for idx, line in enumerate(lines):
        elements.append({
            "id": f"elem_{idx}",
            "type": "rectangle",
            "x": 100,
            "y": y_offset,
            "width": 240,
            "height": 70,
            "strokeColor": "#1e1e1e",
            "backgroundColor": "#e0f2fe" if idx == 0 else "#fff3bf",
            "fillStyle": "hachure",
            "strokeWidth": 2,
            "roughness": 1,
            "opacity": 100,
            "label": {"text": line}
        })
        y_offset += 100

    excalidraw_doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "scummbar-kroki-skill",
        "elements": elements
    }
    return json.dumps(excalidraw_doc, ensure_ascii=False)


def download_kroki_diagram(
    url: str,
    output_path: Path,
    user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Scummbar/1.0"
) -> bool:
    """
    Downloads the diagram from Kroki URL and saves it to output_path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with open(output_path, "wb") as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"❌ Error downloading diagram from Kroki: {e}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate Kroki diagram URLs and images from text source."
    )
    parser.add_argument(
        "source",
        nargs="?",
        default=None,
        help="Diagram text source. If empty or '-', reads from stdin or --file."
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        default=None,
        help="Path to file containing diagram source text."
    )
    parser.add_argument(
        "--type", "-t",
        default="excalidraw",
        help="Diagram type (default: excalidraw). Options: excalidraw, mermaid, plantuml, graphviz, d2, bpmn, etc."
    )
    parser.add_argument(
        "--format", "-fmt",
        default="svg",
        help="Output image format: svg (default), png, jpeg, pdf."
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=None,
        help="Output file path to save downloaded image (optional)."
    )
    parser.add_argument(
        "--title",
        default="Diagram",
        help="Title for Markdown/HTML output tag."
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Output result as Markdown image tag ![Title](URL)."
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Output result as HTML img tag."
    )

    args = parser.parse_args()

    # Determine diagram source
    source_text = ""
    if args.file and args.file.exists():
        source_text = args.file.read_text(encoding="utf-8")
    elif args.source and args.source != "-":
        source_text = args.source
    else:
        source_text = sys.stdin.read()

    if not source_text or not source_text.strip():
        print("❌ Error: No diagram source text provided.", file=sys.stderr)
        sys.exit(1)

    url = generate_kroki_url(
        source_text=source_text,
        diagram_type=args.type,
        output_format=args.format,
    )

    if args.output:
        success = download_kroki_diagram(url, args.output)
        if success:
            print(f"✅ Saved diagram to {args.output}")

    if args.markdown:
        print(f"![{args.title}]({url})")
    elif args.html:
        print(f'<img src="{url}" alt="{args.title}" />')
    else:
        print(url)


if __name__ == "__main__":
    main()
