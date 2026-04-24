#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引用片段提取脚本
从巴菲特致股东信中提取概念关键词的上下文片段
"""

import json
import re
import os
from pathlib import Path
from collections import defaultdict

# 基础路径 - 使用绝对路径
SCRIPT_DIR = Path(__file__).parent.resolve()
BASE_PATH = SCRIPT_DIR
DATA_PATH = BASE_PATH / "data"
LETTERS_PATH = Path("/app/data/所有对话/主对话/投资研究/知识库/buffett-km/english-letters-fixed")
CONCEPTS_PATH = BASE_PATH / "concepts"

# 中文概念到英文关键词的映射
CONCEPT_KEYWORDS = {
    # 高频概念
    "内在价值": ["intrinsic value"],
    "安全边际": ["margin of safety"],
    "护城河": ["economic moat", "moat"],
    "复利": ["compound interest", "compounding"],
    "保险浮存金": ["float", "insurance float"],
    "市值": ["market value", "market capitalization"],
    "竞争优势": ["competitive advantage"],
    "账面价值": ["book value"],
    "通货膨胀": ["inflation"],
    "长期持有": ["hold forever", "hold indefinitely", "never sell", "permanent holding"],
    "股东权益报酬率": ["return on equity", "ROE", "return on net worth"],
    "控股公司": ["holding company"],
    "现金流": ["cash flow", "free cash flow"],
    "分散投资": ["diversification", "diversified"],
    "集中投资": ["concentration", "concentrated holding", "concentrated portfolio"],
    "股票回购": ["stock buyback", "share repurchase", "buyback", "repurchases"],
    "能力圈": ["circle of competence", "circle of competency", "competence"],
    "市场先生": ["Mr. Market"],
    "价值投资": ["value investing", "value investment", "value investor"],
    
    # 中频概念
    "经济商誉": ["economic goodwill", "goodwill"],
    "雪球效应": ["snowball effect", "snowball"],
    "期权": ["option", "options"],
    "可转债": ["convertible", "convertible bond"],
    "优先股": ["preferred stock", "preferred share", "preferred securities"],
    "并购": ["acquisition", "acquisitions", "merge", "merger"],
    "EPS": ["earnings per share", "EPS"],
    "EBITDA": ["EBITDA"],
    "净利润": ["net income", "net profit"],
    "每股收益": ["earnings per share", "EPS"],
    "税前利润": ["pre-tax earnings", "pretax earnings", "pre-tax income"],
    "营业利润": ["operating earnings", "operating profit", "operating income"],
    
    # 低频概念
    "保险业": ["insurance", "insurer"],
    "回购": ["buyback", "repurchase", "stock buyback"],
    "管理层": ["management", "manager", "managerial"],
    "商誉": ["goodwill"],
    "品牌": ["brand", "branding", "brand value"],
    "商业模式": ["business model", "business model"],
    "企业治理": ["corporate governance", "governance"],
    "估值": ["valuation", "value", "valued", "undervalued", "overvalued"],
    "风险管理": ["risk management", "risk"],
    "套利": ["arbitrage"],
    "特许经营权": ["franchise", "franchised business"],
    "媒体与出版": ["media", "publishing", "newspaper"],
    "金融企业": ["financial institution", "bank", "banking"],
    "指数投资": ["index investing", "index fund", "passive investing"],
    "能源": ["energy", "oil", "gas"],
    "航空业": ["airline", "aviation"],
    "衍生品": ["derivative", "derivatives"],
    "诚信": ["integrity", "honesty", "honest"],
    "资本配置": ["capital allocation", "capital deployment"],
    "透视盈余": ["look-through earnings"],
    "通货膨胀": ["inflation", "inflationary"],
    "银行业": ["bank", "banking"],
    "零售与消费": ["retail", "consumer", "retailing"],
    "科技与互联网": ["technology", "internet", "tech"],
    "有效市场": ["efficient market", "efficient-market"],
    "杠杆": ["leverage", "leveraged", "debt"],
    "纺织业务": ["textile", "textile business"],
    "股东导向": ["shareholder oriented", "owner oriented"],
    "税收效率": ["tax efficiency", "tax rate"],
    "股息": ["dividend", "dividends"],
    "债券": ["bond", "bonds", "debt"],
    "科技": ["technology", "tech"],
    "市场预测": ["market forecast", "prediction"],
    "市盈率": ["P/E ratio", "price-earnings", "PE ratio"],
    "承保纪律": ["underwriting discipline", "underwriting"],
    "公司法": ["corporation", "corporate law", "corporate"],
    "float": ["float"],
    "会计商誉": ["accounting goodwill", "goodwill"],
}

# 加载backlinks数据
def load_backlinks():
    with open(DATA_PATH / "backlinks.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 加载信件文件
def load_letter(year):
    letter_file = LETTERS_PATH / f"{year}.txt"
    if letter_file.exists():
        with open(letter_file, "r", encoding="utf-8") as f:
            return f.read()
    return None

# 提取关键词周围的上下文
def clean_context(text):
    """清理上下文文本，去除多余空白"""
    # 先将换行符替换为空格
    text = text.replace('\n', ' ')
    # 将多个空格替换为单个空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_context(text, keywords, context_chars=150):
    """提取关键词周围指定字符数的上下文"""
    results = []
    text_lower = text.lower()
    
    for keyword in keywords:
        pattern = re.escape(keyword.lower())
        for match in re.finditer(pattern, text_lower):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            
            # 提取上下文并清理格式
            context = text[start:end]
            context = clean_context(context)
            
            # 添加省略号
            prefix = "..." if start > 0 else ""
            suffix = "..." if end < len(text) else ""
            
            results.append({
                "keyword": keyword,
                "context": f"{prefix}{context}{suffix}",
                "position": match.start()
            })
    
    # 按位置排序并去重
    seen = set()
    unique_results = []
    for r in sorted(results, key=lambda x: x["position"]):
        if r["context"] not in seen:
            seen.add(r["context"])
            unique_results.append(r)
    
    return unique_results

# 分析信件中的章节（基于标题）
def identify_section(text, position):
    """根据位置识别信件中的章节"""
    # 获取当前位置前的所有章节标题
    before_text = text[:position]
    
    # 匹配常见的章节标题模式
    sections = re.findall(r'^(?:[A-Z][A-Z\s]+|.+:)$', before_text, re.MULTILINE)
    
    if sections:
        # 返回最后一个章节标题
        last_section = sections[-1].strip() if sections else ""
        if len(last_section) < 60:  # 确保是标题而非其他内容
            return last_section
    
    return "投资理念"

# 按年份分组引用
def group_by_year(citations):
    """将引用按年份分组"""
    grouped = defaultdict(list)
    for citation in citations:
        year = citation["year"]
        grouped[year].append(citation)
    return dict(sorted(grouped.items(), reverse=True))

# 生成MD格式的引用片段
def generate_md_citations(concept_name, citations_by_year):
    """生成Markdown格式的引用片段"""
    md = []
    
    total_count = sum(len(v) for v in citations_by_year.values())
    md.append(f"\n## 引用来源（{total_count}处）\n")
    
    for year, citations in citations_by_year.items():
        md.append(f"\n### {year}年\n")
        
        for i, citation in enumerate(citations[:3]):  # 每年最多显示3个片段
            # 添加高亮的关键词
            highlighted = citation["context"]
            for kw in citation.get("keywords", []):
                highlighted = re.sub(
                    rf'\b{re.escape(kw)}\b', 
                    f'**{kw}**', 
                    highlighted, 
                    flags=re.IGNORECASE
                )
            
            section = citation.get("section", "")
            section_label = f"（{section}章节）" if section else ""
            
            md.append(f'> "{highlighted}" {section_label}\n')
        
        if len(citations) > 3:
            md.append(f"> *+还有{len(citations) - 3}处引用*\n")
    
    return "".join(md)

# 生成HTML格式的引用片段
def generate_html_citations(concept_name, citations_by_year):
    """生成HTML格式的引用片段"""
    total_count = sum(len(v) for v in citations_by_year.values())
    
    # 开始标签
    html = f'''<h2>引用来源（{total_count}处）</h2>
<div class="citations-container">
'''
    
    for year, citations in citations_by_year.items():
        html += f'''<div class="citation-year">
<h3>{year}年</h3>
<div class="citation-list">
'''
        
        for citation in citations[:3]:  # 每年最多显示3个片段
            # 高亮关键词并清理文本
            highlighted = clean_for_html(citation["context"])
            for kw in citation.get("keywords", []):
                highlighted = re.sub(
                    rf'\b{re.escape(kw)}\b',
                    f'<span class="highlight">{kw}</span>',
                    highlighted,
                    flags=re.IGNORECASE
                )
            
            section = citation.get("section", "")
            section_label = f'<span class="section-tag">{section}</span>' if section else ''
            
            letter_link = f'../letters/berkshire/{year}.html'
            html += f'''<div class="citation-card">
<blockquote class="citation-text">"{highlighted}"</blockquote>
<div class="citation-meta">{section_label}<a href="{letter_link}" class="citation-link">{year}年致股东信 →</a></div>
</div>
'''
        
        if len(citations) > 3:
            html += f'''<div class="citation-more">
<a href="../letters/berkshire/{year}.html">+ 还有{len(citations) - 3}处引用</a>
</div>
'''
        
        html += '''</div>
</div>
'''
    
    html += '''</div>
'''
    
    return html


def clean_for_html(text):
    """清理文本用于HTML显示"""
    # 先清理换行符和多余空白
    text = clean_context(text)
    # 转义HTML特殊字符
    text = text.replace('\\', '')  # 移除反斜杠
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    return text

# 添加CSS样式
def get_citation_styles():
    return '''
        .citations-container {
            margin: 30px 0;
        }
        .citation-year {
            margin: 25px 0;
        }
        .citation-year h3 {
            color: #1B2A4A;
            font-size: 1.1em;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 1px solid #E5E0D8;
        }
        .citation-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .citation-card {
            background: #F8F5EE;
            border: 1px solid #E5E0D8;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.2s;
        }
        .citation-card:hover {
            border-color: #C9A227;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .citation-text {
            margin: 0 0 15px 0;
            padding: 0;
            font-style: italic;
            color: #2C3E50;
            line-height: 1.7;
        }
        .citation-text .highlight {
            background: #FFF3CD;
            padding: 0 2px;
            border-radius: 2px;
            font-weight: 600;
        }
        .citation-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
        }
        .section-tag {
            background: #E8E4DB;
            color: #5D6D7E;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
        }
        .citation-link {
            color: #1B2A4A;
            text-decoration: none;
            font-weight: 500;
        }
        .citation-link:hover {
            color: #C9A227;
        }
        .citation-more {
            text-align: center;
            padding: 10px;
            background: #F8F5EE;
            border-radius: 8px;
        }
        .citation-more a {
            color: #5D6D7E;
            text-decoration: none;
            font-size: 0.9em;
        }
        .citation-more a:hover {
            color: #C9A227;
        }
    '''

# 处理单个概念
def process_concept(concept_path, concept_name):
    """处理单个概念，提取引用片段并更新文件"""
    print(f"\n处理概念: {concept_name}")
    
    # 获取英文关键词
    keywords = CONCEPT_KEYWORDS.get(concept_name, [])
    if not keywords:
        print(f"  ⚠️  未找到关键词映射，跳过")
        return False
    
    # 加载backlinks
    backlinks = load_backlinks()
    concept_key = f"concepts/{concept_name}"
    
    if concept_key not in backlinks["concepts"]:
        print(f"  ⚠️  未找到反向链接数据，跳过")
        return False
    
    references = backlinks["concepts"][concept_key]
    print(f"  找到 {len(references)} 处引用")
    
    # 收集引用片段
    all_citations = []
    
    for ref in references:
        year = ref["year"]
        source = ref["source"]
        
        # 加载信件
        letter_text = load_letter(year)
        if not letter_text:
            print(f"  ⚠️  未找到 {year} 年信件")
            continue
        
        # 提取引用片段
        contexts = extract_context(letter_text, keywords, context_chars=150)
        
        for ctx in contexts:
            section = identify_section(letter_text, ctx["position"])
            all_citations.append({
                "year": year,
                "context": ctx["context"],
                "keywords": keywords,
                "section": section,
                "source": source
            })
    
    if not all_citations:
        print(f"  ⚠️  未提取到任何引用片段")
        return False
    
    # 按年份分组
    citations_by_year = group_by_year(all_citations)
    
    # 读取现有文件
    md_file = CONCEPTS_PATH / f"{concept_name}.md"
    html_file = CONCEPTS_PATH / f"{concept_name}.html"
    
    # 更新MD文件
    if md_file.exists():
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # 检查是否已有引用来源部分
        if "## 引用来源" in md_content:
            # 替换现有部分
            try:
                pattern = r'\n## 引用来源\([^)]+\)\n.*?(?=\n---|\n## 相关概念|$)'
                new_section = generate_md_citations(concept_name, citations_by_year)
                md_content = re.sub(pattern, new_section, md_content, flags=re.DOTALL)
            except re.error as e:
                print(f"  ⚠️  正则表达式错误: {e}")
                # 如果正则失败，直接追加到文件末尾
                md_content += generate_md_citations(concept_name, citations_by_year)
        else:
            # 添加新部分
            md_content += generate_md_citations(concept_name, citations_by_year)
        
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"  ✓ 更新MD文件: {md_file}")
    
    # 更新HTML文件
    if html_file.exists():
        with open(html_file, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 添加CSS样式
        if ".citation-card {" not in html_content:
            style_tag = "</style>"
            html_content = html_content.replace(
                style_tag,
                get_citation_styles() + "\n        " + style_tag
            )
        
        # 生成新的引用部分
        new_citations_html = generate_html_citations(concept_name, citations_by_year)
        
        # 删除所有旧的引用来源部分（包括重复的）
        # 方法：找到第一个<h2>引用来源，然后删除到最后一个</article>之前
        h2_pattern = r'<h2>引用来源'
        h2_matches = list(re.finditer(h2_pattern, html_content))
        
        if h2_matches:
            # 找到第一个<h2>引用来源的位置
            first_h2_pos = h2_matches[0].start()
            # 找到</footer>的位置
            footer_pos = html_content.find('<footer')
            if footer_pos > 0:
                # 保留<h2>引用来源之前的内容和footer之后的内容
                before_content = html_content[:first_h2_pos]
                footer_content = html_content[footer_pos:]
                html_content = before_content + '\n    </article>\n' + footer_content
        
        # 在</article>前添加新的引用来源
        html_content = html_content.replace(
            "</article>",
            new_citations_html + "\n    </article>"
        )
        
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  ✓ 更新HTML文件: {html_file}")
    
    return True

# 主函数
def main():
    print("=" * 60)
    print("开始提取引用片段...")
    print("=" * 60)
    
    # 从backlinks.json获取所有概念
    backlinks = load_backlinks()
    all_concepts = list(backlinks["concepts"].keys())
    
    # 提取概念名称（去掉 "concepts/" 前缀）
    concept_names = [c.replace("concepts/", "") for c in all_concepts]
    
    success_count = 0
    skip_count = 0
    
    for concept_name in concept_names:
        # 检查是否有关键词映射
        if concept_name not in CONCEPT_KEYWORDS:
            print(f"\n处理概念: {concept_name}")
            print(f"  ⚠️  未配置关键词映射，跳过")
            skip_count += 1
            continue
            
        if process_concept(f"concepts/{concept_name}", concept_name):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"处理完成！成功处理 {success_count} 个概念")
    print(f"跳过 {skip_count} 个概念（无关键词映射）")
    print("=" * 60)

if __name__ == "__main__":
    main()
