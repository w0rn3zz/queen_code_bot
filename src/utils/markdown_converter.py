import re
from uuid import uuid4


def markdown_to_html(text: str) -> str:
    code_blocks = {}
    inline_codes = {}
    links = {}
    
    def save_code_block(match):
        lang = match.group(1).strip() if match.group(1) else ''
        code = match.group(2).strip('\n')
        code = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        html = f'<pre><code class="language-{lang}">{code}</code></pre>' if lang else f'<pre>{code}</pre>'
        placeholder = f'CODEBLOCK{uuid4().hex}'
        code_blocks[placeholder] = html
        return placeholder
    
    text = re.sub(r'```(\w*)\s*\n(.*?)\n```', save_code_block, text, flags=re.DOTALL)
    
    def save_inline_code(match):
        code = match.group(1).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        placeholder = f'INLINECODE{uuid4().hex}'
        inline_codes[placeholder] = f'<code>{code}</code>'
        return placeholder
    
    text = re.sub(r'`([^`\n]+?)`', save_inline_code, text)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    def save_link(match):
        link_text = match.group(1)
        url = match.group(2).replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
        placeholder = f'LINK{uuid4().hex}'
        links[placeholder] = f'<a href="{url}">{link_text}</a>'
        return placeholder
    
    text = re.sub(r'\[(.+?)\]\((.+?)\)', save_link, text)
    text = re.sub(r'^[-*_]{3,}\s*$', '━━━━━━━━━━━━━━━━', text, flags=re.MULTILINE)
    text = re.sub(r'^#{1,6}\s+(.+?)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    text = re.sub(r'(?<!\w)\*(?!\*)([^\*\n]+?)\*(?!\*)(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'(?<!\w)_(?!_)([^_\n]+?)_(?!_)(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
    text = re.sub(r'^[-*+]\s+(.+?)$', r'• \1', text, flags=re.MULTILINE)
    
    lines = text.split('\n')
    result_lines = []
    in_blockquote = False
    blockquote_lines = []
    
    for line in lines:
        if line.startswith('&gt; '):
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            blockquote_lines.append(line[5:])
        else:
            if in_blockquote:
                result_lines.append('<blockquote>' + '\n'.join(blockquote_lines) + '</blockquote>')
                in_blockquote = False
                blockquote_lines = []
            result_lines.append(line)
    
    if in_blockquote:
        result_lines.append('<blockquote>' + '\n'.join(blockquote_lines) + '</blockquote>')
    
    text = '\n'.join(result_lines)
    
    for placeholder, html in links.items():
        text = text.replace(placeholder, html)
    
    for placeholder, html in inline_codes.items():
        text = text.replace(placeholder, html)
    
    for placeholder, html in code_blocks.items():
        text = text.replace(placeholder, html)
    
    return text
