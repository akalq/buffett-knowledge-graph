#!/usr/bin/env python3
import os
import re
from pathlib import Path

BASE_DIR = Path("./投资研究/知识库/巴菲特知识库-LearnBuffett版/letters/berkshire")
OUTPUT_FILE = Path("./投资研究/知识库/巴菲特知识库-LearnBuffett版/check_results.md")

results = []
normal_count = 0
problem_count = 0
problem_years = []

for year in range(1977, 2025):
    file_path = BASE_DIR / f"{year}.html"
    result = {"year": year, "status": "normal", "issues": [], "warnings": []}
    
    if not file_path.exists():
        result["status"] = "problem"
        result["issues"].append("文件不存在")
        problem_count += 1
        problem_years.append(f"{year}: 文件不存在")
        results.append(result)
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_size = os.path.getsize(file_path)
    result["file_size"] = file_size
    
    # 提取标题
    title_match = re.search(r'<title>([^<]*)</title>', content)
    result["title"] = title_match.group(1) if title_match else "无标题"
    
    # 统计关键元素
    bilingual_count = len(re.findall(r'bilingual-block', content))
    lang_block_count = len(re.findall(r'class="lang-block', content))
    lang_cn_count = len(re.findall(r'class="[^"]*lang-cn', content))
    lang_en_count = len(re.findall(r'class="[^"]*lang-en', content))
    berkshire_count = len(re.findall(r'伯克希尔', content))
    pending_count = len(re.findall(r'翻译待完成', content))
    
    result["bilingual_count"] = bilingual_count
    result["lang_block_count"] = lang_block_count
    result["lang_cn_count"] = lang_cn_count
    result["lang_en_count"] = lang_en_count
    result["berkshire_count"] = berkshire_count
    result["pending_count"] = pending_count
    
    # 检查问题 - 更宽松的判断标准
    # 1. 要么有bilingual-block，要么有lang-block结构
    has_bilingual_structure = bilingual_count > 0 or (lang_block_count > 0 and lang_cn_count > 0)
    
    if not has_bilingual_structure:
        result["status"] = "problem"
        result["issues"].append("缺少双语结构(bilingual-block或lang-block)")
    
    if pending_count > 0:
        result["status"] = "problem"
        result["issues"].append(f"存在{pending_count}处'翻译待完成'")
    
    if berkshire_count == 0:
        result["status"] = "problem"
        result["issues"].append("缺少中文内容(伯克希尔)")
    
    # 检查结构差异警告
    if bilingual_count > 0 and lang_block_count == 0:
        result["structure"] = "标准bilingual-block结构"
    elif bilingual_count == 0 and lang_block_count > 0:
        result["structure"] = "lang-block结构"
        result["warnings"].append("使用旧版lang-block结构")
    elif bilingual_count > 0 and lang_block_count > 0:
        result["structure"] = "混合结构"
        result["warnings"].append("混合使用两种结构")
    
    if result["status"] == "problem":
        problem_count += 1
        problem_years.append(f"{year}: {', '.join(result['issues'])}")
    else:
        normal_count += 1
    
    results.append(result)

# 生成报告
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("# 巴菲特知识库信件检查报告\n\n")
    f.write(f"检查时间: {os.popen('date').read().strip()}\n\n")
    
    f.write("## 检查标准\n\n")
    f.write("1. 文件存在\n")
    f.write("2. 有双语结构（bilingual-block 或 lang-block + lang-cn + lang-en）\n")
    f.write("3. 不存在'翻译待完成'标记\n")
    f.write("4. 包含中文内容（伯克希尔等词汇）\n\n")
    
    f.write("## 详细结果\n\n")
    
    for r in results:
        status_icon = "✅" if r["status"] == "normal" else "❌"
        structure = r.get("structure", "未知")
        f.write(f"### {r['year']}年 - {status_icon} ({structure})\n")
        f.write(f"- 文件大小: {r.get('file_size', 'N/A')} bytes\n")
        f.write(f"- 页面标题: {r.get('title', 'N/A')}\n")
        f.write(f"- bilingual-block数量: {r.get('bilingual_count', 0)}\n")
        f.write(f"- lang-block数量: {r.get('lang_block_count', 0)}\n")
        f.write(f"- lang-cn元素数量: {r.get('lang_cn_count', 0)}\n")
        f.write(f"- lang-en元素数量: {r.get('lang_en_count', 0)}\n")
        f.write(f"- 包含'伯克希尔': {r.get('berkshire_count', 0)}\n")
        f.write(f"- 包含'翻译待完成': {r.get('pending_count', 0)}\n")
        if r.get("warnings"):
            f.write(f"- ⚠️ 警告: {', '.join(r['warnings'])}\n")
        if r.get("issues"):
            f.write(f"- ❌ 问题: {', '.join(r['issues'])}\n")
        f.write("\n")
    
    f.write("---\n\n")
    f.write("## 总结\n\n")
    f.write(f"- 检查年份: 1977-2024年，共48年\n")
    f.write(f"- ✅ 正常年份: {normal_count} 年\n")
    f.write(f"- ❌ 有问题年份: {problem_count} 年\n\n")
    
    if problem_years:
        f.write("### 有问题年份详细列表\n\n")
        for item in problem_years:
            f.write(f"- {item}\n")
    else:
        f.write("所有年份信件均正常！\n")

print(f"检查完成！结果已保存到: {OUTPUT_FILE}")
print(f"\n总结:")
print(f"- 正常年份: {normal_count} 年")
print(f"- 有问题年份: {problem_count} 年")
if problem_years:
    print("\n有问题年份:")
    for item in problem_years:
        print(f"  - {item}")
