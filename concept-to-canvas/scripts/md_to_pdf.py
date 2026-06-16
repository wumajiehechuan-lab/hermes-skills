#!/usr/bin/env python3
"""
商业方案骨架 Markdown → PDF 转换脚本

用法:
  python md_to_pdf.py input.md output.pdf [--title "项目名称"] [--author "作者"]

依赖: pip install markdown

渲染引擎（按优先级自动检测）:
  1. WeasyPrint — 有 GTK 系统库时使用（Linux/macOS/部分Windows）
  2. Chrome headless — 系统有 Chrome 时使用（实测 Windows 可用）
  3. 均不可用时报错提示
"""

import sys
import os
import re
import argparse
import subprocess
import shutil
import markdown

# ── CSS 样式 ──
CSS_TEMPLATE = """
@page {
    size: A4;
    margin: 25mm 20mm 20mm 20mm;

    @top-center {
        content: "HEADER_TEXT";
        font-family: "Droid Sans Fallback", Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #95a5a6;
        border-bottom: 0.5pt solid #ecf0f1;
        padding-bottom: 3mm;
    }

    @bottom-center {
        content: "第 " counter(page) " 页";
        font-family: "Droid Sans Fallback", Helvetica, Arial, sans-serif;
        font-size: 8pt;
        color: #95a5a6;
        border-top: 0.8pt solid #e67e22;
        padding-top: 2mm;
    }
}

@page :first {
    @top-center { content: none; }
    @bottom-center { content: none; }
}

body {
    font-family: "Droid Sans Fallback", Helvetica, Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.75;
    color: #2c3e50;
    text-align: justify;
}

/* 封面 */
.cover {
    page-break-after: always;
    text-align: center;
    padding-top: 40%;
}
.cover h1 {
    font-size: 26pt;
    color: #e67e22;
    margin-bottom: 6mm;
    font-weight: bold;
    letter-spacing: 2pt;
}
.cover .subtitle {
    font-size: 13pt;
    color: #7f8c8d;
    margin-bottom: 4mm;
}
.cover .meta {
    font-size: 10pt;
    color: #95a5a6;
    margin-bottom: 3mm;
}
.cover .divider {
    width: 50%;
    margin: 8mm auto;
    border: none;
    border-top: 1.5pt solid #e67e22;
}
.cover .status-badge {
    display: inline-block;
    padding: 3mm 8mm;
    margin-top: 6mm;
    background: #fef9e7;
    border: 1pt solid #f39c12;
    border-radius: 4pt;
    color: #e67e22;
    font-size: 10pt;
    font-weight: bold;
}

/* 一级标题 */
h1 {
    font-size: 18pt;
    color: #2c3e50;
    margin-top: 14mm;
    margin-bottom: 5mm;
    padding-bottom: 3mm;
    border-bottom: 2pt solid #e67e22;
    page-break-before: always;
    font-weight: bold;
}
h1:first-of-type {
    page-break-before: avoid;
}

h2 {
    font-size: 13pt;
    color: #2980b9;
    margin-top: 8mm;
    margin-bottom: 4mm;
    font-weight: bold;
}

h3 {
    font-size: 11pt;
    color: #27ae60;
    margin-top: 5mm;
    margin-bottom: 3mm;
    font-weight: bold;
}

h4 {
    font-size: 10.5pt;
    color: #8e44ad;
    margin-top: 4mm;
    margin-bottom: 2mm;
    font-weight: bold;
}

p {
    margin-top: 1.5mm;
    margin-bottom: 1.5mm;
    orphans: 3;
    widows: 3;
}

/* 引用块 */
blockquote {
    margin: 4mm 0;
    padding: 4mm 4mm 4mm 10mm;
    background: #f8f9fa;
    border-left: 3pt solid #e67e22;
    color: #5d6d7e;
    font-size: 10pt;
}
blockquote p {
    margin: 1mm 0;
}

strong, b {
    font-weight: bold;
    color: #1a252f;
}

code {
    font-family: "Courier New", Courier, monospace;
    background: #fdf2e9;
    color: #c0392b;
    padding: 0.5mm 1.5mm;
    border-radius: 2pt;
    font-size: 9.5pt;
}

pre {
    background: #2c3e50;
    color: #ecf0f1;
    padding: 4mm;
    border-radius: 3pt;
    font-size: 9pt;
    line-height: 1.4;
    overflow-x: auto;
    page-break-inside: avoid;
}
pre code {
    background: transparent;
    color: inherit;
    padding: 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 4mm 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
thead th {
    background: #2c3e50;
    color: white;
    padding: 3mm;
    text-align: left;
    font-weight: bold;
}
tbody td {
    padding: 2.5mm 3mm;
    border-bottom: 0.5pt solid #bdc3c7;
    vertical-align: top;
}
tbody tr:nth-child(even) {
    background: #f8f9fa;
}

hr {
    border: none;
    border-top: 0.5pt solid #bdc3c7;
    margin: 4mm 0;
}

ul, ol {
    margin: 2mm 0;
    padding-left: 8mm;
}
li {
    margin-bottom: 1mm;
}

a {
    color: #2980b9;
    text-decoration: none;
}
"""


def md_to_html(md_text, title="商业方案骨架",
               subtitle="精益画布(Lean Canvas) + 价值主张画布(VPC)",
               meta_line="", author="四喜", status="待验证"):
    """将 Markdown 转为带封面的 HTML"""

    html_body = markdown.markdown(
        md_text,
        extensions=['tables', 'fenced_code', 'nl2br'],
        output_format='html5'
    )

    # 移除正文中的第一个 h1（会用在封面上）
    first_h1_match = re.search(r'<h1>(.*?)</h1>', html_body)
    if first_h1_match:
        extracted_title = first_h1_match.group(1)
        if not title or title == "商业方案骨架":
            title = extracted_title
        html_body = html_body.replace(first_h1_match.group(0), '', 1)

    css = CSS_TEMPLATE.replace("HEADER_TEXT", f"{title}  |  商业方案骨架")

    cover_html = f"""
    <div class="cover">
        <h1 style="page-break-before: avoid; border: none; page-break-after: avoid;">{title}</h1>
        <div class="subtitle">{subtitle}</div>
        {f"<div class='meta'>{meta_line}</div>" if meta_line else ""}
        <hr class="divider">
        <div class="meta">作者: {author}</div>
        <div class="status-badge">🟡 状态: {status} — 以下内容均为假设，需验证</div>
    </div>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>{css}</style>
</head>
<body>
{cover_html}
{html_body}
</body>
</html>"""
    return full_html


def find_chrome():
    """查找系统 Chrome/Chromium 可执行文件路径"""
    # Windows 常见路径
    win_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Chromium\Application\chrome.exe",
    ]
    if sys.platform == "win32":
        for path in win_paths:
            expanded = os.path.expandvars(path)
            if os.path.isfile(expanded):
                return expanded
    # PATH 搜索
    return shutil.which("google-chrome") or shutil.which("chrome") or shutil.which("chromium")


def render_with_chrome(html_path, output_path):
    """用 Chrome headless 将 HTML 渲染为 PDF"""
    chrome = find_chrome()
    if not chrome:
        return False

    abs_html = os.path.abspath(html_path)
    abs_output = os.path.abspath(output_path)

    try:
        result = subprocess.run(
            [chrome, "--headless", "--disable-gpu",
             "--no-margins", "--print-to-pdf-no-header",
             f"--print-to-pdf={abs_output}",
             f"file:///{abs_html.replace(os.sep, '/')}"],
            capture_output=True, text=True, timeout=30
        )
        if os.path.isfile(abs_output) and os.path.getsize(abs_output) > 1000:
            return True
        return False
    except Exception:
        return False


def render_with_weasyprint(html, output_path):
    """用 WeasyPrint 渲染 PDF"""
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(output_path)
        return True
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="商业方案骨架 Markdown → PDF")
    parser.add_argument("input", help="输入的 Markdown 文件路径")
    parser.add_argument("output", help="输出的 PDF 文件路径")
    parser.add_argument("--title", default=None, help="项目名称 / 报告标题（默认从 Markdown 第一个 H1 提取）")
    parser.add_argument("--author", default="四喜", help="作者名")
    parser.add_argument("--status", default="待验证", help="方案状态标签（如：待验证/已验证/迭代中）")
    parser.add_argument("--keep-html", action="store_true", help="保留中间 HTML 文件（默认清理）")
    parser.add_argument("--engine", choices=["auto", "weasyprint", "chrome"],
                        default="auto", help="PDF 渲染引擎（默认 auto：WeasyPrint → Chrome fallback）")
    args = parser.parse_args()

    # 读取 Markdown
    with open(args.input, "r", encoding="utf-8") as f:
        md_text = f.read()

    # 提取元信息
    meta_line = ""
    for line in md_text.split("\n"):
        stripped = line.strip().lstrip(">").strip()
        if "生成时间" in stripped or "方法论" in stripped or "状态" in stripped:
            meta_line = stripped
            break

    # 自动推断标题
    inferred_title = None
    for line in md_text.split("\n"):
        if line.startswith("# ") and not line.startswith("##"):
            inferred_title = line[2:].strip()
            break
    final_title = args.title or inferred_title or "商业方案骨架"

    # 生成 HTML
    html = md_to_html(md_text, title=final_title, meta_line=meta_line,
                      author=args.author, status=args.status)

    html_path = args.output.replace('.pdf', '.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] HTML 已生成: {html_path}")

    # 渲染 PDF
    success = False
    engine_used = None

    if args.engine in ("auto", "weasyprint"):
        if render_with_weasyprint(html, args.output):
            success = True
            engine_used = "WeasyPrint"

    if not success and args.engine in ("auto", "chrome"):
        if render_with_chrome(html_path, args.output):
            success = True
            engine_used = "Chrome headless"

    if success:
        size_kb = os.path.getsize(args.output) / 1024
        print(f"[OK] PDF 已生成: {args.output} ({size_kb:.1f} KB) [引擎: {engine_used}]")
        if not args.keep_html:
            os.remove(html_path)
            print(f"[OK] 中间 HTML 已清理（加 --keep-html 保留）")
    else:
        print(f"[WARN] PDF 渲染失败。可用的引擎: WeasyPrint {'(已安装)' if 'weasyprint' in sys.modules else '(未安装)'}, "
              f"Chrome: {'找到' if find_chrome() else '未找到'}")
        print(f"[HINT] HTML 文件已保存到 {html_path}，可用浏览器打开后打印为 PDF")
        sys.exit(1)


if __name__ == "__main__":
    main()
