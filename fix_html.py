#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件中的重复引用来源部分
"""

import re
from pathlib import Path

CONCEPTS_PATH = Path("./投资研究/知识库/巴菲特知识库-LearnBuffett版/concepts")

def fix_html_file(html_file):
    """修复HTML文件中的重复引用来源部分"""
    with open(html_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否有多个"引用来源"
    count = content.count('>引用来源')
    if count <= 1:
        return False
    
    print(f"  发现 {count} 处引用来源标题")
    
    # 找到第一个<h2>引用来源的位置
    first_pos = content.find('<h2>引用来源')
    if first_pos == -1:
        return False
    
    # 找到</article>的位置
    article_end = content.find('</article>')
    if article_end == -1:
        return False
    
    # 保留从开头到第一个引用来源之前的内容
    before_citations = content[:first_pos]
    
    # 从第一个引用来源开始，找到</article>
    # 找到<h2>引用来源</h2>后面的所有内容，直到</article>
    citations_section_start = first_pos
    citations_section = content[citations_section_start:article_end]
    
    # 清理掉旧的重复引用来源部分，只保留第一个
    # 找到</article>前面最近的一个完整的citations-container
    pattern = r'(<div class="citations-container">.*?</div>\s*</div>\s*)</article>'
    match = re.search(pattern, citations_section, re.DOTALL)
    if match:
        new_citations = '<h2>引用来源' + match.group(1) + '</article>'
    else:
        # 如果上面的模式匹配失败，使用简单的截取
        # 找到最后一个</div>的位置（在</article>之前）
        last_div_before_article = citations_section.rfind('</div>', 0, len(citations_section) - len('</article>'))
        if last_div_before_article > 0:
            new_citations = citations_section[:last_div_before_article + 6] + '\n</article>'
        else:
            new_citations = citations_section + '</article>'
    
    # 组合新内容
    new_content = before_citations + new_citations + '\n\n    ' + content[article_end + len('</article>'):]
    
    # 清理多余的空白
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    return True

def main():
    html_files = list(CONCEPTS_PATH.glob("*.html"))
    fixed_count = 0
    
    for html_file in html_files:
        if fix_html_file(html_file):
            print(f"✓ 修复: {html_file.name}")
            fixed_count += 1
    
    print(f"\n共修复 {fixed_count} 个文件")

if __name__ == "__main__":
    main()
