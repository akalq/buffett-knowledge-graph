#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
巴菲特知识库 - 链接系统构建工具
"""

import json
import os
import re
from collections import defaultdict
from pathlib import Path

# 路径配置 - 使用脚本所在目录的绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(SCRIPT_DIR)
DATA_DIR = BASE_DIR / "data"
CONCEPTS_DIR = BASE_DIR / "concepts"
COMPANIES_DIR = BASE_DIR / "companies"
LETTERS_DIR = BASE_DIR / "letters"

print(f"脚本目录: {SCRIPT_DIR}")
print(f"工作目录: {BASE_DIR}")

# ============================================
# 第一部分：实体名称标准化词典
# ============================================

# 公司名称标准化映射
COMPANY_ALIASES = {
    # 英文名称 -> 标准中文名
    "Berkshire Hathaway": "伯克希尔哈撒韦",
    "Berkshire": "伯克希尔哈撒韦",
    "伯克希尔·哈撒韦": "伯克希尔哈撒韦",
    "伯克希尔哈撒韦": "伯克希尔哈撒韦",
    "GEICO": "盖可保险",
    "GEICO保险": "盖可保险",
    "Washington Post": "华盛顿邮报",
    "华盛顿邮报": "华盛顿邮报",
    "The Washington Post": "华盛顿邮报",
    "See's Candies": "喜诗糖果",
    "喜诗糖果": "喜诗糖果",
    "See's": "喜诗糖果",
    "可口可乐": "可口可乐",
    "Coca-Cola": "可口可乐",
    "美国运通": "美国运通",
    "American Express": "美国运通",
    "IBM": "IBM",
    "Apple": "苹果",
    "苹果公司": "苹果",
    "富国银行": "富国银行",
    "Wells Fargo": "富国银行",
    "Wells Fargo & Company": "富国银行",
    "Wesco Financial": "韦斯科金融",
    "韦斯科": "韦斯科金融",
    "Wesco": "韦斯科金融",
    "BNSF Railway": "BNSF铁路",
    "BNSF": "BNSF铁路",
    "中美能源": "中美能源",
    "MidAmerican": "中美能源",
    "MidAmerican Energy": "中美能源",
    "国民保险": "国民保险公司",
    "National Indemnity": "国民保险公司",
    "吉列": "吉列",
    "Gillette": "吉列",
    "宝洁": "宝洁",
    "Procter & Gamble": "宝洁",
    "卡夫": "卡夫",
    "Kraft": "卡夫",
    "卡夫亨氏": "卡夫亨氏",
    "Kraft Heinz": "卡夫亨氏",
    "Heinz": "卡夫亨氏",
    "比亚迪": "比亚迪",
    "BYD": "比亚迪",
    "鲜果布衣": "鲜果布衣",
    "Fruit of the Loom": "鲜果布衣",
    "冰雪皇后": "冰雪皇后",
    "Dairy Queen": "冰雪皇后",
    "DQ": "冰雪皇后",
    "沃尔玛": "沃尔玛",
    "Walmart": "沃尔玛",
    "Target": "塔吉特",
    "塔吉特": "塔吉特",
    "迪士尼": "迪士尼",
    "Disney": "迪士尼",
    "美国银行": "美国银行",
    "Bank of America": "美国银行",
    "高盛": "高盛",
    "Goldman Sachs": "高盛",
    "摩根大通": "摩根大通",
    "JPMorgan": "摩根大通",
    "JPMorgan Chase": "摩根大通",
    "通用电气": "通用电气",
    "GE": "通用电气",
    "GM": "通用汽车",
    "通用汽车": "通用汽车",
    "房地美": "房地美",
    "Freddie Mac": "房地美",
    "穆迪": "穆迪",
    "Moody's": "穆迪",
    "3M": "3M",
}

# 人物名称标准化映射
PERSON_ALIASES = {
    # 英文名 -> 标准中文名
    "Buffett": "巴菲特",
    "Warren Buffett": "巴菲特",
    "沃伦·巴菲特": "巴菲特",
    "巴菲特": "巴菲特",
    "Charlie Munger": "芒格",
    "Charlie": "芒格",
    "Munger": "芒格",
    "查理·芒格": "芒格",
    "芒格": "芒格",
    "Graham": "格雷厄姆",
    "Ben Graham": "格雷厄姆",
    "本杰明·格雷厄姆": "格雷厄姆",
    "Benjamin Graham": "格雷厄姆",
    "格雷厄姆": "格雷厄姆",
    "Ajit Jain": "阿吉特·贾恩",
    "阿吉特·贾恩": "阿吉特·贾恩",
    "Ajit": "阿吉特·贾恩",
    "贾恩": "阿吉特·贾恩",
    "Greg Abel": "格雷格·阿贝尔",
    "Greg": "格雷格·阿贝尔",
    "阿贝尔": "格雷格·阿贝尔",
    "韦斯科金融": "格雷格·阿贝尔",
    "Todd Combs": "托德·库姆斯",
    "Todd": "托德·库姆斯",
    "库姆斯": "托德·库姆斯",
    "Ted Weschler": "泰德·韦施勒",
    "Ted": "泰德·韦施勒",
    "韦施勒": "泰德·韦施勒",
    "B夫人": "B夫人",
    "Mrs. B": "B夫人",
    "Rose Blumkin": "B夫人",
    "Mrs. Blumkin": "B夫人",
    "Lou Simpson": "路易·辛普森",
    "Lou": "路易·辛普森",
    "辛普森": "路易·辛普森",
    "Simpson": "路易·辛普森",
    "Gene Abegg": "吉恩·阿贝格",
    "Abegg": "吉恩·阿贝格",
    "阿贝格": "吉恩·阿贝格",
    "Phil Liesche": "菲尔·利舍",
    "Liesche": "菲尔·利舍",
    "利舍": "菲尔·利舍",
    "Jack Ringwalt": "杰克·林沃尔特",
    "John Ringwalt": "约翰·林沃尔特",
    "Ringwalt": "杰克·林沃尔特",
    "Ken Chace": "肯·蔡斯",
    "Chace": "肯·蔡斯",
    "Chuck Huggins": "查克·哈金斯",
    "Huggins": "查克·哈金斯",
    "Tom Murphy": "汤姆·墨菲",
    "Murphy": "汤姆·墨菲",
    "墨菲": "汤姆·墨菲",
    "Peter Jeffrey": "彼得·杰弗里",
    "George Young": "乔治·杨",
    "Floyd Taylor": "弗洛伊德·泰勒",
    "Milt Thornton": "米尔特·桑顿",
}

# 概念名称标准化映射
CONCEPT_ALIASES = {
    # 各种写法 -> 标准名称
    "内在价值": "内在价值",
    "Intrinsic Value": "内在价值",
    "企业价值": "内在价值",
    "护城河": "护城河",
    "Economic Moat": "护城河",
    "Moat": "护城河",
    "城堡": "护城河",
    "安全边际": "安全边际",
    "Margin of Safety": "安全边际",
    "能力圈": "能力圈",
    "Circle of Competence": "能力圈",
    "Competence": "能力圈",
    "管理层": "管理层",
    "Management": "管理层",
    "经理": "管理层",
    "复利": "复利",
    "Compound Interest": "复利",
    "Compound": "复利",
    "账面价值": "账面价值",
    "Book Value": "账面价值",
    "账面值": "账面价值",
    "股东权益": "账面价值",
    "市值": "市值",
    "Market Value": "市值",
    "市场价格": "市值",
    "保险浮存金": "保险浮存金",
    "Float": "保险浮存金",
    "浮存金": "保险浮存金",
    "保险公司": "保险业",
    "Insurance": "保险业",
    "保险业务": "保险业",
    "保险": "保险业",
    "股东权益报酬率": "股东权益报酬率",
    "ROE": "股东权益报酬率",
    "Return on Equity": "股东权益报酬率",
    "权益报酬率": "股东权益报酬率",
    "通货膨胀": "通货膨胀",
    "Inflation": "通货膨胀",
    "通胀": "通货膨胀",
    "长期投资": "长期持有",
    "Long-term Investment": "长期持有",
    "长期持有": "长期持有",
    "买入并持有": "长期持有",
    "市场先生": "市场先生",
    "Mr. Market": "市场先生",
    "分散投资": "分散投资",
    "Diversification": "分散投资",
    "多元化": "分散投资",
    "集中投资": "集中投资",
    "Concentration": "集中投资",
    "回购": "股票回购",
    "Share Repurchase": "股票回购",
    "股票回购": "股票回购",
    "回购股票": "股票回购",
    "现金回购": "股票回购",
    "回购股份": "股票回购",
    "股息": "股息",
    "Dividend": "股息",
    "分红": "股息",
    "股利": "股息",
    "留存收益": "留存收益",
    "Retained Earnings": "留存收益",
    "透视盈余": "透视盈余",
    "Look-through Earnings": "透视盈余",
    "商誉": "商誉",
    "Goodwill": "商誉",
    "经济商誉": "经济商誉",
    "品牌": "品牌",
    "Brand": "品牌",
    "特许经营权": "特许经营权",
    "Franchise": "特许经营权",
    "竞争优势": "竞争优势",
    "Competitive Advantage": "竞争优势",
    "企业文化": "企业文化",
    "Corporate Culture": "企业文化",
    "诚信": "诚信",
    "Integrity": "诚信",
    "正直": "诚信",
    "资本主义": "资本主义",
    "并购": "并购",
    "M&A": "并购",
    "收购": "并购",
}

def normalize_entity(entity: str, alias_map: dict) -> str:
    """标准化实体名称"""
    if entity in alias_map:
        return alias_map[entity]
    return entity

def load_links_data():
    """加载links.json数据"""
    links_file = BASE_DIR / "links.json"
    print(f"加载文件: {links_file}")
    with open(links_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_entity_dict():
    """构建标准化实体词典"""
    links_data = load_links_data()
    
    entities = {
        "companies": {},
        "people": {},
        "concepts": {}
    }
    
    # 收集所有唯一实体
    for letter in links_data.get("letters", []):
        year = letter.get("year")
        
        # 处理公司
        for company in letter.get("companies", []):
            normalized = normalize_entity(company, COMPANY_ALIASES)
            if normalized not in entities["companies"]:
                entities["companies"][normalized] = {
                    "aliases": [],
                    "years": []
                }
            entities["companies"][normalized]["years"].append(year)
            if company != normalized and company not in entities["companies"][normalized]["aliases"]:
                entities["companies"][normalized]["aliases"].append(company)
        
        # 处理人物
        for person in letter.get("people", []):
            normalized = normalize_entity(person, PERSON_ALIASES)
            if normalized not in entities["people"]:
                entities["people"][normalized] = {
                    "aliases": [],
                    "years": []
                }
            entities["people"][normalized]["years"].append(year)
            if person != normalized and person not in entities["people"][normalized]["aliases"]:
                entities["people"][normalized]["aliases"].append(person)
        
        # 处理概念
        for concept in letter.get("concepts", []):
            normalized = normalize_entity(concept, CONCEPT_ALIASES)
            if normalized not in entities["concepts"]:
                entities["concepts"][normalized] = {
                    "aliases": [],
                    "years": []
                }
            entities["concepts"][normalized]["years"].append(year)
            if concept != normalized and concept not in entities["concepts"][normalized]["aliases"]:
                entities["concepts"][normalized]["aliases"].append(concept)
    
    # 去重年份并排序
    for category in entities:
        for entity_name in entities[category]:
            entities[category][entity_name]["years"] = sorted(list(set(entities[category][entity_name]["years"])))
    
    return entities

def build_reference_counts():
    """构建引用统计"""
    entities = build_entity_dict()
    
    reference_counts = {
        "concepts": {},
        "companies": {},
        "people": {}
    }
    
    for concept_name, data in entities["concepts"].items():
        reference_counts["concepts"][concept_name] = {
            "count": len(data["years"]),
            "letters": data["years"]
        }
    
    for company_name, data in entities["companies"].items():
        reference_counts["companies"][company_name] = {
            "count": len(data["years"]),
            "letters": data["years"]
        }
    
    for person_name, data in entities["people"].items():
        reference_counts["people"][person_name] = {
            "count": len(data["years"]),
            "letters": data["years"]
        }
    
    # 按引用次数排序
    reference_counts["concepts"] = dict(sorted(
        reference_counts["concepts"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    ))
    reference_counts["companies"] = dict(sorted(
        reference_counts["companies"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    ))
    reference_counts["people"] = dict(sorted(
        reference_counts["people"].items(),
        key=lambda x: x[1]["count"],
        reverse=True
    ))
    
    return reference_counts

def build_backlinks():
    """构建反向链接数据"""
    links_data = load_links_data()
    
    backlinks = {
        "concepts": {},
        "companies": {},
        "people": {}
    }
    
    for letter in links_data.get("letters", []):
        year = letter.get("year")
        letter_key = f"letters/berkshire/{year}"
        
        # 处理公司链接
        for company in letter.get("companies", []):
            normalized = normalize_entity(company, COMPANY_ALIASES)
            key = f"companies/{normalized}"
            if key not in backlinks["companies"]:
                backlinks["companies"][key] = []
            backlinks["companies"][key].append({
                "source": letter_key,
                "year": year
            })
        
        # 处理人物链接
        for person in letter.get("people", []):
            normalized = normalize_entity(person, PERSON_ALIASES)
            key = f"people/{normalized}"
            if key not in backlinks["people"]:
                backlinks["people"][key] = []
            backlinks["people"][key].append({
                "source": letter_key,
                "year": year
            })
        
        # 处理概念链接
        for concept in letter.get("concepts", []):
            normalized = normalize_entity(concept, CONCEPT_ALIASES)
            key = f"concepts/{normalized}"
            if key not in backlinks["concepts"]:
                backlinks["concepts"][key] = []
            backlinks["concepts"][key].append({
                "source": letter_key,
                "year": year
            })
    
    return backlinks

def save_json(data, filename):
    """保存JSON文件"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存: {filepath}")

def main():
    print("=" * 60)
    print("巴菲特知识库 - 链接系统构建工具")
    print("=" * 60)
    
    # 确保data目录存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 第一步：构建实体词典
    print("\n📦 第一步：构建实体词典...")
    entities = build_entity_dict()
    save_json(entities, "entities.json")
    
    # 第二步：构建引用统计
    print("\n📊 第二步：构建引用统计...")
    reference_counts = build_reference_counts()
    save_json(reference_counts, "reference_counts.json")
    
    # 第三步：构建反向链接
    print("\n🔗 第三步：构建反向链接...")
    backlinks = build_backlinks()
    save_json(backlinks, "backlinks.json")
    
    print("\n" + "=" * 60)
    print("数据生成完成！")
    print("=" * 60)
    
    # 输出TOP 10统计
    print("\n📈 TOP 10 概念（按引用次数）：")
    for i, (name, data) in enumerate(list(reference_counts["concepts"].items())[:10]):
        print(f"  {i+1}. {name}: {data['count']}次")
    
    print("\n🏢 TOP 10 公司（按引用次数）：")
    for i, (name, data) in enumerate(list(reference_counts["companies"].items())[:10]):
        print(f"  {i+1}. {name}: {data['count']}次")
    
    print("\n👤 TOP 10 人物（按引用次数）：")
    for i, (name, data) in enumerate(list(reference_counts["people"].items())[:10]):
        print(f"  {i+1}. {name}: {data['count']}次")

if __name__ == "__main__":
    main()
