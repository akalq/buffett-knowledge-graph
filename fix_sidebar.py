import os
import re

base_dir = "."
target_strings = [
    ".sidebar.expanded .nav-item .label {",
]

insert_css = """/* 侧边栏收起时图标居中 */
.sidebar:not(.expanded) .nav-item {
    padding: 12px 0;
    justify-content: center;
}

"""

count = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for target in target_strings:
                    if target in content:
                        if ".sidebar:not(.expanded) .nav-item" not in content:
                            new_content = content.replace(target, insert_css + target)
                            with open(filepath, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                            count += 1
                            print(f"✓ 修改: {filepath}")
                        else:
                            print(f"⏭ 已存在: {filepath}")
                        break
            except Exception as e:
                print(f"✗ 错误 {filepath}: {e}")

print(f"\n总计修改 {count} 个文件")
