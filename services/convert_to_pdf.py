#!/usr/bin/env python3
"""
Convert Markdown to beautifully formatted PDF
This script creates a styled HTML first, then instructions for PDF conversion
"""

import re

# Read the markdown file
with open('Week1_Architecture_Assessment_Report.md', 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Simple markdown to HTML conversion
html_content = markdown_content

# Convert headers
html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)

# Convert bold and italic
html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)

# Convert code blocks
html_content = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html_content, flags=re.DOTALL)
html_content = re.sub(r'`([^`]+)`', r'<code>\1</code>', html_content)

# Convert lists
html_content = re.sub(r'^\- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
html_content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)

# Convert horizontal rules
html_content = re.sub(r'^---$', r'<hr>', html_content, flags=re.MULTILINE)

# Convert paragraphs
lines = html_content.split('\n')
