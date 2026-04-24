#!/usr/bin/env python3
"""
批量更新页面，添加反向链接部分
"""
import json
import os

# 直接指定完整路径
BASE_PATH = "/app/data/所有对话/主对话/投资研究/知识库/巴菲特知识库-LearnBuffett版"
BACKLINKS_PATH = os.path.join(BASE_PATH, "data", "backlinks.json")

# 读取backlinks数据
with open(BACKLINKS_PATH, 'r', encoding='utf-8') as f:
    backlinks_data = json.load(f)

def get_letter_years(sources):
    """获取按年份排序的信件列表"""
    years = sorted(set(item['year'] for item in sources), reverse=True)
    return years

def generate_backlinks_html(years, entity_type="概念"):
    """生成反向链接HTML"""
    if not years:
        return ""
    
    links_html = ""
    for year in years:
        source = f"letters/berkshire/{year}"
        links_html += f'            <a href="../{source}.html">{year}年致股东信</a>\n'
    
    count = len(years)
    
    html = f'''
        <!-- 反向链接部分 -->
        <div class="backlinks">
            <h2>📚 相关{entity_type}</h2>
            <p class="backlinks-intro">此{entity_type}在以下信件中被提及：</p>
            <div class="backlinks-list">
{links_html}            </div>
            <p class="backlinks-count">共被提及 {count} 次</p>
        </div>
    '''
    return html

def add_backlinks_to_html(content, years, entity_type="概念"):
    """向HTML内容添加反向链接部分"""
    backlinks_html = generate_backlinks_html(years, entity_type)
    
    # 在 </article> 之前插入反向链接
    if '</article>' in content:
        # 检查是否已经有反向链接部分
        if 'class="backlinks"' not in content:
            content = content.replace('</article>', backlinks_html + '\n        </article>')
    
    return content

def add_backlinks_css(content):
    """添加反向链接所需的CSS样式"""
    if '/* 反向链接样式 */' in content:
        return content
    
    css = '''
        /* 反向链接样式 */
        .backlinks {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px dashed var(--gold);
        }
        .backlinks h2 {
            color: var(--navy);
            font-size: 1.3em;
            margin-bottom: 15px;
        }
        .backlinks-intro {
            color: var(--secondary);
            margin-bottom: 15px;
        }
        .backlinks-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .backlinks-list a {
            background: linear-gradient(135deg, var(--light-gold) 0%, #fff9e6 100%);
            border: 1px solid var(--gold);
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            color: var(--navy);
            font-size: 0.9em;
            transition: all 0.3s;
        }
        .backlinks-list a:hover {
            background: var(--gold);
            color: white;
            transform: translateY(-2px);
        }
        .backlinks-count {
            margin-top: 15px;
            color: var(--secondary);
            font-size: 0.9em;
        }
'''
    # 在 </style> 之前添加CSS
    if '</style>' in content:
        content = content.replace('</style>', css + '\n    </style>')
    
    return content

def update_concept_page(md_path, html_path, concept_key, years):
    """更新概念页面（同时更新MD和HTML）"""
    print(f"  更新概念: {concept_key}")
    
    # 更新MD文件
    if os.path.exists(md_path):
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        backlinks_md = '''

---

## 📚 相关信件

此概念在以下信件中被提及：

'''
        for year in years:
            backlinks_md += f'- [{year}年致股东信](../letters/berkshire/{year}.html)\n'
        
        backlinks_md += f'\n共被提及 {len(years)} 次\n'
        
        if '## 📚 相关信件' not in md_content:
            md_content += backlinks_md
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"    ✓ 更新MD文件: {os.path.basename(md_path)}")
    
    # 更新HTML文件
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 添加CSS
        html_content = add_backlinks_css(html_content)
        
        # 添加反向链接
        new_content = add_backlinks_to_html(html_content, years, "概念")
        
        if new_content != html_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    ✓ 更新HTML文件: {os.path.basename(html_path)}")

def update_company_page(html_path, company_key, years):
    """更新公司页面"""
    print(f"  更新公司: {company_key}")
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 添加CSS
        html_content = add_backlinks_css(html_content)
        
        new_content = add_backlinks_to_html(html_content, years, "公司")
        
        if new_content != html_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    ✓ 更新HTML文件: {os.path.basename(html_path)}")

def update_people_page(html_path, people_key, years):
    """更新人物页面"""
    print(f"  更新人物: {people_key}")
    
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 添加CSS
        html_content = add_backlinks_css(html_content)
        
        new_content = add_backlinks_to_html(html_content, years, "人物")
        
        if new_content != html_content:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    ✓ 更新HTML文件: {os.path.basename(html_path)}")

def main():
    print("=" * 60)
    print("开始更新页面，添加反向链接...")
    print("=" * 60)
    
    # 更新概念页面
    print("\n【更新概念页面】")
    concepts_path = os.path.join(BASE_PATH, "concepts")
    for concept_key, sources in backlinks_data.get('concepts', {}).items():
        concept_name = concept_key.replace('concepts/', '')
        md_path = os.path.join(concepts_path, f"{concept_name}.md")
        html_path = os.path.join(concepts_path, f"{concept_name}.html")
        years = get_letter_years(sources)
        update_concept_page(md_path, html_path, concept_key, years)
    
    # 更新公司页面
    print("\n【更新公司页面】")
    companies_path = os.path.join(BASE_PATH, "companies")
    for company_key, sources in backlinks_data.get('companies', {}).items():
        company_name = company_key.replace('companies/', '')
        html_path = os.path.join(companies_path, f"{company_name}.html")
        years = get_letter_years(sources)
        update_company_page(html_path, company_key, years)
    
    # 更新人物页面
    print("\n【更新人物页面】")
    people_path = os.path.join(BASE_PATH, "people")
    for people_key, sources in backlinks_data.get('people', {}).items():
        people_name = people_key.replace('people/', '')
        html_path = os.path.join(people_path, f"{people_name}.html")
        years = get_letter_years(sources)
        update_people_page(html_path, people_key, years)
    
    print("\n" + "=" * 60)
    print("反向链接更新完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
