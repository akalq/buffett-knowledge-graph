#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量为巴菲特知识库子页面添加侧边栏导航
"""

import os
import re

# 基础路径 - 使用当前目录
BASE_PATH = '.'

# 侧边栏HTML模板（链接路径会根据页面位置动态调整）
def get_sidebar_html(link_prefix=''):
    """获取侧边栏HTML，link_prefix用于调整链接路径"""
    return f'''    <!-- Sidebar Overlay (Mobile) -->
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    
    <!-- Mobile Menu Button -->
    <button class="mobile-menu-btn" id="mobileMenuBtn">☰</button>
    
    <!-- Sidebar -->
    <aside class="sidebar" id="sidebar">
        <button class="sidebar-toggle" id="sidebarToggle" title="展开/收起菜单">
            <span id="toggleIcon">☰</span>
        </button>
        
        <nav class="sidebar-nav">
            <a href="{link_prefix}index-pages/巴菲特致股东信总览.html" class="nav-item">
                <span class="icon">📝</span>
                <span class="label">信件总览</span>
            </a>
            <a href="{link_prefix}index-pages/核心思想索引.html" class="nav-item">
                <span class="icon">💡</span>
                <span class="label">核心概念</span>
            </a>
            <a href="{link_prefix}index-pages/公司索引.html" class="nav-item">
                <span class="icon">🏢</span>
                <span class="label">公司索引</span>
            </a>
            <a href="{link_prefix}index-pages/人物索引.html" class="nav-item">
                <span class="icon">👤</span>
                <span class="label">人物索引</span>
            </a>
            <a href="{link_prefix}index-pages/时间线.html" class="nav-item">
                <span class="icon">📅</span>
                <span class="label">投资时间线</span>
            </a>
            <a href="{link_prefix}index-pages/关系网络.html" class="nav-item">
                <span class="icon">📊</span>
                <span class="label">关系网络</span>
            </a>
            <a href="{link_prefix}index-pages/概念关系图谱.html" class="nav-item">
                <span class="icon">🕸️</span>
                <span class="label">概念图谱</span>
            </a>
            <a href="{link_prefix}index-pages/知识树.html" class="nav-item">
                <span class="icon">🌳</span>
                <span class="label">知识树</span>
            </a>
            <a href="#" class="nav-item" id="searchBtn">
                <span class="icon">🔍</span>
                <span class="label">搜索</span>
            </a>
        </nav>
        
        <!-- Random Wisdom Module -->
        <div class="wisdom-module">
            <div class="wisdom-title">💭 随机智慧</div>
            <div class="wisdom-content">
                <p class="wisdom-quote" id="wisdomQuote">"护城河的本质是'我与别人不同'，而非'我比别人更好'。"</p>
                <a class="wisdom-source" id="wisdomSource" href="{link_prefix}concepts/护城河.html">— 护城河</a>
            </div>
            <button class="wisdom-refresh" id="wisdomRefresh">
                <span>🔄</span> 换一条
            </button>
        </div>
    </aside>
    
    <!-- Search Modal -->
    <div class="search-modal" id="searchModal">
        <div class="search-box">
            <input type="text" placeholder="搜索概念、公司、人物..." id="searchInput" autofocus>
            <p class="search-hint">按 ESC 或点击外部区域关闭</p>
        </div>
    </div>'''

def get_sidebar_css():
    """获取侧边栏CSS样式"""
    return '''
        /* Sidebar */
        .sidebar {
            position: fixed;
            left: 0;
            top: 0;
            height: 100vh;
            width: 60px;
            background: #1B2A4A;
            z-index: 1000;
            transition: width 0.3s ease;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .sidebar.expanded {
            width: 220px;
        }
        
        .sidebar-toggle {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            height: 60px;
            background: transparent;
            border: none;
            color: #C9A227;
            font-size: 1.5em;
            cursor: pointer;
            transition: all 0.2s;
            flex-shrink: 0;
        }
        
        .sidebar-toggle:hover {
            background: rgba(201, 162, 39, 0.2);
        }
        
        .sidebar-nav {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 10px 0;
        }
        
        .sidebar-nav::-webkit-scrollbar {
            width: 3px;
        }
        
        .sidebar-nav::-webkit-scrollbar-thumb {
            background: rgba(201, 162, 39, 0.3);
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            padding: 12px 15px;
            color: white;
            text-decoration: none;
            font-size: 0.95em;
            transition: all 0.2s;
            white-space: nowrap;
            overflow: hidden;
        }
        
        .nav-item .icon {
            font-size: 1.3em;
            width: 30px;
            flex-shrink: 0;
            text-align: center;
        }
        
        .nav-item .label {
            opacity: 0;
            margin-left: 12px;
            transition: opacity 0.2s;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .sidebar.expanded .nav-item .label {
            opacity: 1;
        }
        
        .nav-item:hover {
            background: rgba(201, 162, 39, 0.15);
            color: #C9A227;
        }
        
        .nav-item:hover .icon {
            transform: scale(1.1);
        }
        
        /* Wisdom Module */
        .wisdom-module {
            border-top: 1px solid rgba(201, 162, 39, 0.3);
            padding: 15px;
            background: rgba(0, 0, 0, 0.2);
            flex-shrink: 0;
            max-height: 200px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .wisdom-title {
            color: #C9A227;
            font-size: 0.85em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 6px;
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .sidebar.expanded .wisdom-title {
            opacity: 1;
        }
        
        .wisdom-content {
            flex: 1;
            overflow: hidden;
        }
        
        .wisdom-quote {
            color: white;
            font-size: 0.85em;
            line-height: 1.6;
            margin-bottom: 8px;
            opacity: 0;
            transition: opacity 0.2s;
            font-style: italic;
        }
        
        .sidebar.expanded .wisdom-quote {
            opacity: 1;
        }
        
        .wisdom-source {
            color: #C9A227;
            font-size: 0.8em;
            text-decoration: none;
            opacity: 0;
            transition: opacity 0.2s;
            display: block;
            cursor: pointer;
        }
        
        .sidebar.expanded .wisdom-source {
            opacity: 1;
        }
        
        .wisdom-source:hover {
            text-decoration: underline;
        }
        
        .wisdom-refresh {
            color: white;
            background: rgba(201, 162, 39, 0.2);
            border: 1px solid rgba(201, 162, 39, 0.4);
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.75em;
            cursor: pointer;
            margin-top: 10px;
            opacity: 0;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 5px;
        }
        
        .sidebar.expanded .wisdom-refresh {
            opacity: 1;
        }
        
        .wisdom-refresh:hover {
            background: rgba(201, 162, 39, 0.4);
        }
        
        /* Search Modal */
        .search-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            z-index: 2000;
            justify-content: center;
            align-items: flex-start;
            padding-top: 100px;
        }
        
        .search-modal.active {
            display: flex;
        }
        
        .search-box {
            background: white;
            border-radius: 12px;
            padding: 25px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .search-box input {
            width: 100%;
            padding: 15px;
            border: 2px solid #E5E0D8;
            border-radius: 8px;
            font-size: 1.1em;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }
        
        .search-box input:focus {
            border-color: #C9A227;
        }
        
        .search-hint {
            color: #5D6D7E;
            font-size: 0.85em;
            margin-top: 12px;
            text-align: center;
        }
        
        /* Main Content Wrapper */
        .main-wrapper {
            margin-left: 60px;
            transition: margin-left 0.3s ease;
        }
        
        .main-wrapper.sidebar-expanded {
            margin-left: 220px;
        }
        
        /* Mobile Overlay */
        .sidebar-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
        }
        
        .sidebar-overlay.active {
            display: block;
        }
        
        /* Mobile toggle button for small screens */
        .mobile-menu-btn {
            display: none;
            position: fixed;
            top: 70px;
            left: 10px;
            width: 44px;
            height: 44px;
            background: #1B2A4A;
            border: none;
            border-radius: 8px;
            color: #C9A227;
            font-size: 1.3em;
            cursor: pointer;
            z-index: 998;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        @media (max-width: 900px) {
            .mobile-menu-btn {
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .sidebar {
                transform: translateX(-100%);
                width: 220px;
            }
            .sidebar.mobile-open {
                transform: translateX(0);
            }
            .sidebar .nav-item .label,
            .sidebar .wisdom-title,
            .sidebar .wisdom-quote,
            .sidebar .wisdom-source,
            .sidebar .wisdom-refresh {
                opacity: 1;
            }
        }'''

def get_sidebar_js():
    """获取侧边栏JavaScript代码"""
    return '''
        <script>
        // Wisdom Data
        const wisdoms = [
            { quote: "护城河的本质是'我与别人不同'，而非'我比别人更好'。", source: "护城河", link: "concepts/护城河.html" },
            { quote: "安全边际不是用来'猜对'的，而是用来应对'猜错'的。", source: "安全边际", link: "concepts/安全边际.html" },
            { quote: "能力圈的核心是知道边界在哪里，而非范围有多大。", source: "能力圈", link: "concepts/能力圈.html" },
            { quote: "价格是你付出的，价值是你得到的。", source: "内在价值", link: "concepts/内在价值.html" },
            { quote: "别人恐惧时我贪婪，别人贪婪时我恐惧。", source: "市场先生", link: "concepts/市场先生.html" },
            { quote: "如果你不愿意持有一只股票十年，那就不要考虑持有它十分钟。", source: "长期持有", link: "concepts/长期持有.html" },
            { quote: "时间是优秀企业的朋友，是平庸企业的敌人。", source: "复利", link: "concepts/复利.html" },
            { quote: "风险来自于你不知道自己在做什么。", source: "风险", link: "concepts/风险.html" },
            { quote: "投资不需要极高的智商，需要的是稳定的情绪和独立思考的能力。", source: "投资者心理", link: "concepts/投资者心理.html" },
            { quote: "买入一家公司的股票，就是买入它的一部分生意。", source: "股东心态", link: "concepts/股东心态.html" }
        ];
        
        let currentWisdomIndex = 0;
        
        function showRandomWisdom() {
            currentWisdomIndex = Math.floor(Math.random() * wisdoms.length);
            const wisdom = wisdoms[currentWisdomIndex];
            document.getElementById('wisdomQuote').textContent = '"' + wisdom.quote + '"';
            document.getElementById('wisdomSource').textContent = '— ' + wisdom.source;
            document.getElementById('wisdomSource').href = wisdom.link;
        }
        
        // Initialize wisdom
        showRandomWisdom();
        
        // Refresh wisdom button
        document.getElementById('wisdomRefresh').addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            showRandomWisdom();
        });
        
        // Sidebar Toggle
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const toggleIcon = document.getElementById('toggleIcon');
        const mainWrapper = document.getElementById('mainWrapper');
        
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('expanded');
            mainWrapper.classList.toggle('sidebar-expanded');
            toggleIcon.textContent = sidebar.classList.contains('expanded') ? '✕' : '☰';
        });
        
        // Mobile Menu
        const mobileMenuBtn = document.getElementById('mobileMenuBtn');
        const sidebarOverlay = document.getElementById('sidebarOverlay');
        
        function openMobileMenu() {
            sidebar.classList.add('mobile-open');
            sidebarOverlay.classList.add('active');
        }
        
        function closeMobileMenu() {
            sidebar.classList.remove('mobile-open');
            sidebarOverlay.classList.remove('active');
        }
        
        mobileMenuBtn.addEventListener('click', function() {
            if (sidebar.classList.contains('mobile-open')) {
                closeMobileMenu();
            } else {
                openMobileMenu();
            }
        });
        
        sidebarOverlay.addEventListener('click', closeMobileMenu);
        
        // Close mobile menu when clicking nav items
        document.querySelectorAll('.nav-item').forEach(function(item) {
            item.addEventListener('click', function() {
                if (window.innerWidth <= 900) {
                    closeMobileMenu();
                }
            });
        });
        
        // Search Modal
        const searchBtn = document.getElementById('searchBtn');
        const searchModal = document.getElementById('searchModal');
        const searchInput = document.getElementById('searchInput');
        
        searchBtn.addEventListener('click', function(e) {
            e.preventDefault();
            searchModal.classList.add('active');
            setTimeout(function() {
                searchInput.focus();
            }, 100);
        });
        
        searchModal.addEventListener('click', function(e) {
            if (e.target === searchModal) {
                searchModal.classList.remove('active');
            }
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                searchModal.classList.remove('active');
                closeMobileMenu();
            }
        });
        
        // Handle window resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 900) {
                closeMobileMenu();
            }
        });
        </script>'''

def process_file(filepath, link_prefix):
    """处理单个HTML文件，添加侧边栏"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已经包含侧边栏（避免重复处理）
        if 'class="sidebar"' in content and 'id="sidebar"' in content:
            print(f"  ⏭️  跳过（已包含侧边栏）: {filepath}")
            return False
        
        # 1. 添加侧边栏CSS到<style>标签中
        sidebar_css = get_sidebar_css()
        # 在 </style> 标签前添加
        content = content.replace('</style>', sidebar_css + '\n    </style>')
        
        # 2. 添加侧边栏HTML到<body>标签后
        sidebar_html = get_sidebar_html(link_prefix)
        content = content.replace('<body>', '<body>\n' + sidebar_html)
        
        # 3. 修改页面结构：
        #    - 将原有内容包裹在 <div class="main-wrapper"> 中
        #    - 删除原有的 <nav class="nav">
        
        # 删除原有的顶部导航栏 <nav class="nav">...</nav>
        nav_pattern = r'\s*<nav class="nav">.*?</nav>\s*'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        # 如果有 <div class="container">，在其前面加上 main-wrapper
        # 找到 header 的结束位置，然后在 header 后面添加 main-wrapper 开始标签
        header_end_pattern = r'(</header>)'
        content = re.sub(header_end_pattern, r'\1\n    <div class="main-wrapper" id="mainWrapper">', content)
        
        # 在 footer 前添加 main-wrapper 结束标签
        # 找到 </footer>，在它前面添加
        footer_pattern = r'(</footer>\s*</body>)'
        content = re.sub(footer_pattern, r'</div>\n    \1', content)
        
        # 4. 在 </body> 前添加 JavaScript
        sidebar_js = get_sidebar_js()
        content = content.replace('</body>', sidebar_js + '\n</body>')
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ 已处理: {filepath}")
        return True
        
    except Exception as e:
        print(f"  ❌ 处理失败: {filepath} - {str(e)}")
        return False

def get_link_prefix(dirname):
    """根据目录确定链接前缀"""
    if dirname == 'index-pages':
        return ''
    else:
        return '../'

def main():
    """主函数"""
    base_path = BASE_PATH
    
    # 要处理的目录和文件类型
    directories = ['concepts', 'companies', 'people', 'index-pages']
    
    total_processed = 0
    total_skipped = 0
    
    for dirname in directories:
        dir_path = os.path.join(base_path, dirname)
        if not os.path.exists(dir_path):
            print(f"⚠️ 目录不存在: {dir_path}")
            continue
        
        print(f"\n📂 处理目录: {dirname}")
        
        # 获取所有HTML文件（排除README.md）
        html_files = []
        for filename in os.listdir(dir_path):
            if filename.endswith('.html'):
                filepath = os.path.join(dir_path, filename)
                html_files.append((filename, filepath))
        
        html_files.sort()
        
        link_prefix = get_link_prefix(dirname)
        count = 0
        
        for filename, filepath in html_files:
            result = process_file(filepath, link_prefix)
            if result:
                count += 1
            else:
                total_skipped += 1
        
        total_processed += count
        print(f"  📊 {dirname} 目录: 处理了 {count} 个文件")
    
    print(f"\n{'='*50}")
    print(f"🎉 处理完成！")
    print(f"   - 新增侧边栏: {total_processed} 个文件")
    print(f"   - 跳过（已处理）: {total_skipped} 个文件")

if __name__ == '__main__':
    main()
