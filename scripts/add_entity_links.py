#!/usr/bin/env python3
"""
增强版：HTML实体链接注入
为HTML信件中的实体名称添加可点击链接
"""

import json
import re
from pathlib import Path

# 路径配置
SCRIPT_DIR = Path(__file__).parent.resolve()
DATA_DIR = SCRIPT_DIR / "data"
HTML_DIR = SCRIPT_DIR.parent / "buffett-km" / "letters"

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_link_map():
    """构建可用于链接的名称映射"""
    entities = load_json(DATA_DIR / "entities.json")
    link_map = {
        "companies": {},
        "people": {},
        "concepts": {}
    }
    
    # 公司名称映射
    for name, data in entities.get("companies", {}).items():
        link_map["companies"][name] = name
        for alias in data.get("aliases", []):
            link_map["companies"][alias] = name
    
    # 人物名称映射
    for name, data in entities.get("people", {}).items():
        link_map["people"][name] = name
        for alias in data.get("aliases", []):
            link_map["people"][alias] = name
    
    # 概念名称映射
    for name, data in entities.get("concepts", {}).items():
        link_map["concepts"][name] = name
        for alias in data.get("aliases", []):
            link_map["concepts"][alias] = name
    
    return link_map

def create_entity_links(html_content, link_map, year):
    """为HTML内容中的实体创建链接"""
    
    # 定义链接模板
    def make_link(entity_type, entity_name):
        url = f'../../{entity_type}/{entity_name}.html'
        return f'<a href="{url}" class="entity-link entity-{entity_type}">{entity_name}</a>'
    
    # 处理公司链接
    for alias, primary in link_map["companies"].items():
        if len(alias) < 2:  # 跳过太短的名称
            continue
        pattern = re.compile(rf'(?<![a-zA-Z]){re.escape(alias)}(?![a-zA-Z])')
        replacement = make_link("companies", primary)
        html_content = pattern.sub(replacement, html_content)
    
    # 处理人物链接
    for alias, primary in link_map["people"].items():
        if len(alias) < 2:
            continue
        pattern = re.compile(rf'(?<![a-zA-Z]){re.escape(alias)}(?![a-zA-Z])')
        replacement = make_link("people", primary)
        html_content = pattern.sub(replacement, html_content)
    
    # 处理概念链接
    for alias, primary in link_map["concepts"].items():
        if len(alias) < 2:
            continue
        pattern = re.compile(rf'(?<![a-zA-Z]){re.escape(alias)}(?![a-zA-Z])')
        replacement = make_link("concepts", primary)
        html_content = pattern.sub(replacement, html_content)
    
    return html_content

def process_html_files():
    """处理所有HTML文件"""
    link_map = build_link_map()
    processed = 0
    
    for html_type in ["berkshire", "partnership", "special"]:
        html_path = HTML_DIR / html_type
        if not html_path.exists():
            continue
        
        for html_file in html_path.glob("*.html"):
            # 提取年份
            match = re.search(r'(\d{4})', html_file.name)
            if not match:
                continue
            year = int(match.group(1))
            
            # 读取文件
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 避免重复处理
            if 'entity-link' in content:
                # 已经有链接，检查是否需要增强
                pass
            
            # 添加实体链接
            content = create_entity_links(content, link_map, year)
            
            # 写回文件
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            processed += 1
    
    return processed

if __name__ == "__main__":
    print("开始为HTML文件注入实体链接...")
    count = process_html_files()
    print(f"处理完成: {count} 个文件")
