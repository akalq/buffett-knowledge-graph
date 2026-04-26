#!/usr/bin/env python3
"""
巴菲特知识库交叉链接脚本 v3
为信件中的概念/公司/人物添加链接，并在目标页面添加反向链接
使用精确的正则表达式处理，避免重复链接和HTML破坏
"""

import os
import json
import re
from pathlib import Path
from collections import defaultdict

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
        url = f"../../concepts/{concept}.html"
        concept_map[concept] = url
    
    # 公司映射（处理中英文别名）
    company_url_mapping = {
        'Berkshire Hathaway': '../../companies/伯克希尔哈撒韦.html',
        '伯克希尔·哈撒韦': '../../companies/伯克希尔哈撒韦.html',
        'Coca-Cola': '../../companies/可口可乐.html',
        '可口可乐': '../../companies/可口可乐.html',
        '可口可乐公司': '../../companies/可口可乐.html',
        'Washington Post': '../../companies/华盛顿邮报.html',
        '华盛顿邮报': '../../companies/华盛顿邮报.html',
        'American Express': '../../companies/美国运通.html',
        '美国运通': '../../companies/美国运通.html',
        'GEICO': '../../companies/GEICO.html',
        'GEICO保险': '../../companies/GEICO.html',
        'Wells Fargo': '../../companies/富国银行.html',
        '富国银行': '../../companies/富国银行.html',
        "See's Candies": '../../companies/喜诗糖果.html',
        '喜诗糖果': '../../companies/喜诗糖果.html',
        'Gillette': '../../companies/吉列.html',
        '吉列': '../../companies/吉列.html',
        'General Re': '../../companies/通用再保险.html',
        '通用再保险': '../../companies/通用再保险.html',
        'Buffalo News': '../../companies/布法罗新闻.html',
        '布法罗新闻': '../../companies/布法罗新闻.html',
        'Nebraska Furniture Mart': '../../companies/内布拉斯加家具店.html',
        '内布拉斯加家具店': '../../companies/内布拉斯加家具店.html',
        'NFM': '../../companies/内布拉斯加家具店.html',
        'MidAmerican': '../../companies/中美能源.html',
        '中美能源': '../../companies/中美能源.html',
        'IBM': '../../companies/IBM.html',
        'IBM公司': '../../companies/IBM.html',
        '冰雪皇后': '../../companies/冰雪皇后.html',
        '宝洁': '../../companies/宝洁.html',
        '沃尔玛': '../../companies/沃尔玛.html',
        'Target': '../../companies/Target.html',
    }
    
    for company in all_companies:
        if company in company_url_mapping:
            url = company_url_mapping[company]
        else:
            url = f"../../companies/{company}.html"
        company_map[company] = url
    
    # 人物映射
    people_url_mapping = {
        '巴菲特': '../../people/巴菲特.html',
        '沃伦·巴菲特': '../../people/巴菲特.html',
        'Warren Buffett': '../../people/巴菲特.html',
        'Buffett': '../../people/巴菲特.html',
        '查理·芒格': '../../people/芒格.html',
        '芒格': '../../people/芒格.html',
        'Charlie Munger': '../../people/芒格.html',
        'Munger': '../../people/芒格.html',
        'Gene Abegg': '../../people/吉恩·阿贝格.html',
        'Abegg': '../../people/吉恩·阿贝格.html',
        '吉恩·阿贝格': '../../people/吉恩·阿贝格.html',
        'Phil Liesche': '../../people/菲尔·利舍.html',
        'Liesche': '../../people/菲尔·利舍.html',
        '菲尔·利舍': '../../people/菲尔·利舍.html',
        'Ken Chace': '../../people/肯·蔡斯.html',
        'Chace': '../../people/肯·蔡斯.html',
        '肯·蔡斯': '../../people/肯·蔡斯.html',
        'Chuck Huggins': '../../people/查克·哈金斯.html',
        'Huggins': '../../people/查克·哈金斯.html',
        '查克·哈金斯': '../../people/查克·哈金斯.html',
        'Graham': '../../people/格雷厄姆.html',
        '本杰明·格雷厄姆': '../../people/格雷厄姆.html',
        'Tom Murphy': '../../people/汤姆·墨菲.html',
        'Murphy': '../../people/汤姆·墨菲.html',
        '汤姆·墨菲': '../../people/汤姆·墨菲.html',
        'Peter Lynch': '../../people/彼得·林奇.html',
        'Lynch': '../../people/彼得·林奇.html',
        '彼得·林奇': '../../people/彼得·林奇.html',
        'Ajit Jain': '../../people/阿吉特·贾恩.html',
        'Ajit': '../../people/阿吉特·贾恩.html',
        '阿吉特·贾恩': '../../people/阿吉特·贾恩.html',
        'Lou Simpson': '../../people/路易·辛普森.html',
        'Simpson': '../../people/路易·辛普森.html',
        '路易·辛普森': '../../people/路易·辛普森.html',
        'Tony Nicely': '../../people/托尼·奈斯利.html',
        '托尼·奈斯利': '../../people/托尼·奈斯利.html',
        'Ralph Schey': '../../people/拉尔夫·谢伊.html',
        'Ralph': '../../people/拉尔夫·谢伊.html',
        '拉尔夫·谢伊': '../../people/拉尔夫·谢伊.html',
        'Todd Combs': '../../people/托德·库姆斯.html',
        '托德·库姆斯': '../../people/托德·库姆斯.html',
        'Greg Abel': '../../people/格雷格·阿贝尔.html',
        '格雷格·阿贝尔': '../../people/格雷格·阿贝尔.html',
        'Ted Weschler': '../../people/泰德·韦施勒.html',
        '泰德·韦施勒': '../../people/泰德·韦施勒.html',
    }
    
    for person in all_people:
        if person in people_url_mapping:
            url = people_url_mapping[person]
        else:
            url = f"../../people/{person}.html"
        people_map[person] = url
    
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


def add_links_safe(text, keyword_map):
    """
    安全地在文本中添加链接
    使用贪婪匹配避免子串重复链接
    """
    # 按关键词长度降序排列
    sorted_keywords = sorted(keyword_map.keys(), key=len, reverse=True)
    
    # 构建正则表达式，按长度降序匹配
    # 使用括号捕获关键词
    patterns = []
    for keyword in sorted_keywords:
        url = keyword_map[keyword]
        # 转义特殊字符
        escaped_keyword = re.escape(keyword)
        patterns.append((escaped_keyword, keyword, url))
    
    # 从长到短依次处理
    for escaped_pattern, original_keyword, url in patterns:
        # 查找所有匹配
        for match in re.finditer(escaped_pattern, text):
            start, end = match.start(), match.end()
            matched_text = match.group()
            
            # 检查是否已经在链接中（向后查看是否有未闭合的<a>标签）
            before = text[:start]
            after = text[end:]
            
            # 简单检查：如果前面最近的开标签没有闭合，跳过
            open_count = len(re.findall(r'<a\b[^>]*>', before))
            close_count = len(re.findall(r'</a>', before))
            if open_count > close_count:
                continue
            
            # 检查匹配位置周围是否有链接标签边界
            # 确保不是在链接内部
            segment = text[max(0, start-10):min(len(text), end+10)]
            if re.search(r'<a\b[^>]*>[^<]*$', before) or re.search(r'^[^<]*</a>', after):
                continue
            
            # 替换为链接
            link = f'<a href="{url}" class="concept-link">{matched_text}</a>'
            text = text[:start] + link + text[end:]
            
            # 由于替换改变了文本长度，需要调整end之后的位置
            # 更简单的方法：只处理第一个匹配，然后重新开始
            # 但这可能导致长关键词内部的短词无法匹配
            # 更好的做法是构建一个更复杂的正则
            
    return text


def add_links_single_pass(text, keyword_map):
    """
    单次遍历完成所有链接替换
    避免子串重复匹配的问题
    """
    # 按关键词长度降序排列
    sorted_keywords = sorted(keyword_map.keys(), key=len, reverse=True)
    
    result = []
    i = 0
    text_len = len(text)
    
    while i < text_len:
        matched = False
        
        for keyword in sorted_keywords:
            url = keyword_map[keyword]
            keyword_len = len(keyword)
            
            # 检查文本片段是否匹配关键词
            if text[i:i+keyword_len] == keyword:
                # 检查是否在链接标签内部
                before = text[:i]
                open_count = len(re.findall(r'<a\b[^>]*>', before))
                close_count = len(re.findall(r'</a>', before))
                
                if open_count > close_count:
                    # 在链接内部，跳过
                    i += 1
                    matched = True
                    break
                
                # 检查链接标签的完整性
                # 如果前面有未闭合的 <a> 标签
                last_open = before.rfind('<a ')
                last_close = before.rfind('</a>')
                
                if last_open > last_close:
                    i += 1
                    matched = True
                    break
                
                # 替换
                result.append(f'<a href="{url}" class="concept-link">{keyword}</a>')
                i += keyword_len
                matched = True
                break
        
        if not matched:
            result.append(text[i])
            i += 1
    
    return ''.join(result)


def process_letter_file_regex(filepath, keyword_map):
    """处理信件文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 只处理 <div class="lang-block lang-cn"> 块
    pattern = r'(<div class="lang-block lang-cn"[^>]*>.*?</div>)'
    
    def process_cn_block(match):
        block = match.group(1)
        # 只处理 blockquote 内的中文文本
        blockquote_pattern = r'(<blockquote>)(.*?)(</blockquote>)'
        
        def process_blockquote(m):
            open_tag, text, close_tag = m.group(1), m.group(2), m.group(3)
            # 处理文本内容
            new_text = add_links_single_pass(text, keyword_map)
            return open_tag + new_text + close_tag
        
        new_block = re.sub(blockquote_pattern, process_blockquote, block, flags=re.DOTALL)
        return new_block
    
    new_content = re.sub(pattern, process_cn_block, content, flags=re.DOTALL)
    
    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def generate_backlinks_html(years, page_type):
    """生成反向链接HTML"""
    if not years:
        return ""
    
    # 去重并排序年份
    unique_years = sorted(set(years), reverse=True)
    count = len(unique_years)
    
    # 根据页面类型设置说明文字
    intro_texts = {
        'concept': '以下年份的信件提到了此概念：',
        'company': '以下年份的信件提到了此公司：',
        'people': '以下年份的信件提到了此人物：'
    }
    intro = intro_texts.get(page_type, '以下年份的信件提到了此条目：')
    
    links_html = []
    for year in unique_years:
        href = f"../letters/berkshire/{year}.html"
        links_html.append(f'<a href="{href}">{year}年</a>')
    
    return f'''
        <div class="backlinks">
            <h2>📚 反向链接</h2>
            <p class="backlinks-intro">{intro}</p>
            <div class="backlinks-list">
                {"".join(links_html)}
            </div>
            <p class="backlinks-count">共 {count} 处引用</p>
        </div>
    '''


def update_backlinks_in_page(filepath, backlinks_html):
    """更新页面中的反向链接部分"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已有反向链接部分
    if 'class="backlinks"' in content:
        # 移除旧的反向链接
        pattern = r'\s*<div class="backlinks">.*?</div>\s*'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    if backlinks_html:
        # 找到 footer 或 body 的末尾，插入反向链接
        footer_match = re.search(r'(</footer>)', content)
        if footer_match:
            insert_pos = footer_match.start()
            content = content[:insert_pos] + backlinks_html + '\n' + content[insert_pos:]
        else:
            # 如果没有 footer，添加到 </body> 前
            body_match = re.search(r'(</body>)', content)
            if body_match:
                insert_pos = body_match.start()
                content = content[:insert_pos] + backlinks_html + '\n' + content[insert_pos:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def get_years_for_concept(concept_name, concept_years):
    """获取概念引用的年份"""
    years = []
    
    # 精确匹配
    if concept_name in concept_years:
        years.extend(concept_years[concept_name])
    
    # 部分匹配
    for key, vals in concept_years.items():
        if concept_name in key or key in concept_name:
            years.extend(vals)
    
    return list(set(years))


def get_years_for_company(company_name, company_years):
    """获取公司引用的年份"""
    years = []
    
    # 精确匹配
    if company_name in company_years:
        years.extend(company_years[company_name])
    
    # URL别名映射
    alias_map = {
        '伯克希尔哈撒韦': ['伯克希尔·哈撒韦', 'Berkshire Hathaway', 'Berkshire'],
        '可口可乐': ['可口可乐', 'Coca-Cola'],
        '华盛顿邮报': ['华盛顿邮报', 'Washington Post'],
        '美国运通': ['美国运通', 'American Express'],
        '吉列': ['吉列', 'Gillette'],
        '喜诗糖果': ['喜诗糖果', "See's Candies"],
        '冰雪皇后': ['冰雪皇后'],
        '富国银行': ['富国银行', 'Wells Fargo'],
        '通用再保险': ['通用再保险', 'General Re'],
        '布法罗新闻': ['布法罗新闻', 'Buffalo News'],
        '中美能源': ['中美能源', 'MidAmerican'],
    }
    
    for url_name, aliases in alias_map.items():
        if company_name == url_name:
            for alias in aliases:
                if alias in company_years:
                    years.extend(company_years[alias])
    
    return list(set(years))


def get_years_for_people(people_name, people_years):
    """获取人物引用的年份"""
    years = []
    
    # 精确匹配
    if people_name in people_years:
        years.extend(people_years[people_name])
    
    # URL别名映射
    alias_map = {
        '巴菲特': ['巴菲特', 'Warren Buffett', 'Buffett', '沃伦·巴菲特'],
        '芒格': ['查理·芒格', 'Charlie Munger', 'Munger', '芒格'],
        '吉恩·阿贝格': ['Gene Abegg', 'Abegg', '吉恩·阿贝格'],
        '菲尔·利舍': ['Phil Liesche', 'Liesche', '菲尔·利舍'],
        '肯·蔡斯': ['Ken Chace', 'Chace', '肯·蔡斯'],
        '查克·哈金斯': ['Chuck Huggins', 'Huggins', '查克·哈金斯'],
        '格雷厄姆': ['Graham', '本杰明·格雷厄姆'],
        '汤姆·墨菲': ['Tom Murphy', 'Murphy', '汤姆·墨菲'],
        '彼得·林奇': ['Peter Lynch', 'Lynch', '彼得·林奇'],
        '阿吉特·贾恩': ['Ajit Jain', 'Ajit', '阿吉特·贾恩'],
        '路易·辛普森': ['Lou Simpson', 'Simpson', '路易·辛普森'],
        '托尼·奈斯利': ['Tony Nicely', '托尼·奈斯利'],
        '拉尔夫·谢伊': ['Ralph Schey', 'Ralph', '拉尔夫·谢伊'],
        '托德·库姆斯': ['Todd Combs', '托德·库姆斯'],
        '格雷格·阿贝尔': ['Greg Abel', '格雷格·阿贝尔'],
        '泰德·韦施勒': ['Ted Weschler', '泰德·韦施勒'],
    }
    
    for url_name, aliases in alias_map.items():
        if people_name == url_name:
            for alias in aliases:
                if alias in people_years:
                    years.extend(people_years[alias])
    
    return list(set(years))


def process_concept_pages(mappings):
    """处理所有概念页面"""
    processed = 0
    
    for concept_file in CONCEPTS_DIR.glob("*.html"):
        concept_name = concept_file.stem
        years = get_years_for_concept(concept_name, mappings['concept_years'])
        
        backlinks_html = generate_backlinks_html(years, 'concept')
        if update_backlinks_in_page(concept_file, backlinks_html):
            processed += 1
    
    return processed


def process_company_pages(mappings):
    """处理所有公司页面"""
    processed = 0
    
    for company_file in COMPANIES_DIR.glob("*.html"):
        company_name = company_file.stem
        years = get_years_for_company(company_name, mappings['company_years'])
        
        backlinks_html = generate_backlinks_html(years, 'company')
        if update_backlinks_in_page(company_file, backlinks_html):
            processed += 1
    
    return processed


def process_people_pages(mappings):
    """处理所有人物页面"""
    processed = 0
    
    for people_file in PEOPLE_DIR.glob("*.html"):
        people_name = people_file.stem
        years = get_years_for_people(people_name, mappings['people_years'])
        
        backlinks_html = generate_backlinks_html(years, 'people')
        if update_backlinks_in_page(people_file, backlinks_html):
            processed += 1
    
    return processed


def main():
    print("=" * 60)
    print("巴菲特知识库交叉链接生成器 v3")
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
        if process_letter_file_regex(letter_file, keyword_map):
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
