#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成巴菲特公司投资案例页面
"""

# 模板文件 - 基于已完成的新格式
TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 巴菲特投资案例</title>
    <style>
        :root { --navy: #1B2A4A; --gold: #C9A227; --cream: #F8F5EE; --secondary: #5D6D7E; --border: #E5E0D8; --light-gold: #F5ECD7; }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Noto Serif SC', Georgia, serif; background: #FFFEF9; color: #2C3E50; line-height: 1.9; }
        .container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
        header { background: linear-gradient(135deg, var(--navy) 0%, #2a3f6a 100%); color: white; padding: 50px 30px; text-align: center; border-radius: 15px; margin-bottom: 30px; }
        header h1 { font-size: 2.2em; margin-bottom: 8px; }
        .en-name { color: rgba(255,255,255,0.7); font-size: 1.1em; }
        .meta { color: var(--gold); margin-top: 15px; }
        .meta span { background: rgba(201, 162, 39, 0.2); padding: 5px 15px; border-radius: 20px; }
        .nav { background: white; border: 1px solid var(--border); padding: 15px 25px; margin-bottom: 30px; border-radius: 10px; text-align: center; }
        .nav a { color: var(--navy); text-decoration: none; margin: 0 15px; padding: 8px 15px; border-radius: 5px; transition: all 0.2s; }
        .nav a:hover { background: var(--gold); color: white; }
        .content { background: white; border: 1px solid var(--border); border-radius: 15px; padding: 40px; }
        .section { margin-bottom: 40px; padding-bottom: 35px; border-bottom: 1px solid var(--border); }
        .section:last-child { border-bottom: none; margin-bottom: 0; }
        h2 { color: var(--navy); font-size: 1.4em; margin: 0 0 20px; padding-bottom: 10px; border-bottom: 3px solid var(--gold); display: inline-block; }
        .overview-card { background: linear-gradient(135deg, var(--navy) 0%, #2C3E50 100%); color: white; padding: 25px; border-radius: 12px; margin: 20px 0; }
        .overview-summary { font-size: 1.15em; margin-bottom: 15px; line-height: 1.6; }
        .overview-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-top: 15px; }
        .stat-item { text-align: center; background: rgba(255,255,255,0.1); padding: 12px; border-radius: 8px; }
        .stat-value { font-size: 1.4em; font-weight: 600; color: var(--gold); }
        .stat-label { font-size: 0.8em; opacity: 0.8; }
        .logic-point { display: flex; margin: 18px 0; padding: 18px; background: var(--cream); border-radius: 10px; }
        .logic-number { font-size: 1.6em; font-weight: 700; color: var(--gold); margin-right: 18px; min-width: 35px; }
        .logic-content { flex: 1; }
        .logic-title { font-weight: 600; color: var(--navy); margin-bottom: 6px; font-size: 1.05em; }
        .logic-desc { color: #555; font-size: 0.95em; }
        .cognition-timeline { position: relative; padding-left: 35px; margin: 20px 0; }
        .cognition-timeline::before { content: ''; position: absolute; left: 8px; top: 0; bottom: 0; width: 3px; background: var(--gold); }
        .cognition-point { position: relative; margin-bottom: 28px; padding-left: 25px; }
        .cognition-point::before { content: ''; position: absolute; left: -30px; top: 6px; width: 14px; height: 14px; border-radius: 50%; background: var(--gold); border: 3px solid white; box-shadow: 0 0 0 3px var(--gold); }
        .cognition-year { font-weight: 700; color: var(--gold); font-size: 1.1em; }
        .cognition-shift { background: var(--light-gold); padding: 8px 15px; border-radius: 6px; margin: 8px 0; font-size: 0.9em; }
        .cognition-shift strong { color: var(--navy); }
        .data-compare { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
        .data-card { background: var(--cream); padding: 20px; border-radius: 10px; }
        .data-card h4 { color: var(--navy); margin-bottom: 12px; font-size: 1em; }
        .data-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed var(--border); }
        .data-row:last-child { border-bottom: none; }
        .data-label { color: var(--secondary); font-size: 0.9em; }
        .data-value { font-weight: 600; color: var(--navy); }
        .lesson-card { background: var(--cream); border-left: 5px solid var(--gold); padding: 22px; margin: 20px 0; border-radius: 0 10px 10px 0; }
        .lesson-title { font-weight: 600; color: var(--navy); margin-bottom: 10px; font-size: 1.05em; }
        .lesson-desc { color: #555; font-size: 0.95em; }
        .quote { background: var(--navy); color: white; padding: 22px 28px; border-left: 5px solid var(--gold); margin: 20px 0; border-radius: 0 12px 12px 0; position: relative; }
        .quote::before { content: '"'; position: absolute; top: 8px; left: 12px; font-size: 3.5em; color: var(--gold); opacity: 0.3; }
        .quote p { margin: 0; font-style: italic; font-size: 1.02em; padding-left: 28px; }
        .quote footer { color: var(--gold); margin-top: 12px; font-size: 0.9em; padding-left: 28px; font-style: normal; }
        .related-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 15px 0; }
        .related-item { background: var(--cream); padding: 14px; border-radius: 8px; text-decoration: none; color: var(--navy); transition: all 0.3s; text-align: center; font-size: 0.95em; }
        .related-item:hover { background: var(--gold); color: white; transform: translateY(-2px); }
        footer { text-align: center; padding: 35px 20px; color: var(--secondary); border-top: 1px solid var(--border); margin-top: 35px; }
        footer a { color: var(--navy); text-decoration: none; }
        @media (max-width: 768px) { .container { padding: 20px 15px; } header { padding: 30px 20px; } header h1 { font-size: 1.7em; } .content { padding: 25px 18px; } .overview-stats { grid-template-columns: repeat(2, 1fr); } .data-compare { grid-template-columns: 1fr; } }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <h1>{icon} {title}</h1>
            <div class="en-name">{en_name}</div>
            <div class="meta"><span>{category}</span></div>
        </header>
        
        <nav class="nav">
            <a href="../index.html">🏠 首页</a>
            <a href="../index-pages/公司索引.html">🏢 公司索引</a>
            <a href="../index-pages/核心思想索引.html">💡 核心思想</a>
        </nav>
        
        <article class="content">
            <div class="overview-card">
                <div class="overview-summary">
                    <strong>{summary}</strong>
                </div>
                <div class="overview-stats">
{stats}
                </div>
            </div>
            
            <div class="section">
                <h2>投资逻辑</h2>
{logic}
            </div>
            
            <div class="section">
                <h2>认知演进</h2>
                <div class="cognition-timeline">
{cognition}
                </div>
            </div>
            
            <div class="section">
                <h2>关键数据</h2>
                <div class="data-compare">
                    <div class="data-card">
                        <h4>📊 基本信息</h4>
{data1}
                    </div>
                    <div class="data-card">
                        <h4>📈 运营特征</h4>
{data2}
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>经验教训</h2>
{lessons}
            </div>
            
            <div class="section">
                <h2>精华原话</h2>
{quotes}
            </div>
            
            <div class="section">
                <h2>相关概念</h2>
                <div class="related-grid">
{related}
                </div>
            </div>
        </article>
        
        <footer>
            <p><a href="../index.html">巴菲特知识库</a> | 数据来源：Berkshire Hathaway Letters</p>
        </footer>
    </div>
</body>
</html>'''

def create_page(data):
    """根据数据生成HTML页面"""
    
    # 统计数据
    stats_html = ""
    for stat in data.get('stats', []):
        stats_html += f'''                    <div class="stat-item">
                        <div class="stat-value">{stat['value']}</div>
                        <div class="stat-label">{stat['label']}</div>
                    </div>
'''
    
    # 投资逻辑
    logic_html = ""
    for i, logic in enumerate(data.get('logic', []), 1):
        logic_html += f'''
                <div class="logic-point">
                    <div class="logic-number">{i}</div>
                    <div class="logic-content">
                        <div class="logic-title">{logic['title']}</div>
                        <div class="logic-desc">{logic['desc']}</div>
                    </div>
                </div>
'''
    
    # 认知演进
    cognition_html = ""
    for cog in data.get('cognition', []):
        cognition_html += f'''
                    <div class="cognition-point">
                        <span class="cognition-year">{cog['year']}</span>
                        <div class="cognition-shift"><strong>从</strong> {cog['from']} <strong>到</strong> {cog['to']}</div>
                        <p>{cog['desc']}</p>
                    </div>
'''
    
    # 关键数据
    data1_html = ""
    for d in data.get('data1', []):
        data1_html += f'''                        <div class="data-row"><span class="data-label">{d['label']}</span><span class="data-value">{d['value']}</span></div>
'''
    
    data2_html = ""
    for d in data.get('data2', []):
        data2_html += f'''                        <div class="data-row"><span class="data-label">{d['label']}</span><span class="data-value">{d['value']}</span></div>
'''
    
    # 经验教训
    lessons_html = ""
    for lesson in data.get('lessons', []):
        lessons_html += f'''
                <div class="lesson-card">
                    <div class="lesson-title">{lesson['title']}</div>
                    <div class="lesson-desc">{lesson['desc']}</div>
                </div>
'''
    
    # 精华原话
    quotes_html = ""
    for q in data.get('quotes', []):
        quotes_html += f'''
                <div class="quote">
                    <p>{q['text']}</p>
                    <footer>—— {q['source']}</footer>
                </div>
'''
    
    # 相关概念
    related_html = ""
    for r in data.get('related', []):
        related_html += f'''                    <a href="../concepts/{r['file']}" class="related-item">{r['icon']} {r['name']}</a>
'''
    
    # 填充模板
    page = TEMPLATE.format(
        title=data['title'],
        icon=data.get('icon', '🏢'),
        en_name=data.get('en_name', ''),
        category=data.get('category', '公司'),
        summary=data['summary'],
        stats=stats_html,
        logic=logic_html,
        cognition=cognition_html,
        data1=data1_html,
        data2=data2_html,
        lessons=lessons_html,
        quotes=quotes_html,
        related=related_html
    )
    
    return page

# 公司数据定义
COMPANIES = {
    '德克斯特鞋业': {
        'title': '德克斯特鞋业',
        'en_name': 'Dexter Shoe',
        'category': '制造业 · 失败案例',
        'icon': '❌',
        'summary': '1993年以4.33亿美元收购的鞋业公司，最终价值归零——这是巴菲特承认的"最糟糕的投资错误"之一。他用伯克希尔股票支付，导致成本被放大到超60亿美元。',
        'stats': [
            {'value': '1993', 'label': '收购年份'},
            {'value': '$4.33亿', 'label': '收购价格'},
            {'value': '≈$0', 'label': '最终价值'},
            {'value': '致命', 'label': '错误等级'},
        ],
        'logic': [
            {'title': '"护城河"误判', 'desc': '巴菲特认为鞋业存在品牌护城河，但忽视了制造业向海外转移的趋势。这种"局部的竞争优势"在行业结构性变革面前不堪一击。'},
            {'title': '用股票支付放大了错误', 'desc': '用伯克希尔A类股支付（25,203股），这些股票在2016年价值超60亿美元。错误的不仅是业务估值，而是整个资本配置决策。'},
            {'title': '国内制造的固执', 'desc': '坚持在美国国内保持生产设施，导致成本远高于竞争对手。在全球化时代，这种"本土情怀"代价惨重。'},
            {'title': '管理层能力不是护城河', 'desc': 'Dexter的管理层同样优秀，但这不能弥补行业本身的夕阳属性。好的管理层救不了夕阳行业。'},
            {'title': '沉没成本谬误', 'desc': '巴菲特承认自己"拖延"了必要的变革，加剧了损失。承认错误并快速行动的勇气至关重要。'},
        ],
        'cognition': [
            {'year': '1993：收购完成', 'from': '"稳健的制造业"', 'to': '噩梦的开始', 'desc': '以4.33亿美元收购Dexter，巴菲特当时认为这是一家有持久竞争优势的企业。'},
            {'year': '1999-2001：问题暴露', 'from': '利润下滑', 'to': '巨额亏损', 'desc': '鞋业开始巨额亏损，H.H. Brown和Justin的利润被Dexter的亏损淹没。2001年亏损达4620万美元。'},
            {'year': '2002：艰难转型', 'from': '危机应对', 'to': '止血成功', 'desc': '在Frank Rooney和Jim Issler的努力下，Dexter业务最终扭亏为盈，但价值已大幅缩水。'},
            {'year': '2007/2016：深度反思', 'from': '自我辩护', 'to': '公开认错', 'desc': '巴菲特多次公开承认这是他最糟糕的错误："我使用股票支付，让这个错误变得极其严重。"'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '1993年11月'},
            {'label': '收购价格', 'value': '4.33亿美元'},
            {'label': '支付方式', 'value': '伯克希尔A类股'},
            {'label': '最终结局', 'value': '价值基本归零'},
        ],
        'data2': [
            {'label': '核心问题', 'value': '国内制造成本过高'},
            {'label': '行业趋势', 'value': '制造业向海外转移'},
            {'label': '机会成本', 'value': '60亿美元（股票增值）'},
            {'label': '教训类型', 'value': '护城河误判+支付方式'},
        ],
        'lessons': [
            {'title': '💡 行业结构决定命运', 'desc': 'Dexter案例最重要的教训是：个体企业的优秀无法对抗行业结构性衰退。当整个行业向低成本地区转移时，坚持本土制造是致命的。巴菲特说："我们试图在美国工厂保持大部分生产，这让我们付出了惨重代价。"'},
            {'title': '💡 用股票支付是双重风险', 'desc': '用伯克希尔股票支付收购，使损失被放大数倍。如果当时用现金，损失是4.33亿；但用股票支付，实际机会成本超过60亿美元。股票价格越高，用它支付的代价就越大。'},
            {'title': '💡 承认错误的勇气', 'desc': '巴菲特在2001年说："我犯了三个伤害你们的决定：1）首先收购它；2）用股票支付；3）拖延变革。"公开承认错误而非推卸责任，体现了真正的领导力。'},
            {'title': '💡 护城河需要持续验证', 'desc': '1993年的Dexter看似有护城河，但这个护城河建立在劳动力成本可控的假设上。当这个假设被打破，护城河就消失了。投资者需要不断重新评估护城河的持久性。'},
        ],
        'quotes': [
            {'text': '我用伯克希尔的股票支付了这场灾难性的收购——那些股票在2016年底价值超过60亿美元。这一举动使伯克希尔的损失变得极其严重。', 'source': '2016年致股东信'},
            {'text': '我做了三个伤害你们在Dexter的决策：1）首先买下它；2）用股票支付；3）当业务需要变革时，我拖延了。我愿意把这些错误归咎于查理（或任何人）。', 'source': '2001年致股东信'},
            {'text': '大约在2001年，我们的鞋类业务损失了4620万美元（税前）。我做出了三个与Dexter相关的决定，严重地伤害了大家。', 'source': '2001年致股东信'},
            {'text': '我明确在为Dexter支付的问题上犯了错误。2010年和2011年我们将面临又一个非常艰难的年份，因为我们正在业务方式上进行重大变革。', 'source': '2000年致股东信'},
        ],
        'related': [
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '资本配置.html', 'icon': '⚙️', 'name': '资本配置'},
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '错误教训.html', 'icon': '📝', 'name': '错误教训'},
        ],
    },
    
    '所罗门': {
        'title': '所罗门公司',
        'en_name': 'Salomon Inc',
        'category': '金融 · 危机处理',
        'icon': '⚖️',
        'summary': '1987年投资7亿美元购买所罗门可转换优先股，1991年巴菲特临危受命担任临时董事长处理国债丑闻。这段经历展示了巴菲特在危机中的领导力和对诚信的坚守。',
        'stats': [
            {'value': '1987', 'label': '初始投资'},
            {'value': '$7亿', 'label': '优先股投资'},
            {'value': '1991', 'label': '危机年份'},
            {'value': '临时董事长', 'label': '关键角色'},
        ],
        'logic': [
            {'title': 'John Gutfreund的信任', 'desc': '巴菲特对所罗门CEO John Gutfreund的能力和品格印象深刻。他说Gutfreund在1976年帮助GEICO脱困时展现了出色能力。'},
            {'title': '可转换优先股的安全垫', 'desc': '9%可转换优先股提供了稳定的利息收入，同时保留了转换为普通股的权利。这种结构在1987年市场环境下提供了下行保护。'},
            {'title': '危机中的道德坚守', 'desc': '1991年国债操纵丑闻爆发后，巴菲特接管临时董事长职务，坚持透明和合规原则，帮助公司度过危机。'},
            {'title': '对投行业务的谨慎', 'desc': '巴菲特坦言无法预测投资银行业的未来前景，因为"缺乏强有力的论点支持"。这促使他对这类投资保持审慎。'},
        ],
        'cognition': [
            {'year': '1987：投资决策', 'from': '信任管理层', 'to': '优先股投资', 'desc': '以7亿美元投资所罗门9%可转换优先股，这是伯克希尔当时最大的一笔单一投资。'},
            {'year': '1991：危机爆发', 'from': '信任管理', 'to': '临时接管', 'desc': '国债操纵丑闻爆发后，Gutfreund下台，巴菲特临危受命担任临时董事长稳定局面。'},
            {'year': '1992：危机化解', 'from': '丑闻缠身', 'to': '声誉恢复', 'desc': '在巴菲特的领导下，所罗门的声誉显著恢复，在《财富》最受尊敬公司调查中排名第二。'},
            {'year': '1995：投资退出', 'from': '长期持有', 'to': '完成使命', 'desc': '所罗门最终被旅行者集团收购，伯克希尔的投资获得了合理回报。'},
        ],
        'data1': [
            {'label': '投资时间', 'value': '1987年'},
            {'label': '投资金额', 'value': '7亿美元'},
            {'label': '股息率', 'value': '9%'},
            {'label': '退出方式', 'value': '被收购'},
        ],
        'data2': [
            {'label': '核心业务', 'value': '投资银行'},
            {'label': '危机类型', 'value': '国债操纵丑闻'},
            {'label': '关键人物', 'value': 'John Gutfreund'},
            {'label': '教训类型', 'value': '危机管理与诚信'},
        ],
        'lessons': [
            {'title': '💡 诚信是不可妥协的底线', 'desc': '巴菲特在被推举为所罗门临时董事长后，明确表示："我不会做任何损害伯克希尔声誉的事。"在危机中，道德标准不能因压力而降低。'},
            {'title': '💡 在别人恐惧时担当', 'desc': '当所罗门陷入危机时，巴菲特没有观望，而是亲自站出来稳定军心。这种领导力不仅帮助了所罗门，也保护了伯克希尔的投资。'},
            {'title': '💡 危机也是机遇', 'desc': '所罗门危机反而提升了伯克希尔的声誉。《财富》调查显示公司在危机后声誉显著改善，因为市场看到了伯克希尔的道德标准。'},
        ],
        'quotes': [
            {'text': '1991年当我被推举为所罗门公司的临时董事长时，我把我的嘴放在了我们的钱上。', 'source': '1991年致股东信'},
            {'text': '我之前关于每天喝五罐樱桃可乐的评论，在所罗门事件面前完全不算什么。', 'source': '1991年致股东信'},
            {'text': '所罗门CEO John Gutfreund的能力和品格给我们留下了深刻印象。', 'source': '1987年致股东信'},
        ],
        'related': [
            {'file': '诚信.html', 'icon': '⭐', 'name': '诚信'},
            {'file': '危机处理.html', 'icon': '🆘', 'name': '危机处理'},
            {'file': '优先股.html', 'icon': '📊', 'name': '优先股投资'},
        ],
    },
    
    '房地美': {
        'title': '房地美',
        'en_name': 'Freddie Mac',
        'category': '金融 · 股权投资',
        'icon': '🏦',
        'summary': '1988年开始投资的政府支持企业，巴菲特视其为"稳健的固定收益替代品"。2000年出售大部分持股，躲过了2008年金融危机。',
        'stats': [
            {'value': '1988', 'label': '开始投资'},
            {'value': '8.6%', 'label': '持股峰值'},
            {'value': '2000', 'label': '清仓年份'},
            {'value': '12.7亿', 'label': '2000年盈利'},
        ],
        'logic': [
            {'title': '政府支持企业的隐形背书', 'desc': '房地美作为政府支持企业享有隐性担保，这提供了类似于主权信用的稳定性。'},
            {'title': '稳定的股息收入', 'desc': '8.6%的股息收益率提供了稳定的现金回报，适合作为固定收益的替代品。'},
            {'title': '"太大了不能倒"的逻辑', 'desc': '巴菲特认为政府不会让房地美倒闭，这种认知影响了投资决策。'},
            {'title': '2000年的前瞻性退出', 'desc': '在问题暴露前出售大部分持股，体现了对风险的敏锐嗅觉。'},
        ],
        'cognition': [
            {'year': '1988：买入启动', 'from': '发现机会', 'to': '建立仓位', 'desc': '与可口可乐同时买入，视其为稳健的固定收益替代品。'},
            {'year': '1991-1999：持续持有', 'from': '稳定增长', 'to': '逐步增持', 'desc': '持股从6%提升至8.6%，享受稳定股息。'},
            {'year': '2000：果断清仓', 'from': '持仓不动', 'to': '出售离场', 'desc': '出售几乎全部房地美和房利美持股，躲过后来的危机。'},
            {'year': '2003：洞察问题', 'from': '问题暴露', 'to': '事后验证', 'desc': '"房地美丑闻"的规模令人震惊，验证了退出的正确性。'},
        ],
        'data1': [
            {'label': '投资时期', 'value': '1988-2000年'},
            {'label': '持股比例', 'value': '6%-8.6%'},
            {'label': '退出时机', 'value': '2000年'},
            {'label': '最终结局', 'value': '2008年被接管'},
        ],
        'data2': [
            {'label': '核心业务', 'value': '住房抵押贷款'},
            {'label': '政府背书', 'value': '隐性担保'},
            {'label': '主要风险', 'value': '2008年危机'},
            {'label': '教训类型', 'value': '周期性判断'},
        ],
        'lessons': [
            {'title': '💡 "太大不能倒"的危险假设', 'desc': '政府隐性背书让房地美看似安全，但这种安全感可能导致过度风险承担。投资者需要独立评估风险，而非依赖政府担保。'},
            {'title': '💡 在泡沫形成前退出', 'desc': '2000年出售房地美是正确的决策。巴菲特选择"不持有当前持仓中的任何廉价品"，体现了对估值的敏感。'},
            {'title': '💡 会计问题是大问题的信号', 'desc': '2003年暴露的"房地美丑闻"规模惊人。巴菲特曾指出衍生品公司披露文件的局限性，这在此后得到验证。'},
        ],
        'quotes': [
            {'text': '2000年我们出售了几乎全部的房地美和房利美股份，并在一些中型公司建立了15%的仓位。', 'source': '2000年致股东信'},
            {'text': '无论是阅读衍生品密集型公司的披露文件，还是你所知道的风险，都无法了解其持仓中隐藏的风险。', 'source': '2003年致股东信'},
        ],
        'related': [
            {'file': '政府支持企业.html', 'icon': '🏛️', 'name': ' GSE'},
            {'file': '风险管理.html', 'icon': '⚖️', 'name': '风险管理'},
            {'file': '估值.html', 'icon': '💰', 'name': '估值'},
        ],
    },
    
    '通用汽车': {
        'title': '通用汽车',
        'en_name': 'General Motors',
        'category': '汽车 · 周期见证',
        'icon': '🚗',
        'summary': '巴菲特长期观察但很少投资汽车股。GM的兴衰史见证了美国制造业的变迁，也是巴菲特反思"行业护城河"的重要案例。',
        'stats': [
            {'value': '1965', 'label': '市值巅峰'},
            {'value': '2009', 'label': '破产年份'},
            {'value': '教训', 'label': '核心认知'},
            {'value': '无投资', 'label': '态度'},
        ],
        'logic': [
            {'title': '制造业的高固定成本', 'desc': '汽车制造业需要大量资本投入和固定成本，在经济衰退时损失惨重。'},
            {'title': '工会力量的负面影响', 'desc': '养老金和医疗保险负担削弱了GM的竞争力，与日系车相比处于劣势。'},
            {'title': '管理层的路径依赖', 'desc': '成功的历史反而成为变革的障碍，管理层难以打破"做大做全"的思维。'},
            {'title': '资本配置的错误激励', 'desc': '汽车公司倾向于将利润再投入而非回报股东，导致资本效率低下。'},
        ],
        'cognition': [
            {'year': '1965：巅峰时刻', 'from': '行业霸主', 'to': '开始衰落', 'desc': 'GM曾是全球最大公司，但暗藏的结构性问题开始积累。'},
            {'year': '1984：观察反思', 'from': '案例分析', 'to': '深入理解', 'desc': '巴菲特以GM为例分析领导力与公司命运的关系。'},
            {'year': '2006：预言应验', 'from': '仍在质疑', 'to': '危机临近', 'desc': '"1965年的十大公司中，只有一家仍在2006年榜单"——GM不在其中。'},
            {'year': '2009：破产重组', 'from': '苦苦挣扎', 'to': '涅槃重生', 'desc': 'GM申请破产保护，美国政府救助后重新上市。'},
        ],
        'data1': [
            {'label': '创立时间', 'value': '1908年'},
            {'label': '破产时间', 'value': '2009年'},
            {'label': '美国政府救助', 'value': '495亿美元'},
            {'label': '教训类型', 'value': '行业结构'},
        ],
        'data2': [
            {'label': '核心问题', 'value': '养老金负担'},
            {'label': '竞争对手', 'value': '日系品牌'},
            {'label': '伯克希尔态度', 'value': '长期回避'},
            {'label': '当前状态', 'value': '2010年重新上市'},
        ],
        'lessons': [
            {'title': '💡 竞争优势可以被侵蚀', 'desc': 'GM曾是美国工业的象征，但竞争优势随着时间被侵蚀。巴菲特在1996年指出，IBM、GM、西尔斯都曾经历"似乎不可战胜"的时期。'},
            {'title': '💡 行业选择决定命运', 'desc': '即使是最优秀的管理层，在夕阳行业中也难以创造持续的卓越表现。投资于有利的行业结构比单纯选择管理层更重要。'},
            {'title': '💡 养老金是隐形炸弹', 'desc': 'GM的养老金和医疗保健承诺最终压垮了公司。投资者需要仔细评估企业的长期劳动力负担。'},
        ],
        'quotes': [
            {'text': '1965年十大非石油公司中，只有沃尔玛在2006年仍然榜上有名。', 'source': '2006年致股东信'},
            {'text': '领导力本身不能保证成功：看看GM、IBM和西尔斯，它们都曾有过看似不可战胜的时期。', 'source': '1996年致股东信'},
        ],
        'related': [
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '行业分析.html', 'icon': '📊', 'name': '行业分析'},
            {'file': '资本配置.html', 'icon': '⚙️', 'name': '资本配置'},
        ],
    },
    
    '通用电气': {
        'title': '通用电气',
        'en_name': 'General Electric',
        'category': '工业 · 优先股投资',
        'icon': '⚡',
        'summary': '2011年持有GE优先股获得12亿美元年收益，后被公司赎回。这笔投资展示了巴菲特在危机时期为优质公司提供流动性支持的能力。',
        'stats': [
            {'value': '2011', 'label': '投资年份'},
            {'value': '$12.8亿', 'label': '赎回总额'},
            {'value': '~$12亿', 'label': '年税前收益'},
            {'value': '短期', 'label': '投资性质'},
        ],
        'logic': [
            {'title': '危机时期的流动性提供者', 'desc': '2008年金融危机后，GE面临融资困难。巴菲特以优先股形式提供资金，同时获得稳定收益。'},
            {'title': '优质公司+合理价格', 'desc': 'GE虽然遇到困难，但其品牌和技术实力仍在。优先股结构提供了下行保护。'},
            {'title': '固定收益特征的吸引力', 'desc': '6%股息率和优先清算权使这笔投资具有类债券的安全特性。'},
            {'title': '快速退出实现收益', 'desc': '2011年被赎回时，巴菲特成功获得了约定的收益，实现了资金的高效利用。'},
        ],
        'cognition': [
            {'year': '2008：危机救援', 'from': 'GE陷入困境', 'to': '巴菲特注资', 'desc': '金融危机期间，GE需要融资维持运营，巴菲特提供资金支持。'},
            {'year': '2008-2011：持有期', 'from': '优先股持有', 'to': '稳定收益', 'desc': '持有期间每年获得约12亿美元税前收益。'},
            {'year': '2011：到期赎回', 'from': '投资完成', 'to': '资金回收', 'desc': 'GE支付128亿美元赎回证券，为伯克希尔创造了约12亿税前收益。'},
        ],
        'data1': [
            {'label': '投资类型', 'value': '优先股'},
            {'label': '赎回金额', 'value': '128亿美元'},
            {'label': '年收益', 'value': '约12亿（税前）'},
            {'label': '持有期', 'value': '约3年'},
        ],
        'data2': [
            {'label': '股息率', 'value': '6%'},
            {'label': '赎回方', 'value': 'GE'},
            {'label': '同期收购', 'value': '路博润'},
            {'label': '教训类型', 'value': '危机投资'},
        ],
        'lessons': [
            {'title': '💡 危机中的商业机会', 'desc': '2008年危机时，优质公司急需资金。巴菲特的角色类似"最后贷款人"，在提供流动性的同时获得优厚回报。'},
            {'title': '💡 优先股的结构优势', 'desc': '优先股既提供固定收益（类似债券），又保留股权上行潜力。这种结构在危机时期特别有吸引力。'},
            {'title': '💡 多元化收入来源', 'desc': '路博润收购抵消了优先股赎回带来的收入减少。巴菲特始终在寻找新的投资机会来替代到期的持仓。'},
        ],
        'quotes': [
            {'text': '瑞士再保险、高盛和通用电气向我们支付了总计128亿美元以赎回证券，这些证券为伯克希尔产生了约12亿美元税前收益。', 'source': '2011年致股东信'},
            {'text': '路博润的收购抵消了大部分被赎回的收入。', 'source': '2011年致股东信'},
        ],
        'related': [
            {'file': '优先股.html', 'icon': '📊', 'name': '优先股'},
            {'file': '危机投资.html', 'icon': '🆘', 'name': '危机投资'},
            {'file': '资本配置.html', 'icon': '⚙️', 'name': '资本配置'},
        ],
    },
}

if __name__ == '__main__':
    print("公司数据定义完成，请在主脚本中调用create_page()生成页面")

# 继续添加公司数据

MORE_COMPANIES = {
    'IBM': {
        'title': 'IBM',
        'en_name': 'International Business Machines',
        'category': '科技 · 股权投资',
        'icon': '💻',
        'summary': '2011年以109亿美元买入6390万股IBM，占比5.5%。巴菲特称这是"价值投资的重新发现"，但2018年清仓，承认对科技行业判断有误。',
        'stats': [
            {'value': '2011', 'label': '开始买入'},
            {'value': '$109亿', 'label': '投资总额'},
            {'value': '5.5%→6%', 'label': '持股变化'},
            {'value': '2018', 'label': '清仓年份'},
        ],
        'logic': [
            {'title': '"经济护城河"的重新评估', 'desc': '巴菲特认为IBM存在"大型机的转换成本护城河"，企业更换系统的成本极高。'},
            {'title': '股票回购带来的增持', 'desc': 'IBM的回购计划提高了伯克希尔的持股比例，从5.5%升至6%以上。'},
            {'title': 'CEO郭士纳的转型', 'desc': '郭士纳1993年以来的改革提升了IBM的竞争力和现金流。'},
            {'title': '晚年承认判断失误', 'desc': '2017年巴菲特表示"我在IBM上的判断不如苹果"，承认对科技股理解不够。'},
        ],
        'cognition': [
            {'year': '2011：首次建仓', 'from': '观望科技股', 'to': '大举买入', 'desc': '以109亿美元买入6390万股，成为"四大投资"之一。'},
            {'year': '2012-2014：持续增持', 'from': '稳定持有', 'to': '比例提升', 'desc': '因回购使持股比例从5.5%升至6%以上。'},
            {'year': '2017：公开反思', 'from': '继续持有', 'to': '承认误判', 'desc': '巴菲特表示"我在IBM上犯了一个错误"，对苹果更看好。'},
            {'year': '2018：清仓离场', 'from': '长期持有', 'to': '止损出局', 'desc': '几乎卖光了IBM股票，承认IBM的竞争优势已减弱。'},
        ],
        'data1': [
            {'label': '买入时间', 'value': '2011年'},
            {'label': '买入成本', 'value': '109亿美元'},
            {'label': '持股数量', 'value': '6390万股'},
            {'label': '初始持股', 'value': '5.5%'},
        ],
        'data2': [
            {'label': '增持后持股', 'value': '约6%'},
            {'label': '主要业务', 'value': '企业IT服务'},
            {'label': '核心优势', 'value': '转换成本'},
            {'label': '教训类型', 'value': '科技判断'},
        ],
        'lessons': [
            {'title': '💡 科技股需要特殊能力圈', 'desc': '巴菲特坦言IBM的判断不如苹果，因为科技行业的快速变化使竞争优势更难持久评估。'},
            {'title': '💡 "护城河"可能被侵蚀', 'desc': 'IBM的大型机护城河虽然看似坚固，但云计算的兴起削弱了其价值。'},
            {'title': '💡 承认错误并止损', 'desc': '2018年清仓IBM是痛苦的，但正确的决策。长期持有一个判断错误的标的只会扩大损失。'},
        ],
        'quotes': [
            {'text': '2011年我们进行了一项重大投资，买入6390万股IBM，成本约109亿美元。', 'source': '2011年致股东信'},
            {'text': '我在IBM上的判断不如苹果。我对IBM的判断有误。', 'source': '2017年伯克希尔股东大会'},
            {'text': '苹果与其说是一个科技公司，不如说是一个消费品公司。', 'source': '2017年伯克希尔股东大会'},
        ],
        'related': [
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '能力圈.html', 'icon': '🎯', 'name': '能力圈'},
            {'file': '错误教训.html', 'icon': '📝', 'name': '错误教训'},
        ],
    },

    '中国石油': {
        'title': '中国石油',
        'en_name': 'PetroChina',
        'category': '能源 · H股投资',
        'icon': '🛢️',
        'summary': '2003年以4.88亿美元买入中国石油H股，2007年以40亿美元卖出，获利约7倍。这是巴菲特在A股市场的经典操作之一。',
        'stats': [
            {'value': '2003', 'label': '买入年份'},
            {'value': '$4.88亿', 'label': '买入成本'},
            {'value': '~$40亿', 'label': '卖出金额'},
            {'value': '~7倍', 'label': '获利倍数'},
        ],
        'logic': [
            {'title': '政府背书的能源巨头', 'desc': '中国石油作为国有控股企业，拥有稳定的资源和市场地位。'},
            {'title': '被低估的H股价值', 'desc': '2003年H股价格远低于内在价值，巴菲特识别出了这个明显的廉价机会。'},
            {'title': '石油资源的战略价值', 'desc': '2003年油价处于上升周期，石油资源的价值正在被重估。'},
            {'title': '在泡沫形成前退出', 'desc': '2007年中国股市泡沫期间清仓，实现了丰厚利润。'},
        ],
        'cognition': [
            {'year': '2003：发现价值', 'from': 'H股低迷', 'to': '大举买入', 'desc': '以约5亿美元买入中国石油H股。'},
            {'year': '2003-2007：价值重估', 'from': '持有等待', 'to': '享受牛市', 'desc': '持有期间市值从5亿涨至40亿美元以上。'},
            {'year': '2007：果断卖出', 'from': '继续持有', 'to': '实现利润', 'desc': '在泡沫高点卖出，获利约7倍。'},
        ],
        'data1': [
            {'label': '买入时间', 'value': '2003年'},
            {'label': '买入成本', 'value': '4.88亿美元'},
            {'label': '持股数量', 'value': '11.09亿H股'},
            {'label': '买入价格', 'value': '约$1.7/股'},
        ],
        'data2': [
            {'label': '卖出时间', 'value': '2007年'},
            {'label': '卖出金额', 'value': '约40亿美元'},
            {'label': '持有期限', 'value': '约4年'},
            {'label': '教训类型', 'value': '周期投资'},
        ],
        'lessons': [
            {'title': '💡 在别人恐惧时贪婪', 'desc': '2003年中国市场不被看好时，巴菲特识别出了被低估的价值。'},
            {'title': '💡 知道何时卖出', 'desc': '2007年A股泡沫期间，巴菲特没有贪婪，而是实现了利润。知道何时离开比何时进入更重要。'},
            {'title': '💡 石油股的周期性', 'desc': '大宗商品价格有周期性，了解行业周期有助于选择买卖时机。'},
        ],
        'quotes': [
            {'text': '2003年我们大量买入中国石油H股，成本约4.88亿美元。', 'source': '伯克希尔官方披露'},
            {'text': '买入中国石油是因为它的价值明显被低估了。', 'source': '2008年伯克希尔股东大会'},
        ],
        'related': [
            {'file': '估值.html', 'icon': '💰', 'name': '估值'},
            {'file': '周期投资.html', 'icon': '📈', 'name': '周期投资'},
            {'file': '能力圈.html', 'icon': '🎯', 'name': '能力圈'},
        ],
    },

    'TTI': {
        'title': 'TTI',
        'en_name': 'TTI',
        'category': '电子元器件 · 收购',
        'icon': '🔌',
        'summary': '2006年收购的电子元器件分销商，由保罗·安德鲁斯(Paul Andrews)领导。这是伯克希尔"五小强"之一，展现了巴菲特对利基市场冠军的偏好。',
        'stats': [
            {'value': '2006', 'label': '收购年份'},
            {'value': '保罗·安德鲁斯', 'label': 'CEO'},
            {'value': '$11.3亿→$13亿', 'label': '营收增长'},
            {'value': '冠军', 'label': '市场地位'},
        ],
        'logic': [
            {'title': '利基市场冠军', 'desc': 'TTI是电子元器件专业分销商，市场份额领先，是典型的"小池塘里的大鱼"。'},
            {'title': '优秀的CEO', 'desc': '安德鲁斯使TTI从11.2万美元营收成长为13亿美元，用了35年。'},
            {'title': '简单可预测的业务', 'desc': '元器件分销的商业模式相对简单，收入稳定可预测。'},
            {'title': '伯克希尔的文化契合', 'desc': '安德鲁斯像典型的伯克希尔经理人——专注、节俭、注重长期。'},
        ],
        'cognition': [
            {'year': '2006：收购完成', 'from': '寻找归宿', 'to': '加入伯克希尔', 'desc': '安德鲁斯寻求伯克希尔的收购，因为欣赏伯克希尔的文化和声誉。'},
            {'year': '2006-2017：稳健增长', 'from': '持续增长', 'to': '越来越强', 'desc': 'TTI成为伯克希尔增长最快的业务之一。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '2006年'},
            {'label': '营收规模', 'value': '约13亿美元'},
            {'label': '员工规模', 'value': '约3000人'},
            {'label': 'CEO', 'value': 'Paul Andrews'},
        ],
        'data2': [
            {'label': '主营业务', 'value': '电子元器件分销'},
            {'label': '市场地位', 'value': '行业领先'},
            {'label': '增长模式', 'value': '内生+收购'},
            {'label': '教训类型', 'value': '利基冠军'},
        ],
        'lessons': [
            {'title': '💡 小池塘里的大鱼', 'desc': 'TTI所在的细分市场虽小，但足够支撑一家优秀企业长期增长。'},
            {'title': '💡 优秀CEO是关键', 'desc': '安德鲁斯35年如一日地把TTI从11万做到13亿，体现了企业家的专注精神。'},
            {'title': '💡 文化契合很重要', 'desc': '安德鲁斯专门寻找伯克希尔式的收购方，说明企业文化和价值观的契合度。'},
        ],
        'quotes': [
            {'text': 'TTI由保罗·安德鲁斯领导，他是一位杰出且专注的商人，把公司从11.2万美元做到了13亿美元。', 'source': '2006年致股东信'},
            {'text': 'TTI和伊斯卡是由CEO领导的优秀企业，2007年表现出色。', 'source': '2007年致股东信'},
        ],
        'related': [
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '收购.html', 'icon': '🤝', 'name': '收购'},
        ],
    },

    '利捷航空': {
        'title': '利捷航空',
        'en_name': 'NetJets',
        'category': '航空 · 部分所有权',
        'icon': '✈️',
        'summary': 'NetJets是全球最大的私人飞机部分所有权项目，伯克希尔通过飞安国际拥有该业务。这代表了巴菲特对航空业的复杂态度转变。',
        'stats': [
            {'value': '1998', 'label': '收购飞安'},
            {'value': 'NetJets', 'label': '关联公司'},
            {'value': '高端', 'label': '市场定位'},
            {'value': '全球', 'label': '服务范围'},
        ],
        'logic': [
            {'title': '与GEICO的客户协同', 'desc': 'NetJets的用户包括许多GEICO的潜在客户，形成了业务协同。'},
            {'title': '"时间价值"护城河', 'desc': '私人飞机服务对高净值人士和企业高管有不可替代的价值。'},
            {'title': '阿尔·尤因的战略眼光', 'desc': '飞安国际创始人阿尔·尤因是航空业的传奇人物，其战略眼光值得信赖。'},
            {'title': '对抗无聊的航空业务', 'desc': '在伯克希尔的收购组合中，NetJets提供了一定的业务多元化。'},
        ],
        'cognition': [
            {'year': '1998：收购飞安', 'from': '飞安独立', 'to': '伯克希尔旗下', 'desc': '收购飞安国际，后将其与NetJets整合。'},
            {'year': '持续运营', 'from': '稳定经营', 'to': '行业领先', 'desc': 'NetJets保持私人飞机市场的领导地位。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '1998年'},
            {'label': '主营业务', 'value': '飞机部分所有权'},
            {'label': '市场地位', 'value': '全球领先'},
            {'label': '关联公司', 'value': '飞安国际'},
        ],
        'data2': [
            {'label': '客户群', 'value': '高净值人士'},
            {'label': '核心优势', 'value': '时间灵活性'},
            {'label': '协同业务', 'value': 'GEICO'},
            {'label': '教训类型', 'icon': '航空业', 'name': '资本密集'},
        ],
        'lessons': [
            {'title': '💡 航空业的资本密集性', 'desc': '飞机业务需要大量资本投入，维护成本高。伯克希尔的资本实力使这项业务可行。'},
            {'title': '💡 客户协同的价值', 'desc': 'NetJets的用户往往也是GEICO的潜在客户，业务协同创造了额外价值。'},
        ],
        'quotes': [
            {'text': 'NetJets的用户包括许多大型企业，其中通用电气最大——它拥有自己的机队，但我们是最了解如何有效和经济地使用飞机的。', 'source': '2002年致股东信'},
        ],
        'related': [
            {'file': '业务协同.html', 'icon': '🤝', 'name': '业务协同'},
            {'file': '资本配置.html', 'icon': '⚙️', 'name': '资本配置'},
        ],
    },
}

# 继续添加更多公司

EVEN_MORE_COMPANIES = {
    '大都会通信': {
        'title': '大都会通信',
        'en_name': 'Capital Cities Communications',
        'category': '媒体 · 收购',
        'icon': '📺',
        'summary': '1985年以172.5美元/股收购Capital Cities Broadcasting，远高于市场价。这笔投资最终演变为与ABC的合并，成为美国最大的传媒集团之一。',
        'stats': [
            {'value': '1985', 'label': '收购年份'},
            {'value': '$172.5/股', 'label': '收购价'},
            {'value': '溢价', 'label': '支付方式'},
            {'value': 'ABC合并', 'label': '后续发展'},
        ],
        'logic': [
            {'title': '对Tom Murphy的信任', 'desc': 'Tom Murphy是巴菲特眼中最优秀的CEO之一，是"真正懂得如何经营企业的人"。'},
            {'title': '广播、电视的地域护城河', 'desc': '特定市场的广播牌照具有天然的垄断性，是有价值的无形资产。'},
            {'title': '愿意为好公司付溢价', 'desc': '172.5美元的价格比市场价高出25%，但巴菲特认为优质资产值得溢价。'},
        ],
        'cognition': [
            {'year': '1985：收购完成', 'from': '独立运营', 'to': '与伯克希尔合作', 'desc': '以172.5美元/股收购Capital Cities。'},
            {'year': '1995：与ABC合并', 'from': '单独发展', 'to': '超级传媒集团', 'desc': 'Capital Cities与ABC合并，成为美国最大传媒公司之一。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '1985年3月'},
            {'label': '收购价格', 'value': '$172.5/股'},
            {'label': '收购数量', 'value': '300万股'},
            {'label': '溢价幅度', 'value': '约25%'},
        ],
        'data2': [
            {'label': '主营业务', 'value': '广播、电视'},
            {'label': '核心资产', 'value': '地域广播牌照'},
            {'label': '关键人物', 'value': 'Tom Murphy'},
            {'label': '教训类型', 'icon': '优质溢价', 'name': '成长投资'},
        ],
        'lessons': [
            {'title': '💡 好公司的溢价是值得的', 'desc': '虽然172.5美元比市场价高出25%，但Capital Cities的内在价值更高。这证明了"合理价格买优质企业"的价值。'},
            {'title': '💡 管理层是重要的护城河', 'desc': 'Tom Murphy的能力和品格是这笔投资成功的关键因素之一。'},
        ],
        'quotes': [
            {'text': 'Tom Murphy真正懂得如何经营企业，是我见过的最优秀的CEO之一。', 'source': '巴菲特评价'},
            {'text': '我对Capital Cities的管理层充满信心。', 'source': '1985年致股东信'},
        ],
        'related': [
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '合理价格买入优质企业.html', 'icon': '💎', 'name': 'GARP'},
        ],
    },

    '布法罗新闻报': {
        'title': '布法罗新闻报',
        'en_name': 'Buffalo Evening News',
        'category': '媒体 · 报纸',
        'icon': '📰',
        'summary': '1977年以3250万美元收购的报纸，是伯克希尔最成功的收购之一。在stan Lipsey的管理下，新闻报垄断了布法罗市场，成为"七贤"之一。',
        'stats': [
            {'value': '1977', 'label': '收购年份'},
            {'value': '$3250万', 'label': '收购价格'},
            {'value': 'Stan Lipsey', 'label': '管理者'},
            {'value': '垄断', 'label': '市场地位'},
        ],
        'logic': [
            {'title': '日报的天然垄断', 'desc': '布法罗只有一份主要日报，享有类似自然垄断的市场地位。'},
            {'title': '人格的信任', 'desc': 'Stan Lipsey的管理能力和诚信是巴菲特投资的重要原因。'},
            {'title': '广告收入护城河', 'desc': '一旦成为当地主要信息来源，用户和广告商都难以离开。'},
        ],
        'cognition': [
            {'year': '1977：早期挣扎', 'from': '亏损运营', 'to': '逐步改善', 'desc': '收购初期经历多年亏损，但最终垄断了市场。'},
            {'year': '1980s-1990s：黄金时代', 'from': '扭亏为盈', 'to': '持续增长', 'desc': '新闻报成为布法罗唯一的主要日报，利润持续增长。'},
            {'year': '2000s：行业衰退', 'from': '稳定盈利', 'to': '随行业下滑', 'desc': '随着互联网冲击，报纸行业整体衰退，但新闻报仍相对稳定。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '1977年'},
            {'label': '收购价格', 'value': '3250万美元'},
            {'label': '管理者', 'value': 'Stan Lipsey'},
            {'label': '市场地位', 'value': '唯一主要日报'},
        ],
        'data2': [
            {'label': '业务模式', 'value': '日报+广告'},
            {'label': '市场特征', 'value': '自然垄断'},
            {'label': '巅峰时期', 'value': '1990年代'},
            {'label': '教训类型', 'icon': '报纸衰落', 'name': '行业变革'},
        ],
        'lessons': [
            {'title': '💡 地方垄断的持久价值', 'desc': '布法罗只有一份主要日报，这种垄断地位维持了数十年。但最终敌不过互联网的冲击。'},
            {'title': '💡 优秀管理层的价值', 'desc': 'Stan Lipsey把新闻报做成了真正的印钞机，体现了管理层的重要性。'},
            {'title': '💡 行业趋势不可抗拒', 'desc': '即使是最好的报纸，在互联网面前也难以幸免。投资者需要关注行业的长期趋势。'},
        ],
        'quotes': [
            {'text': '布法罗新闻报在1985年税前利润达到3200万美元，1999年进一步增长到3500万美元。', 'source': '伯克希尔年报'},
            {'text': 'Stan Lipsey是报纸行业最优秀的经理人之一。', 'source': '巴菲特评价'},
        ],
        'related': [
            {'file': '护城河.html', 'icon': '🏰', 'name': '护城河'},
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '行业分析.html', 'icon': '📊', 'name': '行业分析'},
        ],
    },

    '庄臣': {
        'title': '庄臣',
        'en_name': 'S.C. Johnson',
        'category': '消费品 · 持股',
        'icon': '🧴',
        'summary': '巴菲特持有庄臣（SC Johnson）股份但规模较小。这家家族企业以消费品业务闻名，是巴菲特研究"消费者品牌护城河"的案例。',
        'stats': [
            {'value': '小型', 'label': '持股规模'},
            {'value': '消费品', 'label': '业务类型'},
            {'value': '家族', 'label': '所有制'},
            {'value': '品牌', 'label': '护城河'},
        ],
        'logic': [
            {'title': '消费者品牌的护城河', 'desc': '庄臣拥有Windex、Raid等知名品牌，具有强大的消费者忠诚度。'},
            {'title': '家族企业的稳定性', 'desc': '作为未上市的家族企业，庄臣可以着眼长期而非短期股价。'},
        ],
        'cognition': [
            {'year': '观察研究', 'from': '持股规模小', 'to': '长期关注', 'desc': '虽然不是重仓，但庄臣是巴菲特研究消费品行业的窗口。'},
        ],
        'data1': [
            {'label': '持股规模', 'value': '相对较小'},
            {'label': '持股目的', 'value': '消费品研究'},
            {'label': '业务类型', 'value': '家庭清洁用品'},
            {'label': '品牌', 'value': 'Windex等'},
        ],
        'data2': [
            {'label': '所有制', 'value': '家族私有'},
            {'label': '竞争优势', 'value': '品牌+渠道'},
            {'label': '市场地位', 'value': '细分市场领先'},
            {'label': '教训类型', 'icon': '消费品', 'name': '品牌投资'},
        ],
        'lessons': [
            {'title': '💡 消费品牌的持久力', 'desc': '庄臣这样的消费品公司即使不上市也能长期增长，体现了品牌的内在价值。'},
        ],
        'quotes': [],
        'related': [
            {'file': '品牌护城河.html', 'icon': '🏰', 'name': '品牌护城河'},
            {'file': '消费品投资.html', 'icon': '🛒', 'name': '消费品'},
        ],
    },

    '德尔': {
        'title': '德尔',
        'en_name': 'Graham Holdings',
        'category': '媒体 · 教育',
        'icon': '📚',
        'summary': '前身是华盛顿邮报公司，2013年改名德尔。该公司已从传统媒体转型为教育和媒体公司，格雷厄姆家族的传承故事令人印象深刻。',
        'stats': [
            {'value': '1933', 'label': '邮报创立'},
            {'value': '2013', 'label': '改名'},
            {'value': '格雷厄姆', 'label': '家族传承'},
            {'value': '转型', 'label': '业态变化'},
        ],
        'logic': [
            {'title': '华盛顿邮报的品牌价值', 'desc': '邮报因水门事件闻名世界，拥有无可比拟的新闻声誉。'},
            {'title': '教育业务的拓展', 'desc': 'Kaplan教育业务成为新的增长引擎，实现了业务转型。'},
            {'title': '家族企业的传承', 'desc': '格雷厄姆家族的女性领导（Don Graham的母亲）是美国商业史上的佳话。'},
        ],
        'cognition': [
            {'year': '1973：成为第二大股东', 'from': '观望', 'to': '大举买入', 'desc': '巴菲特开始建仓华盛顿邮报。'},
            {'year': '1980s-2000s：长期持有', 'from': '长期持有', 'to': '丰厚回报', 'desc': '邮报为巴菲特带来丰厚回报，但最终他选择退出。'},
            {'year': '2013：战略转型', 'from': '华盛顿邮报', 'to': 'Graham Holdings', 'desc': '公司更名为Graham Holdings，专注于教育和媒体。'},
        ],
        'data1': [
            {'label': '投资时期', 'value': '1973-2000s'},
            {'label': '创始人', 'value': 'Eugene Meyer'},
            {'label': '关键人物', 'value': 'Don Graham'},
            {'label': '转型时间', 'value': '2013年'},
        ],
        'data2': [
            {'label': '原主营业务', 'value': '报纸出版'},
            {'label': '新主营业务', 'value': '教育+媒体'},
            {'label': '品牌资产', 'value': '华盛顿邮报'},
            {'label': '教训类型', 'icon': '媒体转型', 'name': '行业变革'},
        ],
        'lessons': [
            {'title': '💡 品牌的持久与变迁', 'desc': '华盛顿邮报从报纸转型为教育和媒体集团，说明企业需要随时代变化而进化。'},
            {'title': '💡 创始人的重要性', 'desc': '格雷厄姆家族的领导力是华盛顿邮报成功的关键因素。'},
        ],
        'quotes': [
            {'text': '菲尔·格雷厄姆曾说："新闻是历史的第一手草稿。"', 'source': '1984年致股东信'},
        ],
        'related': [
            {'file': '品牌护城河.html', 'icon': '🏰', 'name': '品牌护城河'},
            {'file': '媒体投资.html', 'icon': '📺', 'name': '媒体'},
            {'file': '长期投资.html', 'icon': '⏳', 'name': '长期投资'},
        ],
    },

    '斯科特费泽': {
        'title': '斯科特费泽',
        'en_name': 'Scott Fetzer',
        'category': '制造业 · 收购',
        'icon': '⚙️',
        'summary': '1986年收购的制造业集团，旗下包括World Book百科全书、Kirby吸尘器等业务。是伯克希尔"七贤"之一，展现了巴菲特对中等规模优质企业的偏好。',
        'stats': [
            {'value': '1986', 'label': '收购年份'},
            {'value': '"七贤"', 'label': '称号'},
            {'value': '多个', 'label': '子公司'},
            {'value': '稳健', 'label': '盈利模式'},
        ],
        'logic': [
            {'title': '多元化的制造业组合', 'desc': '旗下业务覆盖百科全书、保险、吸尘器等多个领域，风险分散。'},
            {'title': '可靠的现金流', 'desc': '这些业务虽然不起眼，但现金流稳定，是典型的"现金牛"。'},
            {'title': '优秀的经理人Ralph Schey', 'desc': 'Ralph Schey是Scott Fetzer的CEO，被巴菲特高度评价。'},
        ],
        'cognition': [
            {'year': '1986：收购完成', 'from': '独立发展', 'to': '伯克希尔旗下', 'desc': '以合理价格收购Scott Fetzer。'},
            {'year': '1986-2000s：持续贡献', 'from': '稳定盈利', 'to': '核心资产', 'desc': 'Scott Fetzer多年为伯克希尔提供稳定的利润。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '1986年'},
            {'label': '主要业务', 'value': '百科全书、保险'},
            {'label': 'CEO', 'value': 'Ralph Schey'},
            {'label': '市场地位', 'value': '细分市场领先'},
        ],
        'data2': [
            {'label': '现金流', 'value': '稳定'},
            {'label': '业务类型', 'value': '多元制造'},
            {'label': '竞争优势', 'value': '品牌+渠道'},
            {'label': '教训类型', 'icon': '中盘股', 'name': '收购'},
        ],
        'lessons': [
            {'title': '💡 中等规模企业的价值', 'desc': 'Scott Fetzer不是耀眼的公司，但多年稳定地贡献现金流，体现了"隐形冠军"的价值。'},
            {'title': '💡 优秀CEO的重要性', 'desc': 'Ralph Schey的管理能力是这笔投资成功的关键因素。'},
        ],
        'quotes': [
            {'text': '我们把Scott Fetzer、World Book、Kirby等公司称为"七贤"。', 'source': '1988年致股东信'},
        ],
        'related': [
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '收购.html', 'icon': '🤝', 'name': '收购'},
            {'file': '现金牛.html', 'icon': '🐄', 'name': '现金牛'},
        ],
    },

    '森林河公司': {
        'title': '森林河公司',
        'en_name': 'Forest River',
        'category': '制造业 · 房车',
        'icon': '🏕️',
        'summary': '2005年收购的房车和船艇制造商，由CEO Tim Kenesey领导。是伯克希尔"五小强"之一，代表了伯克希尔对休闲制造业的布局。',
        'stats': [
            {'value': '2005', 'label': '收购年份'},
            {'value': 'Tim Kenesey', 'label': 'CEO'},
            {'value': '房车+船艇', 'label': '业务类型'},
            {'value': '"五小强"', 'label': '称号'},
        ],
        'logic': [
            {'title': '休闲消费的增长趋势', 'desc': '随着美国人口老龄化和休闲需求增加，房车市场前景良好。'},
            {'title': '优秀的管理层', 'desc': 'Tim Kenesey被巴菲特称赞为"本能地像伯克希尔经理人一样思考"。'},
            {'title': '制造能力的护城河', 'desc': 'Forest River在房车和船艇制造方面具有规模效应和工艺积累。'},
        ],
        'cognition': [
            {'year': '2005：收购完成', 'from': '独立发展', 'to': '伯克希尔旗下', 'desc': '收购Forest River，继续扩张制造业版图。'},
            {'year': '2005-今：持续增长', 'from': '稳定增长', 'to': '行业领先', 'desc': 'Forest River成为房车和船艇行业的领导者。'},
        ],
        'data1': [
            {'label': '收购时间', 'value': '2005年'},
            {'label': 'CEO', 'value': 'Tim Kenesey'},
            {'label': '主营业务', 'value': '房车、船艇'},
            {'label': '市场地位', 'value': '行业领先'},
        ],
        'data2': [
            {'label': '业务模式', 'value': '制造+销售'},
            {'label': '目标客户', 'value': '休闲消费者'},
            {'label': '竞争优势', 'value': '规模+品牌'},
            {'label': '教训类型', 'icon': '休闲制造', 'name': '消费升级'},
        ],
        'lessons': [
            {'title': '💡 消费升级的机会', 'desc': 'Forest River代表了美国休闲消费的趋势，老龄化社会将带来更多房车需求。'},
            {'title': '💡 管理层契合度', 'desc': 'Tim Kenesey被称赞"本能地像伯克希尔经理人"，说明企业文化契合的重要性。'},
        ],
        'quotes': [
            {'text': 'Forest River的CEO Tim Kenesey是一位聪明且充满活力的领导者，他本能地像伯克希尔经理人一样思考。', 'source': '2005年致股东信'},
        ],
        'related': [
            {'file': '管理层.html', 'icon': '👔', 'name': '管理层'},
            {'file': '消费升级.html', 'icon': '🛍️', 'name': '消费升级'},
            {'file': '收购.html', 'icon': '🤝', 'name': '收购'},
        ],
    },
}

# 继续添加更多公司

FINAL_BATCH = {
    '威瑞森通讯': {
        'title': '威瑞森通讯',
        'en_name': 'Verizon',
        'category': '电信 · 股权投资',
        'icon': '📱',
        'summary': '威瑞森是美国最大的电信运营商之一。巴菲特在2020年开始建仓，代表了对稳定现金流的通信基础设施公司的偏好。',
        'stats': [
            {'value': '2020', 'label': '开始建仓'},
            {'value': '电信', 'label': '行业'},
            {'value': '高股息', 'label': '收益特征'},
            {'value': '基础设施', 'label': '护城河'},
        ],
        'logic': [
            {'title': '5G基础设施的价值', 'desc': '作为美国最大电信运营商，威瑞森拥有稀缺的无线频谱资源和基础设施。'},
            {'title': '稳定的现金流', 'desc': '电信服务是刚性需求，收入相对稳定，适合作为防御性持仓。'},
            {'title': '高股息收益率', 'desc': '威瑞森提供相对较高的股息收益率，对追求现金流的投资者有吸引力。'},
        ],
        'cognition': [
            {'year': '2020：开始建仓', 'from': '观望', 'to': '逐步买入', 'desc': '巴菲特开始买入威瑞森股票。'},
        ],
        'data1': [
            {'label': '行业', 'value': '无线通信'},
            {'label': '市场地位', 'value': '美国最大'},
            {'label': '业务模式', 'value': '基础设施+服务'},
            {'label': '股息', 'value': '相对较高'},
        ],
        'data2': [
            {'label': '护城河', 'value': '频谱资源'},
            {'label': '竞争优势', 'value': '网络效应'},
            {'label': '风险', 'value': '资本支出'},
            {'label': '教训类型', 'icon': '电信投资', 'name': '基础设施'},
        ],
        'lessons': [
            {'title': '💡 基础设施的稳定价值', 'desc': '电信网络是现代社会的基础设施，具有相对稳定的现金流特征。'},
        ],
        'quotes': [],
        'related': [
            {'file': '基础设施投资.html', 'icon': '🏗️', 'name': '基础设施'},
            {'file': '现金流.html', 'icon': '💵', 'name': '现金流'},
            {'file': '高股息.html', 'icon': '📈', 'name': '高股息'},
        ],
    },

    '特许通讯': {
        'title': '特许通讯',
        'en_name': 'Charter Communications',
        'category': '有线电视 · 股权投资',
        'icon': '📡',
        'summary': '特许通讯是美国第二大有线电视运营商。巴菲特的持仓代表了其对宽带基础设施的兴趣。',
        'stats': [
            {'value': '2014+', 'label': '建仓时间'},
            {'value': '有线电视', 'label': '行业'},
            {'value': '宽带', 'label': '核心业务'},
            {'value': '整合', 'label': '行业趋势'},
        ],
        'logic': [
            {'title': '宽带是刚需', 'desc': '互联网接入是现代生活的必需品，宽带需求持续增长。'},
            {'title': '地区垄断的特性', 'desc': '有线电视网络具有地域垄断特性，一旦建成竞争者难以进入。'},
            {'title': '行业整合的机会', 'desc': '有线电视行业正在整合，规模较大的运营商可能受益。'},
        ],
        'cognition': [
            {'year': '2014至今', 'from': '逐步买入', 'to': '持续持有', 'desc': '巴菲特通过伯克希尔持续买入特许通讯。'},
        ],
        'data1': [
            {'label': '行业', 'value': '有线电视'},
            {'label': '市场地位', 'value': '美国第二'},
            {'label': '主营业务', 'value': '宽带+视频'},
            {'label': '竞争优势', 'value': '网络资源'},
        ],
        'data2': [
            {'label': '护城河', 'value': '地区垄断'},
            {'label': '增长驱动', 'value': '宽带需求'},
            {'label': '风险', 'value': '债务负担'},
            {'label': '教训类型', 'icon': '有线电视', 'name': '媒体'},
        ],
        'lessons': [
            {'title': '💡 网络资源的战略价值', 'desc': '有线网络是稀有资源，地区垄断特性提供了稳定的现金流。'},
        ],
        'quotes': [],
        'related': [
            {'file': '网络效应.html', 'icon': '🌐', 'name': '网络效应'},
            {'file': '基础设施投资.html', 'icon': '🏗️', 'name': '基础设施'},
        ],
    },

    '美国合众银行': {
        'title': '美国合众银行',
        'en_name': 'U.S. Bancorp',
        'category': '银行 · 股权投资',
        'icon': '🏦',
        'summary': '美国合众银行是美国第五大商业银行。巴菲特曾持有其股份，是其银行投资组合的一部分。',
        'stats': [
            {'value': '2006', 'label': '可见年份'},
            {'value': '第五', 'label': '规模排名'},
            {'value': '商业银行', 'label': '业务类型'},
            {'value': '稳定', 'label': '经营风格'},
        ],
        'logic': [
            {'title': '规模化的商业银行', 'desc': '美国合众银行作为大型区域性银行，具有稳定的客户基础。'},
            {'title': '审慎的经营风格', 'desc': '该行以审慎的风险管理著称，在金融危机中相对稳健。'},
        ],
        'cognition': [
            {'year': '2006：出现在持仓', 'from': '建仓', 'to': '持有', 'desc': '伯克希尔持仓中出现美国合众银行。'},
        ],
        'data1': [
            {'label': '行业', 'value': '商业银行'},
            {'label': '规模', 'value': '美国第五大'},
            {'label': '业务', 'value': '传统银行业务'},
            {'label': '市场', 'value': '中西部为主'},
        ],
        'data2': [
            {'label': '竞争优势', 'value': '规模+地域'},
            {'label': '风险特征', 'value': '信用风险'},
            {'label': '教训类型', 'icon': '银行', 'name': '金融'},
        ],
        'lessons': [
            {'title': '💡 大型银行的稳定性', 'desc': '美国合众银行这样的规模提供了稳定性，但也要关注其风险管理能力。'},
        ],
        'quotes': [],
        'related': [
            {'file': '银行投资.html', 'icon': '🏦', 'name': '银行'},
            {'file': '风险管理.html', 'icon': '⚖️', 'name': '风险管理'},
        ],
    },

    '美国家庭服务': {
        'title': '美国家庭服务',
        'en_name': 'Home Services of America',
        'category': '房地产 · 中介',
        'icon': '🏠',
        'summary': '中美能源旗下的房地产中介公司，是美国第二大住宅经纪公司。在房地产市场中扮演重要角色。',
        'stats': [
            {'value': '2003', 'label': '并入时间'},
            {'value': '第二', 'label': '市场地位'},
            {'value': '20+', 'label': '地区品牌'},
            {'value': '20,300', 'label': '经纪人'},
        ],
        'logic': [
            {'title': '房地产市场的中介角色', 'desc': 'Home Services连接买家和卖家，是房地产市场流动性的关键。'},
            {'title': '多品牌策略', 'desc': '通过收购和保留本地品牌，Home Services实现了地域扩张。'},
            {'title': '与中美能源的协同', 'desc': '作为中美能源的一部分，可以共享资源和客户。'},
        ],
        'cognition': [
            {'year': '2003：收购', 'from': '独立公司', 'to': '中美能源旗下', 'desc': '中美能源收购Home Services。'},
            {'year': '2006：持续发展', 'from': '扩张', 'to': '整合', 'desc': '运营20多个地区品牌，拥有20300名经纪人。'},
        ],
        'data1': [
            {'label': '母公司', 'value': '中美能源'},
            {'label': '市场地位', 'value': '全美第二'},
            {'label': '品牌数', 'value': '20+个'},
            {'label': '经纪人', 'value': '约20,300人'},
        ],
        'data2': [
            {'label': '业务模式', 'value': '住宅经纪'},
            {'label': '收入来源', 'value': '佣金'},
            {'label': '竞争优势', 'value': '品牌+规模'},
            {'label': '教训类型', 'icon': '房地产', 'name': '中介'},
        ],
        'lessons': [
            {'title': '💡 中介的商业模式', 'desc': '房地产中介的商业模式简单直接，核心竞争力在于经纪人的数量和质量。'},
        ],
        'quotes': [
            {'text': '中美能源旗下的美国家庭服务公司是美国第二大不动产中介业者，拥有20,300位经纪人。', 'source': '2006年致股东信'},
        ],
        'related': [
            {'file': '中美能源.html', 'icon': '⚡', 'name': '中美能源'},
            {'file': '中介投资.html', 'icon': '🤝', 'name': '中介'},
        ],
    },

    '韦斯科': {
        'title': '韦斯科',
        'en_name': 'Wesco Financial',
        'category': '保险 · 子公司',
        'icon': '🛡️',
        'summary': '韦斯科金融是伯克希尔的控股子公司，主要从事保险和投资业务。芒格曾是韦斯科的董事长，是伯克希尔系的重要成员。',
        'stats': [
            {'value': '1977', 'label': '首次接触'},
            {'value': '1980s', 'label': '完全收购'},
            {'value': '芒格', 'label': '董事长'},
            {'value': '保险+投资', 'label': '主营业务'},
        ],
        'logic': [
            {'title': '芒格的影响力', 'desc': '芒格长期担任韦斯科董事长，其价值投资理念深刻影响了这家公司。'},
            {'title': '保险业务的稳定性', 'desc': '韦斯科的保险业务为伯克希尔提供了稳定的浮存金。'},
            {'title': '价值投资的践行者', 'desc': '韦斯科的投资风格体现了芒格的价值投资哲学。'},
        ],
        'cognition': [
            {'year': '1977：首次投资', 'from': '蓝筹邮票控股', 'to': '逐步整合', 'desc': '通过蓝筹邮票持有韦斯科80%股权。'},
            {'year': '1980s：完全收购', 'from': '控股', 'to': '全资', 'desc': '伯克希尔完全收购韦斯科，成为子公司。'},
        ],
        'data1': [
            {'label': '主营业务', 'value': '保险+投资'},
            {'label': '关键人物', 'value': '查理·芒格'},
            {'label': '持股比例', 'value': '100%'},
            {'label': '文化', 'value': '价值投资'},
        ],
        'data2': [
            {'label': '投资风格', 'value': '长期价值'},
            {'label': '竞争优势', 'value': '芒格智慧'},
            {'label': '教训类型', 'icon': '保险', 'name': '价值投资'},
        ],
        'lessons': [
            {'title': '💡 芒格思想的体现', 'desc': '韦斯科的运营体现了芒格的价值投资理念，强调长期视角和理性分析。'},
            {'title': '💡 保险+投资的协同', 'desc': '韦斯科的保险业务提供了低成本资金，用于价值投资。'},
        ],
        'quotes': [
            {'text': '蓝筹邮票持有80%股权的韦斯科金融公司由Louis Vincenti管理。', 'source': '1977年致股东信'},
        ],
        'related': [
            {'file': '芒格.html', 'icon': '🧠', 'name': '芒格'},
            {'file': '价值投资.html', 'icon': '💎', 'name': '价值投资'},
            {'file': '保险.html', 'icon': '🛡️', 'name': '保险'},
        ],
    },
}

# 汇总所有公司数据
ALL_COMPANIES = {}
ALL_COMPANIES.update(COMPANIES)
ALL_COMPANIES.update(MORE_COMPANIES)
ALL_COMPANIES.update(EVEN_MORE_COMPANIES)
ALL_COMPANIES.update(FINAL_BATCH)

def generate_all_pages(output_dir):
    """生成所有公司页面"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    generated = []
    for company_id, data in ALL_COMPANIES.items():
        try:
            page = create_page(data)
            filepath = os.path.join(output_dir, f"{company_id}.html")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page)
            generated.append(company_id)
            print(f"✓ Generated: {company_id}")
        except Exception as e:
            print(f"✗ Failed: {company_id} - {e}")
    
    return generated

if __name__ == '__main__':
    output_dir = "./投资研究/知识库/巴菲特知识库-LearnBuffett版/companies/"
    generated = generate_all_pages(output_dir)
    print(f"\n共生成 {len(generated)} 个页面")
