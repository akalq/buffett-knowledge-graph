#!/usr/bin/env python3
"""
巴菲特知识库链接系统处理脚本
1. 清洗链接数据
2. 完善反向链接统计
3. 更新HTML页面
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path

# 获取当前脚本所在目录
SCRIPT_DIR = Path(__file__).parent.resolve()

# 路径配置 - 使用相对于脚本的路径
DATA_DIR = SCRIPT_DIR / "data"
HTML_DIR = SCRIPT_DIR.parent / "buffett-km" / "letters"
OUTPUT_DIR = DATA_DIR / "processed"

# 确保输出目录存在
OUTPUT_DIR.mkdir(exist_ok=True)

def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """保存JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== 第1部分：清洗链接数据 ====================

def normalize_entity_name(name):
    """标准化实体名称"""
    # 去除首尾空格
    name = name.strip()
    # 统一引号
    name = name.replace('"', '"').replace('"', '"')
    name = name.replace(''', "'").replace(''', "'")
    return name

def clean_entities():
    """清洗并标准化实体数据"""
    entities = load_json(DATA_DIR / "entities.json")
    
    cleaned = {
        "companies": {},
        "people": {},
        "concepts": {}
    }
    
    # 标准化公司名称
    seen_companies = {}  # 用于检测重复
    for name, data in entities.get("companies", {}).items():
        norm_name = normalize_entity_name(name)
        if norm_name in seen_companies:
            # 合并别名和年份
            existing = seen_companies[norm_name]
            existing["aliases"] = list(set(existing["aliases"] + data.get("aliases", [])))
            existing["years"] = sorted(set(existing["years"] + data.get("years", [])))
        else:
            cleaned["companies"][norm_name] = {
                "aliases": list(set(data.get("aliases", []))),
                "years": sorted(set(data.get("years", [])))
            }
            seen_companies[norm_name] = cleaned["companies"][norm_name]
    
    # 标准化人物名称
    seen_people = {}
    for name, data in entities.get("people", {}).items():
        norm_name = normalize_entity_name(name)
        if norm_name in seen_people:
            existing = seen_people[norm_name]
            existing["aliases"] = list(set(existing["aliases"] + data.get("aliases", [])))
            existing["years"] = sorted(set(existing["years"] + data.get("years", [])))
        else:
            cleaned["people"][norm_name] = {
                "aliases": list(set(data.get("aliases", []))),
                "years": sorted(set(data.get("years", [])))
            }
            seen_people[norm_name] = cleaned["people"][norm_name]
    
    # 标准化概念名称
    for name, data in entities.get("concepts", {}).items():
        norm_name = normalize_entity_name(name)
        cleaned["concepts"][norm_name] = {
            "aliases": list(set(data.get("aliases", []))),
            "years": sorted(set(data.get("years", [])))
        }
    
    return cleaned

# ==================== 第2部分：完善反向链接统计 ====================

def calculate_reference_stats():
    """计算引用统计并排序"""
    ref_counts = load_json(DATA_DIR / "reference_counts.json")
    backlinks = load_json(DATA_DIR / "backlinks.json")
    entities = load_json(DATA_DIR / "entities.json")
    
    stats = {
        "concepts": {},
        "companies": {},
        "people": {}
    }
    
    # 计算概念引用统计
    for concept, data in ref_counts.get("concepts", {}).items():
        count = data.get("count", 0)
        years = data.get("letters", [])
        stats["concepts"][concept] = {
            "count": count,
            "years": sorted(years),
            "first_year": min(years) if years else None,
            "last_year": max(years) if years else None
        }
    
    # 计算公司引用统计
    for company, data in entities.get("companies", {}).items():
        years = data.get("years", [])
        stats["companies"][company] = {
            "count": len(years),
            "years": years,
            "first_year": min(years) if years else None,
            "last_year": max(years) if years else None
        }
    
    # 计算人物引用统计
    for person, data in entities.get("people", {}).items():
        years = data.get("years", [])
        stats["people"][person] = {
            "count": len(years),
            "years": years,
            "first_year": min(years) if years else None,
            "last_year": max(years) if years else None
        }
    
    # 按引用频率排序
    stats["concepts_sorted"] = sorted(
        stats["concepts"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )
    stats["companies_sorted"] = sorted(
        stats["companies"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )
    stats["people_sorted"] = sorted(
        stats["people"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )
    
    return stats

def build_link_lookup(entities):
    """构建可用于链接查找的数据结构"""
    lookup = {}
    
    # 添加主要名称
    for category, items in entities.items():
        for name, data in items.items():
            lookup[name] = {
                "category": category.rstrip("s"),  # 去掉复数形式
                "count": len(data.get("years", []))
            }
            # 添加别名映射
            for alias in data.get("aliases", []):
                lookup[alias] = {
                    "category": category.rstrip("s"),
                    "primary_name": name,
                    "count": len(data.get("years", []))
                }
    
    return lookup

# ==================== 第3部分：更新HTML页面 ====================

def get_year_from_filename(filename):
    """从文件名提取年份"""
    match = re.search(r'(\d{4})', filename)
    return int(match.group(1)) if match else None

def add_entity_links_to_html(html_content, entities, year):
    """为HTML内容添加实体链接"""
    # 构建该年份涉及的所有实体
    year_entities = {
        "companies": [],
        "people": [],
        "concepts": []
    }
    
    for category, items in entities.items():
        for name, data in items.items():
            if year in data.get("years", []):
                category_key = category.rstrip("s") if category != "concepts" else "concept"
                year_entities[category_key if category == "concepts" else category].append(name)
    
    # 创建链接模式
    def make_link(match, entity_name, entity_type):
        """生成带链接的文本"""
        base_urls = {
            "companies": "../../companies/",
            "people": "../../people/",
            "concepts": "../../concepts/"
        }
        url = f'{base_urls[entity_type]}{entity_name}.html'
        return f'<a href="{url}" class="entity-link entity-{entity_type}" data-ref-count="{len(entities.get(entity_type if entity_type != "concept" else "concepts", {}).get(entity_name, {}).get("years", []))}">{match.group(0)}</a>'
    
    return html_content

def update_html_files(entities, stats):
    """更新所有HTML文件"""
    updated_count = 0
    
    # 遍历所有HTML文件
    for html_type in ["berkshire", "partnership", "special"]:
        html_path = HTML_DIR / html_type
        if not html_path.exists():
            continue
        
        for html_file in html_path.glob("*.html"):
            year = get_year_from_filename(html_file.name)
            if not year:
                continue
            
            # 读取HTML
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否需要更新
            if 'entity-link' in content:
                continue  # 已经处理过
            
            # 为HTML添加引用统计信息
            content = add_reference_stats_to_html(content, entities, stats, year)
            
            # 写回文件
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            updated_count += 1
    
    return updated_count

def add_reference_stats_to_html(content, entities, stats, year):
    """为HTML添加引用统计信息"""
    # 找到当前年份涉及的实体
    year_entities = {
        "companies": [],
        "people": [],
        "concepts": []
    }
    
    for category, items in entities.items():
        if category == "concepts":
            for name, data in items.items():
                if year in data.get("years", []):
                    year_entities["concepts"].append(name)
        elif category == "companies":
            for name, data in items.items():
                if year in data.get("years", []):
                    year_entities["companies"].append(name)
        elif category == "people":
            for name, data in items.items():
                if year in data.get("years", []):
                    year_entities["people"].append(name)
    
    # 生成引用统计面板HTML
    stats_html = generate_stats_panel(year_entities, stats, entities)
    
    # 在文章内容后添加统计面板
    if '</article>' in content:
        content = content.replace('</article>', stats_html + '\n                </article>')
    
    return content

def generate_stats_panel(year_entities, stats, entities):
    """生成引用统计面板"""
    panels = []
    
    # 概念统计
    if year_entities["concepts"]:
        concept_stats = []
        for name in year_entities["concepts"][:10]:  # 最多显示10个
            if name in stats.get("concepts", {}):
                count = stats["concepts"][name]["count"]
                concept_stats.append(f'<span class="stat-tag">{name} ({count}次)</span>')
        if concept_stats:
            panels.append(f'''
                <div class="entity-stats-panel">
                    <h3>📚 本年核心概念</h3>
                    <div class="stats-tags">{''.join(concept_stats)}</div>
                </div>''')
    
    # 公司统计
    if year_entities["companies"]:
        company_stats = []
        for name in year_entities["companies"][:10]:
            if name in stats.get("companies", {}):
                count = stats["companies"][name]["count"]
                company_stats.append(f'<span class="stat-tag stat-company">{name} ({count}次)</span>')
        if company_stats:
            panels.append(f'''
                <div class="entity-stats-panel">
                    <h3>🏢 涉及公司</h3>
                    <div class="stats-tags">{''.join(company_stats)}</div>
                </div>''')
    
    # 人物统计
    if year_entities["people"]:
        people_stats = []
        for name in year_entities["people"][:10]:
            if name in stats.get("people", {}):
                count = stats["people"][name]["count"]
                people_stats.append(f'<span class="stat-tag stat-person">{name} ({count}次)</span>')
        if people_stats:
            panels.append(f'''
                <div class="entity-stats-panel">
                    <h3>👤 关键人物</h3>
                    <div class="stats-tags">{''.join(people_stats)}</div>
                </div>''')
    
    if panels:
        return '<div class="reference-stats">' + '\n'.join(panels) + '\n                </div>'
    return ''

# ==================== 主函数 ====================

def main():
    print("=" * 60)
    print("巴菲特知识库链接系统处理")
    print("=" * 60)
    
    # 1. 清洗链接数据
    print("\n[1/3] 清洗链接数据...")
    cleaned_entities = clean_entities()
    save_json(cleaned_entities, OUTPUT_DIR / "entities_cleaned.json")
    print(f"   - 处理公司: {len(cleaned_entities['companies'])}")
    print(f"   - 处理人物: {len(cleaned_entities['people'])}")
    print(f"   - 处理概念: {len(cleaned_entities['concepts'])}")
    
    # 2. 计算引用统计
    print("\n[2/3] 计算引用统计...")
    stats = calculate_reference_stats()
    save_json(stats, OUTPUT_DIR / "reference_stats.json")
    print(f"   - 概念引用统计: {len(stats['concepts'])}")
    print(f"   - 公司引用统计: {len(stats['companies'])}")
    print(f"   - 人物引用统计: {len(stats['people'])}")
    
    # 显示Top 10概念
    print("\n   Top 10 引用概念:")
    for i, (name, data) in enumerate(stats["concepts_sorted"][:10], 1):
        print(f"   {i:2d}. {name}: {data['count']}次")
    
    # 3. 更新HTML文件
    print("\n[3/3] 更新HTML页面...")
    updated = update_html_files(cleaned_entities, stats)
    print(f"   - 更新文件数: {updated}")
    
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)
    
    return cleaned_entities, stats

if __name__ == "__main__":
    entities, stats = main()
