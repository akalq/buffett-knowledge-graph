#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析1996.html中需要翻译的块"""

import re

def normalize_whitespace(text):
    """规范化空白字符"""
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\t', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = text.strip()
    return text

def extract_blocks(html_content):
    """提取所有bilingual-block"""
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
            'match': match
        })
    
    return blocks

def main():
    with open('1996.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    blocks = extract_blocks(html_content)
    print(f"总共 {len(blocks)} 个块\n")
    
    need_translation = []
    already_complete = []
    empty_blocks = []
    
    for i, block in enumerate(blocks):
        en_text = block['en_text']
        cn_text = block['cn_text']
        
        en_plain = re.sub(r'<[^>]+>', '', en_text).strip()
        cn_plain = re.sub(r'<[^>]+>', '', cn_text).strip()
        
        en_len = len(en_plain)
        cn_len = len(cn_plain)
        
        if not en_plain and not cn_plain:
            empty_blocks.append(i)
        elif cn_len >= en_len * 0.4:
            already_complete.append(i)
        else:
            need_translation.append(i)
    
    print(f"需要翻译: {len(need_translation)}")
    print(f"已完成: {len(already_complete)}")
    print(f"空块: {len(empty_blocks)}")
    
    print(f"\n需要翻译的块索引 ({len(need_translation)}个):")
    for idx in need_translation:
        block = blocks[idx]
        en_plain = re.sub(r'<[^>]+>', '', block['en_text']).strip()
        cn_plain = re.sub(r'<[^>]+>', '', block['cn_text']).strip()
        en_len = len(en_plain)
        cn_len = len(cn_plain)
        ratio = cn_len / en_len if en_len > 0 else 0
        print(f"\n--- 块 {idx} (中/英={ratio:.1%}) ---")
        print(f"EN ({en_len}): {en_plain[:200]}...")
        print(f"CN ({cn_len}): {cn_plain[:100]}...")

if __name__ == '__main__':
    main()
