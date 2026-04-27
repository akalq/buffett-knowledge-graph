#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巴菲特致股东信中英对照文件生成器 - 方案A（章节对照版）
"""

import os
import re
import html
from pathlib import Path

# 章节对照映射表
CHAPTER_MAPPING = {
    # 英文章节 -> 中文章节
    'TO THE SHAREHOLDERS': '致股东',
    'TO THE STOCKHOLDERS': '致股东',
    'TEXTILE OPERATIONS': '纺织事业',
    'TEXTILES': '纺织事业',
    'INSURANCE OPERATIONS': '保险业务',
    'INSURANCE BUSINESS': '保险业务',
    'INSURANCE': '保险业务',
    'INSURANCE INVESTMENTS': '保险投资',
    'INSURANCE INVESTMENT': '保险投资',
    'BANKING': '银行业',
    'THE BANK': '银行业',
    'BLUE CHIP STAMPS': '蓝筹邮票',
    'BLUECHIP STAMPS': '蓝筹邮票',
    'BLUE CHIP': '蓝筹邮票',
    'WESCO FINANCIAL': '韦斯科金融',
    'FINANCIAL': '金融',
    'TAXATION': '税务',
    'MUTUAL FUND': '共同基金',
    'CORPORATE': '公司治理',
    'MANAGEMENT': '管理',
    'DIVIDEND': '股息',
    'ACQUISITIONS': '购并',
    'ACQUISITION': '购并',
    'OUTLOOK': '展望',
    'ACCOUNTING': '会计',
    'TREASURY STOCK': '库存股',
    'COMMON STOCK': '普通股',
    'MARKET': '市场',
    'INVESTMENT': '投资',
    'OTHER': '其他',
    'CONCLUSION': '结语',
    'DATA': '数据',
    'TABLE': '表格',
    'GEICO': '盖可保险',
    'RAILROAD': '铁路',
    'BNSF': '伯灵顿北方圣太菲铁路',
    'UTILITIES': '公用事业',
    'MANUFACTURING': '制造业',
    'RETAILING': '零售业',
    'BUILDING': '建筑业',
    'BUILDING PRODUCTS': '建材',
    'CONSUMER': '消费品',
    'PRODUCTS': '产品',
    'SALES': '销售',
    'EARNINGS': '盈余',
    'OWNERSHIP': '所有权',
    'SHAREHOLDER': '股东',
    'STOCKHOLDERS': '股东',
    'GENERALLY': '一般',
    'LOSS': '损失',
    'LOSSES': '损失',
    'PROFIT': '利润',
    'PROFITS': '利润',
}

def extract_text_from_html(html_content):
    """从HTML中提取纯文本"""
    # 提取<pre>标签内的内容
    match = re.search(r'<pre>(.*?)</pre>', html_content, re.DOTALL)
    if match:
        text = match.group(1)
        # 解码HTML实体
        text = html.unescape(text)
        # 清理多余空白
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

def parse_english_sections(text):
    """解析英文原文的章节结构"""
    sections = []
    
    # 分割段落
    paragraphs = text.split('\n\n')
    
    current_section = {"title": "Opening", "content": []}
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # 检测是否为章节标题（全大写且较短）
        is_title = False
        if para.isupper() and len(para) < 50:
            # 保存之前的章节
            if current_section["content"]:
                sections.append(current_section)
            # 新章节
            current_section = {"title": para, "content": []}
            is_title = True
        elif len(para) < 100 and para == para.title() and not para.endswith('.'):
            # 可能也是标题
            pass
        
        if not is_title:
            current_section["content"].append(para)
    
    # 保存最后一个章节
    if current_section["content"]:
        sections.append(current_section)
    
    return sections

def parse_chinese_sections(text):
    """解析中文翻译的章节结构"""
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
                # 分割成段落
                paras = [p.strip() for p in part.split('\n\n') if p.strip()]
                current_section["content"].extend(paras)
    
    if current_section["content"]:
        sections.append(current_section)
    
    return sections

def match_sections(eng_sections, chi_sections, year):
    """匹配中英文章节"""
    matched = []
    
    # 首先尝试按顺序匹配（考虑不同章节数量）
    eng_idx = 0
    chi_idx = 0
    
    while eng_idx < len(eng_sections) and chi_idx < len(chi_sections):
        eng_sec = eng_sections[eng_idx]
        chi_sec = chi_sections[chi_idx]
        
        eng_title = eng_sec["title"].upper().strip()
        chi_title = chi_sec["title"].strip()
        
        # 查找章节映射
        chi_eng_title = None
        for eng_key, chi_val in CHAPTER_MAPPING.items():
            if chi_val in chi_title or chi_title in eng_title:
                chi_eng_title = eng_key
                break
        
        matched.append({
            "title_en": eng_sec["title"],
            "title_zh": chi_sec["title"],
            "content_en": '\n\n'.join(eng_sec["content"]),
            "content_zh": '\n\n'.join(chi_sec["content"])
        })
        
        eng_idx += 1
        chi_idx += 1
    
    return matched

def generate_bilingual_content(year, matched_sections, source_url):
    """生成方案A格式的中英对照内容"""
    lines = []
    lines.append(f"# {year}年巴菲特致股东信 - 中英对照")
    lines.append("")
    lines.append(f"> 原文来源：{source_url}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    for i, section in enumerate(matched_sections, 1):
        lines.append(f"## {section['title_zh']}")
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
    out_dir = base_path / "bilingual-letters"
    
    # 读取英文原文（优先html，然后txt）
    eng_html = eng_dir / f"{year}.html"
    eng_txt = eng_dir / f"{year}.txt"
    
    eng_text = ""
    source_url = f"berkshirehathaway.com/letters/{year}.html"
    
    if eng_html.exists():
        eng_content = read_file_safe(eng_html)
        eng_text = extract_text_from_html(eng_content)
    elif eng_txt.exists():
        eng_content = read_file_safe(eng_txt, 'utf-8')
        if eng_content:
            eng_text = eng_content
    
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
    
    # 解析章节
    eng_sections = parse_english_sections(eng_text)
    chi_sections = parse_chinese_sections(chi_content)
    
    print(f"  英文章节: {len(eng_sections)}, 中文章节: {len(chi_sections)}")
    
    # 匹配章节
    matched = match_sections(eng_sections, chi_sections, year)
    
    # 生成对照内容
    bilingual_content = generate_bilingual_content(year, matched, source_url)
    
    # 保存文件
    out_file = out_dir / f"{year}.md"
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(bilingual_content)
    
    print(f"  [完成] {year}: {out_file}")
    return True

def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = Path(__file__).parent
    base_path = script_dir
    
    # 中文翻译目录在上级目录
    chi_dir = script_dir.parent / "巴菲特股东信翻译"
    
    # 确保输出目录存在
    out_dir = base_path / "bilingual-letters"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理年份范围：1977-1990
    years = range(1977, 1991)
    
    print("=" * 60)
    print("巴菲特致股东信中英对照文件生成器 - 方案A")
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
