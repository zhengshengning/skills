---
name: markdown-formatter
description: Formats and beautifies Markdown content without altering the text or meaning. Use this skill when the user provides Markdown text or a file and asks to improve its formatting.
license: Complete terms in LICENSE.txt
---

# Markdown Formatter

This skill helps you beautify Markdown content by applying consistent formatting rules, ensuring readability and professional appearance, without changing the underlying text or meaning.

## Workflow

To format Markdown content:

1.  **Receive Content**: The user provides Markdown text or points to a Markdown file.
2.  **Format**: Apply the formatting rules described below.
3.  **Output**: Return the formatted Markdown content.

## Formatting Rules

Apply the following rules to the content:

*   **Headings**: Ensure there is a blank line before and after each heading (except at the very top of the file).
*   **Lists**:
    *   Ensure consistent indentation (2 or 4 spaces) for nested lists.
    *   Add a blank line before the start of a list.
    *   Ensure there is a space after the list marker (e.g., `- item`, `1. item`).
*   **Code Blocks**:
    *   Ensure code blocks are fenced with triple backticks (```).
    *   Specify the language if it can be inferred from context, otherwise leave it blank or use `text`.
    *   Add a blank line before and after code blocks.
*   **Blockquotes**: Add a space after the `>` character.
*   **Links and Images**: Ensure correct syntax `[text](url)` and `![alt](url)`.
*   **Spacing**:
    *   Remove trailing whitespace from the end of lines.
    *   Ensure there is a single newline at the end of the file.
    *   Limit consecutive blank lines to one.
*   **Tables**: Align table columns for readability if possible.

## Constraints

*   **DO NOT** change the wording, spelling, or grammar of the text.
*   **DO NOT** translate the content.
*   **DO NOT** add or remove content (except for whitespace adjustments for formatting).

## Example

**User Input**:
```markdown
#Title
This is a paragraph.
- item 1
-item 2
```

**Formatted Output**:
```markdown
# Title

This is a paragraph.

- item 1
- item 2
```
