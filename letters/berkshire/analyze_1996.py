#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复1996年巴菲特致股东信的中文翻译质量
- 分析双语块，找出中文长度不足英文50%的块
- 使用参考翻译补全
"""

import re
from pathlib import Path

# 读取原始HTML文件 - 使用绝对路径
BASE_DIR = Path("/app/data/所有对话/主对话")
html_path = BASE_DIR / "投资研究/知识库/巴菲特知识库-LearnBuffett版/letters/berkshire/1996.html"
html_content = html_path.read_text(encoding='utf-8')

def count_chinese_chars(text):
    """统计中文字符数量"""
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    return len(chinese_pattern.findall(text))

def count_en_chars(text):
    """统计英文字符数量"""
    en_pattern = re.compile(r'[a-zA-Z]')
    return len(en_pattern.findall(text))

def strip_tags(text):
    """移除HTML标签"""
    return re.sub(r'<[^>]+>', '', text)

def extract_all_bilingual_blocks(html):
    """提取所有bilingual block"""
    blocks = []
    pattern = re.compile(
        r'<div class="bilingual-block">\s*<div class="lang-block lang-en">.*?<span class="lang-label">English</span>\s*<blockquote>(.*?)</blockquote>\s*</div>\s*<div class="lang-block lang-cn">.*?<span class="lang-label">中文翻译</span>\s*<blockquote>(.*?)</blockquote>\s*</div>\s*</div>',
        re.DOTALL
    )
    for match in pattern.finditer(html):
        en_content = strip_tags(match.group(1)).strip()
        cn_content = strip_tags(match.group(2)).strip()
        blocks.append({
            'en': en_content,
            'cn': cn_content,
            'match_start': match.start(),
            'match_end': match.end(),
            'full_match': match.group(0)
        })
    return blocks

def analyze_blocks():
    """分析所有双语块"""
    blocks = extract_all_bilingual_blocks(html_content)
    
    print(f"总共找到 {len(blocks)} 个双语块")
    
    incomplete = []
    for i, block in enumerate(blocks):
        en_len = count_en_chars(block['en'])
        cn_len = count_chinese_chars(block['cn'])
        
        # 跳过空块
        if not block['en'] or not block['cn']:
            continue
        
        # 跳过纯分隔符
        if block['en'].replace('*', '').replace('-', '').replace(' ', '').replace('=', '') == '':
            continue
        
        ratio = cn_len / en_len if en_len > 0 else 0
        
        if ratio < 0.5 and en_len > 50:
            incomplete.append({
                'index': i,
                'en': block['en'],
                'cn': block['cn'],
                'en_len': en_len,
                'cn_len': cn_len,
                'ratio': ratio,
                'match_start': block['match_start'],
                'match_end': block['match_end']
            })
    
    return blocks, incomplete

if __name__ == "__main__":
    blocks, incomplete = analyze_blocks()
    print(f"\n发现 {len(incomplete)} 个翻译不完整的双语块（中文/英文 < 50%）")
    
    print("\n" + "="*80)
    print("不完整块示例（前20个）:")
    print("="*80)
    
    for i, block in enumerate(incomplete[:20]):
        print(f"\n【块 {block['index']}】英文长度: {block['en_len']}, 中文长度: {block['cn_len']}, 比例: {block['ratio']:.2%}")
        print(f"英文开头: {block['en'][:150]}...")
        print(f"中文开头: {block['cn'][:100]}...")
