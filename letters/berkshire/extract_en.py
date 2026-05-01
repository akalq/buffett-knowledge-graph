#!/usr/bin/env python3
"""提取需要翻译的块的英文原文"""

import re

def extract_blocks(html_content):
    blocks = []
    
    block_pattern = re.compile(
        r'<div class="bilingual-block">\s*'
        r'<div class="lang-block lang-en">\s*'
        r'<span class="lang-label">English</span>\s*'
        r'<blockquote>(.*?)</blockquote>\s*'
        r'</div>\s*'
        r'<div class="lang-block lang-cn">\s*'
        r'<span class="lang-label">中文翻译</span>\s*'
        r'<blockquote>(.*?)</blockquote>\s*'
        r'</div>\s*'
        r'</div>',
        re.DOTALL
    )
    
    for match in block_pattern.finditer(html_content):
        en_content = match.group(1).strip()
        cn_content = match.group(2).strip()
        blocks.append({
            'en_text': en_content,
            'cn_text': cn_content,
        })
    
    return blocks

def main():
    with open('1996.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    blocks = extract_blocks(html_content)
    
    need_translation = []
    for i, block in enumerate(blocks):
        en_plain = re.sub(r'<[^>]+>', '', block['en_text']).strip()
        cn_plain = re.sub(r'<[^>]+>', '', block['cn_text']).strip()
        en_len = len(en_plain)
        cn_len = len(cn_plain)
        
        if en_len > 0 and cn_len < en_len * 0.4:
            need_translation.append((i, en_plain))
    
    with open('need_translation.txt', 'w', encoding='utf-8') as f:
        for idx, en in need_translation:
            f.write(f"=== BLOCK {idx} ===\n")
            f.write(en + "\n\n")

if __name__ == '__main__':
    main()
