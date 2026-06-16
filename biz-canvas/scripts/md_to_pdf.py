#!/usr/bin/env python3
"""
biz-canvas 商业模式五维分析报告 — Markdown → HTML → PDF 转换脚本

用法:
  python md_to_pdf.py input.md output.pdf [--title "报告标题"] [--author "作者"]

依赖:
  pip install markdown

流程:
  1. 读取 Markdown 输入文件
  2. 转为带排版的 HTML（内嵌 CSS）
  3. 调用系统 Chrome headless 模式将 HTML 打印为 PDF
  4. 清理临时 HTML（可选）

Chrome 路径自动检测: Windows / macOS / Linux
"""

import sys
import os
import re
import argparse
import subprocess
import platform


# ── CSS 样式 ──
CSS_STYLE = """
body {
    font-family: "Microsoft YaHei", "Droid Sans Fallback", Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #2c3e50;
    max-width: 900px;
    margin: 40px auto;
    padding: 0 20px;
}
h1 {
    color: #1a5276;
    border-bottom: 2pt solid #1a5276;
    padding-bottom: 8px;
    font-size: 22pt;
}
h2 {
    color: #1e8449;
    margin-top: 30px;
    font-size: 16pt;
}
h3 {
    color: #2e86c1;
    font-size: 13pt;
}
h4 {
    color: #5b2c6f;
    font-size: 11.5pt;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 10.5pt;
}
th {
    background: #1a5276;
    color: white;
    padding: 8px;
    text-align: left;
    font-weight: bold;
}
td {
    padding: 8px;
    border-bottom: 1px solid #bdc3c7;
}
tr:nth-child(even) {
    background: #f8f9fa;
}
blockquote {
    border-left: 3px solid #1a5276;
    background: #f8f9fa;
    padding: 8px 16px;
    margin: 16px 0;
    color: #5d6d7e;
}
code {
    background: #fdf2e9;
    color: #c0392b;
    padding: 2px 6px;
    border-radius: 2px;
    font-size: 10pt;
}
pre {
    background: #f8f9fa;
    border-left: 3px solid #1a5276;
    padding: 12px;
    overflow-x: auto;
    font-size: 9.5pt;
}
hr {
    border: none;
    border-top: 1px solid #bdc3c7;
    margin: 24px 0;
}
strong {
    color: #1a252f;
}
a {
    color: #2e86c1;
    text-decoration: none;
}
"""


def find_chrome():
    """自动检测系统 Chrome 路径"""
    system = platform.system()
    candidates = []

    if system == "Windows":
        candidates = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]
        # 也检查注册表
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                 r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
            reg_path = winreg.QueryValue(key, None)
            if reg_path:
                candidates.insert(0, reg_path)
        except Exception:
            pass
    elif system == "Darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
    else:  # Linux
        candidates = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ]

    for path in candidates:
        if os.path.isfile(path):
            return path

    return None


def md_to_html(md_text, title="商业模式五维分析"):
    """将 Markdown 转为带排版的 HTML"""
    import markdown

    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br'],
        output_format='html5'
    )

    # 提取标题
    first_h1 = re.search(r'<h1>(.*?)</h1>', html_body)
    if first_h1 and title == "商业模式五维分析":
        title = first_h1.group(1)

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{CSS_STYLE}</style>
</head>
<body>
{html_body}
</body>
</html>"""
    return full_html


def main():
    parser = argparse.ArgumentParser(description="biz-canvas 报告 MD → HTML → PDF")
    parser.add_argument("input", help="输入的 Markdown 文件路径")
    parser.add_argument("output", help="输出的 PDF 文件路径")
    parser.add_argument("--title", default="商业模式五维分析", help="报告标题")
    parser.add_argument("--author", default="四喜", help="作者名")
    parser.add_argument("--keep-html", action="store_true", help="保留中间 HTML 文件")
    args = parser.parse_args()

    # 1. 读取 Markdown
    with open(args.input, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 2. 转为 HTML
    html = md_to_html(md_text, title=args.title)

    # 保存 HTML
    html_path = args.output.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML 已生成: {html_path}")

    # 3. 转 PDF（Chrome headless）
    chrome_path = find_chrome()
    if not chrome_path:
        print(f"[WARN] 未找到 Chrome 浏览器，仅生成了 HTML 文件: {html_path}")
        print("[HINT] 手动用浏览器打开 HTML 文件，按 Ctrl+P 打印为 PDF")
        sys.exit(0)

    # 获取 HTML 的绝对路径（Chrome 需要 file://）
    abs_html = os.path.abspath(html_path)
    file_url = f"file:///{abs_html.replace(os.sep, '/')}"

    cmd = [
        chrome_path,
        "--headless", "--disable-gpu",
        "--no-margins", "--print-to-pdf-no-header",
        f"--print-to-pdf={os.path.abspath(args.output)}",
        file_url,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if os.path.isfile(args.output):
        size_kb = os.path.getsize(args.output) / 1024
        print(f"[OK] PDF 已生成: {args.output} ({size_kb:.1f} KB)")
    else:
        print(f"[ERR] PDF 生成失败")
        print(result.stderr)
        sys.exit(1)

    # 4. 清理 HTML（默认删除）
    if not args.keep_html and os.path.isfile(html_path):
        os.remove(html_path)
        print(f"[OK] 中间 HTML 已清理")


if __name__ == "__main__":
    main()
