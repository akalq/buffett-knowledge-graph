#!/usr/bin/env python3
"""
批量修复巴菲特知识库信件详情页的Logo和导航栏一致性
"""

import os
import re
from pathlib import Path

# 统一的新Header HTML (用于 site-header 类)
NEW_HEADER_SITE = '''    <header class="site-header">
        <div class="header-inner">
            <a href="../../index.html" class="site-logo">
                <span>📚 巴菲特知识库</span>
            </a>
            <nav class="site-nav">
                <a href="../index-pages/巴菲特致股东信总览.html" class="nav-link">📝 信件</a>
                <a href="../index-pages/核心思想索引.html" class="nav-link">💡 概念</a>
                <a href="../index-pages/公司索引.html" class="nav-link">🏢 公司</a>
                <a href="../index-pages/人物索引.html" class="nav-link">👤 人物</a>
                <a href="../index-pages/时间线.html" class="nav-link">📅 时间线</a>
                <a href="../index-pages/知识树.html" class="nav-link">🌳 知识树</a>
            </nav>
        </div>
    </header>'''

# 统一的新Header HTML (用于内联样式的header)
NEW_HEADER_INLINE = '''    <header>
        <div class="container">
            <a href="../../index.html" class="logo">
                <span>📚 巴菲特知识库</span>
            </a>
            <nav>
                <a href="../../index-pages/巴菲特致股东信总览.html">📝 信件</a>
                <a href="../../index-pages/核心思想索引.html">💡 概念</a>
                <a href="../../index-pages/公司索引.html">🏢 公司</a>
                <a href="../../index-pages/人物索引.html">👤 人物</a>
                <a href="../../index-pages/时间线.html">📅 时间线</a>
                <a href="../../index-pages/知识树.html">🌳 知识树</a>
            </nav>
        </div>
    </header>'''

def fix_letter_html(filepath):
    """修复单个信件详情页的header"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 检查是否是 site-header 类
    if 'class="site-header"' in content:
        if '📚 巴菲特知识库' in content and '📅 时间线' in content:
            return False  # 已经修复
        old_header_pattern = r'<header class="site-header">.*?</header>'
        new_content = re.sub(old_header_pattern, NEW_HEADER_SITE, content, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    
    # 检查是否是内联样式的 header
    if re.search(r'<header>\s*<div class="container">\s*<a href="../../index.html" class="logo">', content):
        if '📚 巴菲特知识库' in content and '📅 时间线' in content:
            return False  # 已经修复
        old_header_pattern = r'<header>\s*<div class="container">\s*<a href="../../index\.html" class="logo">.*?</header>'
        new_content = re.sub(old_header_pattern, NEW_HEADER_INLINE, content, flags=re.DOTALL)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    
    return False

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.absolute()
    base_path = script_dir
    
    # 需要检查的目录
    dirs_to_check = [
        base_path / 'letters' / 'berkshire',
        base_path / 'letters' / 'partnership',
        base_path / 'letters' / 'special',
    ]
    
    total_fixed = 0
    total_skipped = 0
    total_errors = 0
    
    for dir_path in dirs_to_check:
        if not dir_path.exists():
            print(f"目录不存在: {dir_path}")
            continue
        
        html_files = list(dir_path.glob('*.html'))
        print(f"\n检查目录: {dir_path.name}/ ({len(html_files)} 个文件)")
        
        for html_file in html_files:
            try:
                if fix_letter_html(html_file):
                    print(f"  ✅ 修复: {html_file.name}")
                    total_fixed += 1
                else:
                    total_skipped += 1
            except Exception as e:
                print(f"  ❌ 错误: {html_file.name} - {e}")
                total_errors += 1
    
    print(f"\n========== 修复完成 ==========")
    print(f"修复: {total_fixed} 个文件")
    print(f"跳过: {total_skipped} 个文件")
    print(f"错误: {total_errors} 个文件")

if __name__ == '__main__':
    main()
