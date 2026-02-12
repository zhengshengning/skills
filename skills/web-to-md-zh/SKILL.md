---
name: web-to-md-zh
description: Extracts content from a given URL, converts it to Markdown, and translates it into Chinese. Use this skill when the user provides a URL and asks for the content in Chinese Markdown format.
license: Complete terms in LICENSE.txt
---

# Web to Markdown (Chinese)

This skill helps you fetch content from a webpage, convert it to clean Markdown, and then translate it into Chinese.

## Workflow

To process a URL:

1.  **Fetch and Convert**: Run the provided script to get the English (or original language) Markdown content.
    ```bash
    python scripts/fetch_webpage.py <URL>
    ```

2.  **Translate**: Take the output from the script and translate it into Chinese. Ensure the translation is accurate and fluent, preserving the Markdown structure (headings, lists, code blocks, links).

3.  **Output**: Present the final Chinese Markdown document to the user.

## Script Usage

The `scripts/fetch_webpage.py` script requires the `requests` and `beautifulsoup4` libraries.

```bash
# Install dependencies if needed
pip install requests beautifulsoup4
```

Then run:

```bash
python scripts/fetch_webpage.py "https://example.com/article"
```

The script outputs the raw Markdown to stdout. Capture this output to proceed with translation.

## Translation Guidelines

*   **Headings**: Translate headings but keep the `#` level.
*   **Links**: Translate the link text `[text](url)`, but keep the URL `(url)` unchanged.
*   **Code Blocks**: Do NOT translate code content, but translate comments if helpful.
*   **Images**: Translate alt text if present `![alt text](url)`.
*   **Terminology**: Keep technical terms, proper nouns, and specific product names in English. Do NOT translate them unless there is a widely accepted Chinese equivalent, and even then, consider keeping the English term in parentheses for clarity (e.g., "Agent (智能体)").
*   **Tone**: Use a professional and clear tone suitable for technical or general documentation.

## Example

**User**: "Please get the content of https://example.com/guide and give me a Chinese version."

**Claude**:
1.  Executes `python scripts/fetch_webpage.py https://example.com/guide`.
2.  Receives Markdown output.
3.  Translates the Markdown to Chinese.
4.  Returns the Chinese Markdown.