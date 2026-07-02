import argparse
import html
import json
import re
import sys
from pathlib import Path

from docx import Document

HEADERS = ["来源", "商品中文名称", "型号", "产品名称（英文）", "URL", "简介", "产品详情", "代码", "网站分类", "主图", "详情图", "图片文件名", "alt text", "title", "Caption", "价格", "💲", "是否上传"]
DEFAULT_SOURCES = [
    ("加热搅拌全部产品", "Atomfair_heating_stirring_HTML"),
    ("温控系列全部产品", "温控系列全部产品"),
    ("蒸馏系列全部产品", "Atomfair_distillation_HTML"),
]

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(value or "")).strip()


def strip_tags(value):
    return clean_text(re.sub(r"<[^>]+>", " ", value or ""))


def read_docx_text(path):
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()


def read_html_text(path):
    if path.suffix.lower() in (".html", ".htm"):
        return path.read_text(encoding="utf-8", errors="ignore").strip()
    return read_docx_text(path)


def find_overview(text):
    overview_match = re.search(r"<h2[^>]*>\s*Complete\s+Product\s+Description\s*</h2>(.*?)(?:</section>|<section\b|<h2\b)", text, re.I | re.S) or re.search(r"<h2[^>]*>\s*Product\s+Overview\s*</h2>(.*?)(?:</section>|<section\b|<h2\b)", text, re.I | re.S)
    if not overview_match:
        return ""
    block = overview_match.group(1)
    paras = re.findall(r"<p[^>]*>(.*?)</p>", block, re.I | re.S)
    overview = "\n\n".join(strip_tags(p) for p in paras if strip_tags(p))
    return overview or strip_tags(block)


def record_from_file(path, sheet_name, text):
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.I | re.S)
    product_en = strip_tags(h1.group(1)) if h1 else ""
    model_match = re.search(r"<div[^>]*class\s*=\s*['\"]?model['\"]?[^>]*>(.*?)</div>", text, re.I | re.S)
    model_text = strip_tags(model_match.group(1)) if model_match else ""
    model_text = re.sub(r"^(Atomfair\s+)?Model\s*:\s*", "", model_text, flags=re.I).strip()
    return {
        "来源": "",
        "商品中文名称": path.stem,
        "型号": model_text,
        "产品名称（英文）": product_en,
        "URL": "",
        "简介": find_overview(text),
        "产品详情": "",
        "代码": text,
        "网站分类": "",
        "主图": "",
        "详情图": "",
        "图片文件名": "",
        "alt text": "",
        "title": "",
        "Caption": "",
        "价格": "",
        "💲": "",
        "是否上传": "",
    }


def eligible_files(folder):
    suffixes = {".docx", ".html", ".htm"}
    return sorted(
        [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in suffixes and not p.name.startswith("~$")],
        key=lambda p: str(p.relative_to(folder)).lower(),
    )


def parse_sources(values):
    if not values:
        return DEFAULT_SOURCES
    sources = []
    for value in values:
        if "=" in value:
            sheet_name, folder_name = value.split("=", 1)
        else:
            sheet_name = folder_name = value
        sources.append((sheet_name.strip(), folder_name.strip()))
    return sources


def main():
    parser = argparse.ArgumentParser(description="Extract generated HTML records for Excel.")
    parser.add_argument("--html-root", default=r"C:\Users\hz-user\Desktop\大龙")
    parser.add_argument("--out", default=str(Path(__file__).with_name("html_records.json")))
    parser.add_argument("--sources", nargs="*", help="Use SheetName=FolderName. FolderName can also be an absolute path.")
    args = parser.parse_args()

    html_root = Path(args.html_root)
    payload = []
    for sheet_name, folder_name in parse_sources(args.sources):
        folder_path = Path(folder_name)
        folder = folder_path if folder_path.is_absolute() else html_root / folder_name
        if not folder.exists():
            payload.append({"sheetName": sheet_name, "folder": str(folder), "records": [], "warning": "folder not found"})
            continue
        records = []
        for path in eligible_files(folder):
            try:
                text = read_html_text(path)
                if text:
                    records.append(record_from_file(path, sheet_name, text))
            except Exception as exc:
                record = {h: "" for h in HEADERS}
                record["来源"] = ""
                record["商品中文名称"] = path.stem
                record["产品详情"] = f"读取失败: {exc}"
                records.append(record)
        payload.append({"sheetName": sheet_name, "folder": str(folder), "records": records})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(out), "sheets": [{"name": g["sheetName"], "folder": g["folder"], "count": len(g["records"])} for g in payload]}, ensure_ascii=False))


if __name__ == "__main__":
    main()



