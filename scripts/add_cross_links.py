#!/usr/bin/env python3
"""
巴菲特知识库交叉链接脚本
为信件中的概念/公司/人物添加链接，并在目标页面添加反向链接
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import shutil

# 基础路径 - 使用绝对路径
BASE_DIR = Path("/app/data/所有对话/主对话/投资研究/知识库/巴菲特知识库-LearnBuffett版")
LETTERS_DIR = BASE_DIR / "letters/berkshire"
CONCEPTS_DIR = BASE_DIR / "concepts"
COMPANIES_DIR = BASE_DIR / "companies"
PEOPLE_DIR = BASE_DIR / "people"
LINKS_FILE = BASE_DIR / "links.json"


def load_links_data():
    """加载links.json数据"""
    with open(LINKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_keyword_mappings():
    """构建关键词到URL的映射"""
    data = load_links_data()
    
    # 收集所有概念、公司和人物
    all_concepts = set()
    all_companies = set()
    all_people = set()
    
    # 按年份记录引用关系
    concept_years = defaultdict(list)
    company_years = defaultdict(list)
    people_years = defaultdict(list)
    
    for letter in data.get('letters', []):
        year = str(letter['year'])
        for concept in letter.get('concepts', []):
            all_concepts.add(concept)
            concept_years[concept].append(year)
        for company in letter.get('companies', []):
            all_companies.add(company)
            company_years[company].append(year)
        for person in letter.get('people', []):
            all_people.add(person)
            people_years[person].append(year)
    
    # 构建URL映射
    concept_map = {}  # 关键词 -> URL
    company_map = {}  # 关键词 -> URL
    people_map = {}   # 关键词 -> URL
    
    # 概念映射
    for concept in all_concepts:
        # 转换概念名为URL
        url_concept = concept.replace(' ', '-')
        url = f"../../concepts/{concept}.html"
        concept_map[concept] = url
        # 添加英文变体
        if ' ' in concept:
            concept_map[concept.lower()] = url
            concept_map[concept.upper()] = url
    
    # 公司映射（处理中英文别名）
    company_url_map = {}  # 标准名 -> URL
    for company in all_companies:
        # 确定URL文件名
        if company in ['伯克希尔·哈撒韦']:
            url = "../../companies/伯克希尔哈撒韦.html"
        elif company in ['可口可乐']:
            url = "../../companies/可口可乐.html"
        elif company in ['华盛顿邮报']:
            url = "../../companies/华盛顿邮报.html"
        elif company in ['冰雪皇后']:
            url = "../../companies/冰雪皇后.html"
        elif company in ['吉列']:
            url = "../../companies/吉列.html"
        elif company in ['喜诗糖果']:
            url = "../../companies/喜诗糖果.html"
        elif company in ['美国运通']:
            url = "../../companies/美国运通.html"
        elif company in ['通用再保险']:
            url = "../../companies/通用再保险.html"
        elif company in ['布法罗新闻']:
            url = "../../companies/布法罗新闻.html"
        elif company in ['富国银行']:
            url = "../../companies/富国银行.html"
        elif company in ['宝洁']:
            url = "../../companies/宝洁.html"
        elif company in ['沃尔玛']:
            url = "../../companies/沃尔玛.html"
        elif company in ['中美能源']:
            url = "../../companies/中美能源.html"
        else:
            url = f"../../companies/{company}.html"
        
        company_url_map[company] = url
        company_map[company] = url
        
        # 添加中英文别名
        if company == 'Berkshire Hathaway':
            company_map['伯克希尔·哈撒韦'] = url
            company_map['Berkshire'] = url
            company_map['巴菲特的公司'] = url
        elif company == 'Coca-Cola':
            company_map['可口可乐'] = url
            company_map['可口可乐公司'] = url
        elif company == 'Washington Post':
            company_map['华盛顿邮报'] = url
        elif company == 'American Express':
            company_map['美国运通'] = url
        elif company == 'GEICO':
            company_map['GEICO保险'] = url
        elif company == 'Wells Fargo':
            company_map['富国银行'] = url
        elif company == "See's Candies":
            company_map['喜诗糖果'] = url
        elif company == 'Gillette':
            company_map['吉列'] = url
        elif company == 'General Re':
            company_map['通用再保险'] = url
        elif company == 'Buffalo News':
            company_map['布法罗新闻'] = url
        elif company == 'Nebraska Furniture Mart':
            company_map['内布拉斯加家具店'] = url
            company_map['NFM'] = url
        elif company == 'MidAmerican':
            company_map['中美能源'] = url
        elif company == 'IBM':
            company_map['IBM公司'] = url
    
    # 人物映射（处理别名）
    people_url_map = {}  # 标准名 -> URL
    for person in all_people:
        # 确定URL文件名
        if person in ['巴菲特', 'Warren Buffett', 'Buffett']:
            url = "../../people/巴菲特.html"
        elif person in ['查理·芒格', 'Charlie Munger', 'Munger']:
            url = "../../people/芒格.html"
        elif person in ['Gene Abegg', 'Abegg']:
            url = "../../people/吉恩·阿贝格.html"
        elif person in ['Phil Liesche', 'Liesche']:
            url = "../../people/菲尔·利舍.html"
        elif person in ['Ken Chace', 'Chace']:
            url = "../../people/肯·蔡斯.html"
        elif person in ['Chuck Huggins', 'Huggins']:
            url = "../../people/查克·哈金斯.html"
        elif person in ['Graham', '本杰明·格雷厄姆']:
            url = "../../people/格雷厄姆.html"
        elif person in ['Tom Murphy', 'Murphy']:
            url = "../../people/汤姆·墨菲.html"
        elif person in ['Peter Lynch', 'Lynch']:
            url = "../../people/彼得·林奇.html"
        elif person in ['Ajit Jain', 'Ajit']:
            url = "../../people/阿吉特·贾恩.html"
        elif person in ['Lou Simpson', 'Simpson']:
            url = "../../people/路易·辛普森.html"
        elif person in ['Tony Nicely']:
            url = "../../people/托尼·奈斯利.html"
        elif person in ['Ralph Schey', 'Ralph']:
            url = "../../people/拉尔夫·谢伊.html"
        elif person in ['Todd Combs', '托德·库姆斯']:
            url = "../../people/托德·库姆斯.html"
        elif person in ['Greg Abel', '格雷格·阿贝尔']:
            url = "../../people/格雷格·阿贝尔.html"
        elif person in ['Ted Weschler', '泰德·韦施勒']:
            url = "../../people/泰德·韦施勒.html"
        else:
            url = f"../../people/{person}.html"
        
        people_url_map[person] = url
        people_map[person] = url
        
        # 添加别名
        if person == '巴菲特':
            people_map['沃伦·巴菲特'] = url
            people_map['Warren Buffett'] = url
            people_map['Buffett'] = url
        elif person == '查理·芒格':
            people_map['芒格'] = url
            people_map['Charlie Munger'] = url
            people_map['Munger'] = url
        elif person == 'Gene Abegg':
            people_map['Abegg'] = url
            people_map['吉恩·阿贝格'] = url
        elif person == 'Phil Liesche':
            people_map['Liesche'] = url
            people_map['菲尔·利舍'] = url
        elif person == 'Ken Chace':
            people_map['Chace'] = url
            people_map['肯·蔡斯'] = url
        elif person == 'Chuck Huggins':
            people_map['Huggins'] = url
            people_map['查克·哈金斯'] = url
        elif person == 'Graham':
            people_map['本杰明·格雷厄姆'] = url
        elif person == 'Tom Murphy':
            people_map['Murphy'] = url
            people_map['汤姆·墨菲'] = url
        elif person == 'Peter Lynch':
            people_map['Lynch'] = url
            people_map['彼得·林奇'] = url
        elif person == 'Ajit Jain':
            people_map['Ajit'] = url
            people_map['阿吉特·贾恩'] = url
        elif person == 'Lou Simpson':
            people_map['Simpson'] = url
            people_map['路易·辛普森'] = url
    
    return {
        'concept_map': concept_map,
        'company_map': company_map,
        'people_map': people_map,
        'concept_years': dict(concept_years),
        'company_years': dict(company_years),
        'people_years': dict(people_years)
    }


def merge_keyword_maps(mappings):
    """合并所有关键词映射，按长度降序排列"""
    all_keywords = {}
    
    # 优先使用较长的映射（避免短词先匹配）
    for keyword, url in mappings['people_map'].items():
        all_keywords[keyword] = url
    for keyword, url in mappings['company_map'].items():
        if keyword not in all_keywords:
            all_keywords[keyword] = url
    for keyword, url in mappings['concept_map'].items():
        if keyword not in all_keywords:
            all_keywords[keyword] = url
    
    # 按长度降序排序
    sorted_keywords = sorted(all_keywords.keys(), key=len, reverse=True)
    return {k: all_keywords[k] for k in sorted_keywords}


def add_links_to_cn_block(soup, keyword_map, processed_refs=None):
    """使用BeautifulSoup安全地在中文块中添加链接"""
    if processed_refs is None:
        processed_refs = set()
    
    modified = False
    
    for cn_block in soup.find_all('div', class_='lang-cn'):
        # 遍历所有文本节点
        for element in cn_block.find_all(text=True):
            parent = element.parent
            # 跳过已在链接内的文本
            if parent.name == 'a':
                continue
            
            text = str(element)
            new_text = text
            
            # 按关键词长度降序替换
            for keyword in sorted(keyword_map.keys(), key=len, reverse=True):
                # 检查是否已处理过此引用
                ref = f"{id(element)}:{keyword}"
                if ref in processed_refs:
                    continue
                
                if keyword in new_text:
                    url = keyword_map[keyword]
                    # 创建链接标签
                    link_html = f'<a href="{url}" class="concept-link">{keyword}</a>'
                    new_text = new_text.replace(keyword, link_html, 1)
                    processed_refs.add(ref)
                    modified = True
            
            if new_text != text:
                # 用新的HTML替换文本节点
                new_soup = BeautifulSoup(new_text, 'html.parser')
                element.replace_with(new_soup)
    
    return modified


def process_letter_file(filepath, keyword_map):
    """处理单个信件文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 添加链接
    processed_refs = set()
    modified = add_links_to_cn_block(soup, keyword_map, processed_refs)
    
    if modified:
        # 保存修改后的文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False


def generate_backlinks_html(years, base_path):
    """生成反向链接HTML"""
    if not years:
        return ""
    
    # 去重并排序年份
    unique_years = sorted(set(years), reverse=True)
    count = len(unique_years)
    
    links_html = []
    for year in unique_years:
        href = f"../letters/berkshire/{year}.html"
        links_html.append(f'<a href="{href}">{year}年</a>')
    
    return f'''
        <div class="backlinks">
            <h2>📚 反向链接</h2>
            <p class="backlinks-intro">以下年份的信件提到了此概念：</p>
            <div class="backlinks-list">
                {"".join(links_html)}
            </div>
            <p class="backlinks-count">共 {count} 处引用</p>
        </div>
    '''


def update_backlinks_in_page(filepath, backlinks_html, page_type):
    """更新页面中的反向链接部分"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 查找是否已有反向链接部分
    existing_backlinks = soup.find('div', class_='backlinks')
    if existing_backlinks:
        existing_backlinks.decompose()
    
    # 查找footer或main内容的末尾
    footer = soup.find('footer')
    main = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
    
    if backlinks_html:
        backlinks_soup = BeautifulSoup(backlinks_html, 'html.parser')
        if footer:
            footer.insert_before(backlinks_soup)
        elif main:
            main.append(backlinks_soup)
        else:
            soup.body.append(backlinks_soup)
        
        # 保存修改
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return True
    return False


def process_concept_pages(mappings):
    """处理所有概念页面"""
    processed = 0
    
    for concept_file in CONCEPTS_DIR.glob("*.html"):
        concept_name = concept_file.stem
        
        # 查找引用的年份
        years = []
        for concept_key, concept_years in mappings['concept_years'].items():
            if concept_name == concept_key or concept_name in concept_key:
                years.extend(concept_years)
        
        # 也从文件名直接匹配
        if concept_name in mappings['concept_years']:
            years = mappings['concept_years'][concept_name]
        
        backlinks_html = generate_backlinks_html(years, "concepts")
        if update_backlinks_in_page(concept_file, backlinks_html, 'concept'):
            processed += 1
    
    return processed


def process_company_pages(mappings):
    """处理所有公司页面"""
    processed = 0
    
    for company_file in COMPANIES_DIR.glob("*.html"):
        company_name = company_file.stem
        
        # 查找引用的年份
        years = []
        for company_key, company_years in mappings['company_years'].items():
            # 匹配公司名
            if (company_name == company_key or 
                company_name in company_key or
                company_key in company_name):
                years.extend(company_years)
        
        # 从URL别名映射中查找
        for orig_name, years_list in mappings['company_years'].items():
            # 伯克希尔·哈撒韦 <-> 伯克希尔哈撒韦
            if company_name == '伯克希尔哈撒韦' and orig_name in ['伯克希尔·哈撒韦', 'Berkshire Hathaway', 'Berkshire']:
                years.extend(years_list)
            elif company_name == '可口可乐' and orig_name in ['可口可乐', 'Coca-Cola']:
                years.extend(years_list)
            elif company_name == '华盛顿邮报' and orig_name in ['华盛顿邮报', 'Washington Post']:
                years.extend(years_list)
            elif company_name == '美国运通' and orig_name in ['美国运通', 'American Express']:
                years.extend(years_list)
            elif company_name == '吉列' and orig_name in ['吉列', 'Gillette']:
                years.extend(years_list)
            elif company_name == '喜诗糖果' and orig_name in ["喜诗糖果", "See's Candies"]:
                years.extend(years_list)
            elif company_name == '冰雪皇后' and orig_name == '冰雪皇后':
                years.extend(years_list)
            elif company_name == '富国银行' and orig_name in ['富国银行', 'Wells Fargo']:
                years.extend(years_list)
            elif company_name == '通用再保险' and orig_name in ['通用再保险', 'General Re']:
                years.extend(years_list)
            elif company_name == '布法罗新闻' and orig_name in ['布法罗新闻', 'Buffalo News']:
                years.extend(years_list)
            elif company_name == '中美能源' and orig_name in ['中美能源', 'MidAmerican']:
                years.extend(years_list)
        
        backlinks_html = generate_backlinks_html(years, "companies")
        if update_backlinks_in_page(company_file, backlinks_html, 'company'):
            processed += 1
    
    return processed


def process_people_pages(mappings):
    """处理所有人物页面"""
    processed = 0
    
    for people_file in PEOPLE_DIR.glob("*.html"):
        people_name = people_file.stem
        
        # 查找引用的年份
        years = []
        for people_key, people_years in mappings['people_years'].items():
            # 匹配人物名
            if (people_name == people_key or 
                people_name in people_key or
                people_key in people_name):
                years.extend(people_years)
        
        # 从URL别名映射中查找
        for orig_name, years_list in mappings['people_years'].items():
            # 巴菲特
            if people_name == '巴菲特' and orig_name in ['巴菲特', 'Warren Buffett', 'Buffett', '沃伦·巴菲特']:
                years.extend(years_list)
            # 芒格
            elif people_name == '芒格' and orig_name in ['查理·芒格', 'Charlie Munger', 'Munger', '芒格']:
                years.extend(years_list)
            # 吉恩·阿贝格
            elif people_name == '吉恩·阿贝格' and orig_name in ['Gene Abegg', 'Abegg', '吉恩·阿贝格']:
                years.extend(years_list)
            # 菲尔·利舍
            elif people_name == '菲尔·利舍' and orig_name in ['Phil Liesche', 'Liesche', '菲尔·利舍']:
                years.extend(years_list)
            # 肯·蔡斯
            elif people_name == '肯·蔡斯' and orig_name in ['Ken Chace', 'Chace', '肯·蔡斯']:
                years.extend(years_list)
            # 查克·哈金斯
            elif people_name == '查克·哈金斯' and orig_name in ['Chuck Huggins', 'Huggins', '查克·哈金斯']:
                years.extend(years_list)
            # 格雷厄姆
            elif people_name == '格雷厄姆' and orig_name in ['Graham', '本杰明·格雷厄姆']:
                years.extend(years_list)
            # 汤姆·墨菲
            elif people_name == '汤姆·墨菲' and orig_name in ['Tom Murphy', 'Murphy', '汤姆·墨菲']:
                years.extend(years_list)
            # 彼得·林奇
            elif people_name == '彼得·林奇' and orig_name in ['Peter Lynch', 'Lynch', '彼得·林奇']:
                years.extend(years_list)
            # 阿吉特·贾恩
            elif people_name == '阿吉特·贾恩' and orig_name in ['Ajit Jain', 'Ajit', '阿吉特·贾恩']:
                years.extend(years_list)
            # 路易·辛普森
            elif people_name == '路易·辛普森' and orig_name in ['Lou Simpson', 'Simpson', '路易·辛普森']:
                years.extend(years_list)
            # 托尼·奈斯利
            elif people_name == '托尼·奈斯利' and orig_name in ['Tony Nicely', '托尼·奈斯利']:
                years.extend(years_list)
            # 拉尔夫·谢伊
            elif people_name == '拉尔夫·谢伊' and orig_name in ['Ralph Schey', 'Ralph', '拉尔夫·谢伊']:
                years.extend(years_list)
            # 托德·库姆斯
            elif people_name == '托德·库姆斯' and orig_name in ['Todd Combs', '托德·库姆斯']:
                years.extend(years_list)
            # 格雷格·阿贝尔
            elif people_name == '格雷格·阿贝尔' and orig_name in ['Greg Abel', '格雷格·阿贝尔']:
                years.extend(years_list)
            # 泰德·韦施勒
            elif people_name == '泰德·韦施勒' and orig_name in ['Ted Weschler', '泰德·韦施勒']:
                years.extend(years_list)
        
        backlinks_html = generate_backlinks_html(years, "people")
        if update_backlinks_in_page(people_file, backlinks_html, 'people'):
            processed += 1
    
    return processed


def main():
    print("=" * 60)
    print("巴菲特知识库交叉链接生成器")
    print("=" * 60)
    
    # 步骤1: 构建关键词映射
    print("\n[步骤1] 构建关键词映射...")
    mappings = build_keyword_mappings()
    keyword_map = merge_keyword_maps(mappings)
    print(f"  - 概念映射: {len(mappings['concept_map'])} 条")
    print(f"  - 公司映射: {len(mappings['company_map'])} 条")
    print(f"  - 人物映射: {len(mappings['people_map'])} 条")
    print(f"  - 总关键词: {len(keyword_map)} 条")
    
    # 步骤2: 处理信件文件
    print("\n[步骤2] 处理信件文件...")
    letter_files = list(LETTERS_DIR.glob("[0-9]*.html"))
    letter_count = 0
    modified_count = 0
    
    for letter_file in sorted(letter_files):
        letter_count += 1
        if process_letter_file(letter_file, keyword_map):
            modified_count += 1
    
    print(f"  - 处理信件: {letter_count} 封")
    print(f"  - 修改文件: {modified_count} 封")
    
    # 步骤3: 处理概念页面
    print("\n[步骤3] 处理概念页面...")
    concept_count = process_concept_pages(mappings)
    print(f"  - 更新概念页面: {concept_count} 个")
    
    # 步骤4: 处理公司页面
    print("\n[步骤4] 处理公司页面...")
    company_count = process_company_pages(mappings)
    print(f"  - 更新公司页面: {company_count} 个")
    
    # 步骤5: 处理人物页面
    print("\n[步骤5] 处理人物页面...")
    people_count = process_people_pages(mappings)
    print(f"  - 更新人物页面: {people_count} 个")
    
    print("\n" + "=" * 60)
    print("✅ 交叉链接生成完成!")
    print("=" * 60)
    
    return {
        'letters_processed': letter_count,
        'letters_modified': modified_count,
        'concepts_updated': concept_count,
        'companies_updated': company_count,
        'people_updated': people_count
    }


if __name__ == "__main__":
    main()
