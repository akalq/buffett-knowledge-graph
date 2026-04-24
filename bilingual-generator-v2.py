#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巴菲特致股东信中英对照文件生成器 - 方案A（章节对照版）
改进版：基于段落对齐的智能匹配
"""

import os
import re
import html
from pathlib import Path

def extract_text_from_html(html_content):
    """从HTML中提取纯文本"""
    match = re.search(r'<pre>(.*?)</pre>', html_content, re.DOTALL)
    if match:
        text = match.group(1)
        text = html.unescape(text)
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    return ""

def read_file_safe(path, encoding='utf-8'):
    """安全读取文件"""
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='latin-1') as f:
                return f.read()
        except:
            return ""

def split_english_paragraphs(text):
    """分割英文原文为段落"""
    # 按双换行分割
    paras = text.split('\n\n')
    result = []
    for p in paras:
        p = p.strip()
        if p:
            result.append(p)
    return result

def split_chinese_sections(text):
    """解析中文翻译的章节结构，返回章节列表"""
    sections = []
    
    # 按**标题**分割
    parts = re.split(r'\*\*([^*]+)\*\*', text)
    
    current_section = {"title": "开场", "content": []}
    
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
            
        if i % 2 == 1:
            # 这是标题
            if current_section["content"]:
                sections.append(current_section)
            current_section = {"title": part, "content": []}
        else:
            # 这是内容
            if part:
                paras = [p.strip() for p in part.split('\n\n') if p.strip()]
                current_section["content"].extend(paras)
    
    if current_section["content"]:
        sections.append(current_section)
    
    return sections

def align_paragraphs(eng_paras, chi_sections):
    """将英文段落与中文章节对齐"""
    matched = []
    
    eng_idx = 0
    total_eng = len(eng_paras)
    
    for section in chi_sections:
        chi_title = section["title"]
        chi_content = section["content"]
        num_chi_paras = len(chi_content)
        
        # 估算应该分配的英文段落数
        # 根据比例分配
        if total_eng > eng_idx:
            # 至少分配1段，最多分配剩余的全部
            eng_slice = eng_paras[eng_idx:eng_idx + max(1, num_chi_paras)]
            eng_content = '\n\n'.join(eng_slice)
            eng_idx += len(eng_slice)
        else:
            eng_content = ""
        
        # 查找中英文章节对应关系
        chi_eng_title = find_chapter_mapping(chi_title)
        
        matched.append({
            "title_zh": chi_title,
            "title_en": chi_eng_title,
            "content_en": eng_content,
            "content_zh": '\n\n'.join(chi_content)
        })
    
    return matched

def find_chapter_mapping(chi_title):
    """根据中文章节标题查找对应的英文标题"""
    mappings = {
        "致股东": "To the Shareholders",
        "纺织事业": "Textile Operations",
        "纺织": "Textile Operations",
        "保险业务": "Insurance Operations",
        "保险": "Insurance",
        "保险投资": "Insurance Investments",
        "银行业": "Banking",
        "蓝筹邮票": "Blue Chip Stamps",
        "韦斯科金融": "Wesco Financial",
        "税务": "Taxation",
        "会计": "Accounting",
        "购并": "Acquisitions",
        "展望": "Outlook",
        "结语": "Conclusion",
        "数据": "Data",
        "公用事业": "Utilities",
        "铁路": "Railroad",
        "制造业": "Manufacturing",
        "零售业": "Retailing",
        "股东": "Shareholders",
        "一般": "General",
    }
    
    for chi, eng in mappings.items():
        if chi in chi_title:
            return eng
    return ""

def generate_bilingual_content(year, matched, source_url):
    """生成方案A格式的中英对照内容"""
    lines = []
    lines.append(f"# {year}年巴菲特致股东信 - 中英对照")
    lines.append("")
    lines.append(f"> 原文来源：{source_url}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for i, section in enumerate(matched, 1):
        # 标题行使用中文章节名（因为更完整）
        title = section['title_zh']
        if section['title_en']:
            title = f"{title} / {section['title_en']}"
        
        lines.append(f"## {title}")
        lines.append("")
        lines.append("### 英文")
        lines.append("")
        lines.append(section['content_en'])
        lines.append("")
        lines.append("### 中文")
        lines.append("")
        lines.append(section['content_zh'])
        lines.append("")
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)

def process_year(year, base_path, chi_dir):
    """处理单个年份的文件"""
    eng_dir = base_path / "english-letters"
    raw_dir = base_path.parent / "巴菲特股东信翻译"
    out_dir = base_path / "bilingual-letters"
    
    source_url = f"berkshirehathaway.com/letters/{year}.html"
    
    # 读取英文原文：优先html，然后raw_txt，最后txt
    eng_html = eng_dir / f"{year}.html"
    raw_txt = raw_dir / f"{year}_raw.txt"
    eng_txt = eng_dir / f"{year}.txt"
    
    eng_text = ""
    
    if eng_html.exists():
        eng_content = read_file_safe(eng_html)
        eng_text = extract_text_from_html(eng_content)
    elif raw_txt.exists():
        eng_text = read_file_safe(raw_txt)
    elif eng_txt.exists():
        eng_text = read_file_safe(eng_txt, 'utf-8')
    
    if not eng_text:
        print(f"  [跳过] {year}: 无法读取英文原文")
        return False
    
    # 读取中文翻译
    chi_file = chi_dir / f"{year}.md"
    if not chi_file.exists():
        print(f"  [跳过] {year}: 找不到中文翻译")
        return False
    
    chi_content = read_file_safe(chi_file)
    if not chi_content:
        print(f"  [跳过] {year}: 无法读取中文翻译")
        return False
    
    # 分割段落
    eng_paras = split_english_paragraphs(eng_text)
    chi_sections = split_chinese_sections(chi_content)
    
    print(f"  英文段落: {len(eng_paras)}, 中文章节: {len(chi_sections)}")
    
    # 对齐
    matched = align_paragraphs(eng_paras, chi_sections)
    
    # 生成内容
    bilingual_content = generate_bilingual_content(year, matched, source_url)
    
    # 保存
    out_file = out_dir / f"{year}.md"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(bilingual_content)
    
    print(f"  [完成] {year}: {out_file}")
    return True

def main():
    """主函数"""
    script_dir = Path(__file__).parent
    base_path = script_dir
    chi_dir = script_dir.parent / "巴菲特股东信翻译"
    
    out_dir = base_path / "bilingual-letters"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    years = range(1977, 1991)
    
    print("=" * 60)
    print("巴菲特致股东信中英对照文件生成器 - 方案A (改进版)")
    print("=" * 60)
    print()
    
    success_count = 0
    for year in years:
        print(f"处理 {year} 年...")
        if process_year(year, base_path, chi_dir):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"完成！成功处理 {success_count}/{len(years)} 个年份")
    print("=" * 60)

if __name__ == "__main__":
    main()
