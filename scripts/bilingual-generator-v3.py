#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巴菲特致股东信中英对照文件生成器 - 方案A（章节对照版）
最终版：智能段落对齐
"""

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

def split_english_text(text):
    """将英文文本分割成段落列表"""
    # 按双换行或单行分割
    # 先标准化空白
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # 分割段落
    paragraphs = []
    current = []
    
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            if current:
                para = ' '.join(current)
                if para:
                    paragraphs.append(para)
                current = []
        else:
            current.append(line)
    
    # 处理最后一段
    if current:
        para = ' '.join(current)
        if para:
            paragraphs.append(para)
    
    return paragraphs

def split_chinese_sections(text):
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
                # 按段落分割（中文通常用换行或空行分隔）
                paras = re.split(r'\n\s*\n', part)
                paras = [p.strip() for p in paras if p.strip()]
                current_section["content"].extend(paras)
    
    if current_section["content"]:
        sections.append(current_section)
    
    return sections

def align_content(eng_paras, chi_sections):
    """将英文内容分配到中文章节"""
    matched = []
    
    total_eng = len(eng_paras)
    total_chi_paras = sum(len(s["content"]) for s in chi_sections)
    
    eng_idx = 0
    
    for section in chi_sections:
        chi_title = section["title"]
        chi_paras = section["content"]
        num_chi = len(chi_paras)
        
        # 计算应该分配的英文段落数
        # 按中英文章节比例分配
        if total_chi_paras > 0 and eng_idx < total_eng:
            # 估算比例，但确保至少分配一些内容
            ratio = total_eng / total_chi_paras if total_chi_paras > 0 else 1
            estimated_eng_count = max(1, int(num_chi * ratio))
            
            # 分配英文段落
            eng_slice = eng_paras[eng_idx:eng_idx + estimated_eng_count]
            eng_idx += len(eng_slice)
        else:
            eng_slice = []
        
        eng_content = '\n\n'.join(eng_slice) if eng_slice else ""
        chi_content = '\n\n'.join(chi_paras)
        
        # 查找中英文章节对应
        chi_eng_title = find_chapter_mapping(chi_title)
        
        matched.append({
            "title_zh": chi_title,
            "title_en": chi_eng_title,
            "content_en": eng_content,
            "content_zh": chi_content
        })
    
    return matched

def find_chapter_mapping(chi_title):
    """根据中文章节标题查找对应的英文"""
    mappings = {
        "致股东": "To the Shareholders / Stockholders",
        "开场": "Opening",
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
    
    for section in matched:
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
    
    # 读取英文原文
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
    
    # 分割内容
    eng_paras = split_english_text(eng_text)
    chi_sections = split_chinese_sections(chi_content)
    
    print(f"  英文段落: {len(eng_paras)}, 中文章节: {len(chi_sections)}")
    
    # 对齐并生成
    matched = align_content(eng_paras, chi_sections)
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
    print("巴菲特致股东信中英对照文件生成器 - 方案A (最终版)")
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
