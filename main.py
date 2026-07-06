import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from docx import Document
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill, Border, Side

HEADERS = [
    "来源", "商品中文名称", "型号", "产品名称（英文）", "URL", "简介", "产品详情", "代码", "网站分类",
    "主图", "详情图", "图片文件名", "alt text", "title", "Caption", "价格", "💲", "是否上传"
]

SUPPORTED_EXTENSIONS = {".docx", ".txt", ".md", ".csv", ".xlsx"}

FORBIDDEN_MARKETING_PHRASES = [
    "separate from the family record",
    "separated from the family record",
    "separate ordering product",
    "independent ordering product",
    "keeps the source product name",
    "source product name",
    "unified order model",
    "uniform order model",
    "listed separately",
]


def html_escape(value: Any) -> str:
    import html
    return html.escape(str(value or ""), quote=True)


def read_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def extract_docx_text(path: Path) -> str:
    doc = Document(path)
    parts: list[str] = []
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            parts.append(text)
    for table_index, table in enumerate(doc.tables, 1):
        parts.append(f"\n[TABLE {table_index}]")
        for row in table.rows:
            cells = [cell.text.strip().replace("\n", " / ") for cell in row.cells]
            if any(cells):
                parts.append(" | ".join(cells))
    return "\n".join(parts)


def extract_xlsx_text(path: Path) -> str:
    workbook = load_workbook(path, read_only=True, data_only=True)
    parts: list[str] = []
    for sheet in workbook.worksheets:
        parts.append(f"\n[SHEET {sheet.title}]")
        for row in sheet.iter_rows(values_only=True):
            values = [str(cell).strip() if cell is not None else "" for cell in row]
            if any(values):
                parts.append(" | ".join(values))
    return "\n".join(parts)


def extract_plain_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_manual_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".docx":
        return extract_docx_text(path)
    if suffix == ".xlsx":
        return extract_xlsx_text(path)
    if suffix in {".txt", ".md", ".csv"}:
        return extract_plain_text(path)
    raise ValueError(f"Unsupported input type: {path}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}")


def cjk_exists(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text or ""))


def has_forbidden_phrase(text: str) -> str | None:
    lowered = (text or "").lower()
    for phrase in FORBIDDEN_MARKETING_PHRASES:
        if phrase in lowered:
            return phrase
    return None


def safe_json_from_text(text: str) -> list[dict[str, Any]]:
    text = text.strip()
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, flags=re.S)
    if fenced:
        text = fenced.group(1).strip()
    start = text.find("[")
    end = text.rfind("]")
    if start >= 0 and end > start:
        text = text[start:end + 1]
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("AI response must be a JSON array.")
    return data


def build_prompt(source_text: str, brand: str, model_prefix: str) -> str:
    return f"""
You convert laboratory product manuals into ecommerce upload records.

Strict rules:
- Return JSON only, no markdown.
- HTML and all English fields must be English only.
- Keep Chinese product names from the manual in chinese_name.
- If a source product name contains another manufacturer or brand, replace it with {brand}.
- Do not invent product names.
- Every different product specification, capacity, channel count, volume range, rotor, module, accessory or spare part must become a separate item.
- If one product family has 8-channel, 12-channel, 16-channel or other channel variants, each channel variant and range is a separate item.
- Do not summarize multiple ranges into one generic range. Do not borrow ranges, accuracy tables or specifications from another family.
- Each item may use only the parameter table, ordering table and description that belong to the same source product family or heading.
- Preserve all parameters, specifications, dimensions, capacities, ranges, increments, accuracy values, precision values, power values, speed ranges, temperature ranges, compatibility data, accessories and ordering data.
- Accessories are products too. Every listed accessory, adapter, module, electrode, rotor, rack, block, cable or spare part must be represented as its own item when it can be ordered separately.
- Product Overview must be professionally expanded into 2 to 3 rigorous paragraphs. Mention suitable research or laboratory application scenarios only when supported by the source text and product type.
- Do not write meta explanations such as "this row is separated", "keeps the source product name", "unified order model" or similar internal workflow language.
- If a value is not specified in the source, write "Not specified" rather than guessing.
- source_column must always be an empty string.
- atomfair_model must be unique and start with {model_prefix}-.

Return a JSON array. Each item must have:
{{
  "chinese_name": "...",
  "atomfair_model": "{model_prefix}-...",
  "english_name": "...",
  "category": "...",
  "product_type": "...",
  "overview_paragraphs": ["...", "..."],
  "features": ["...", "..."],
  "specifications": [{{"parameter":"...", "value":"..."}}],
  "accessories": [{{"name":"...", "reference_code":"", "specification":"...", "compatibility":"..."}}],
  "ordering_rows": [{{"order_model":"...", "source_model":"...", "key_specification":"...", "application":"..."}}],
  "source_evidence": ["short source heading/table reference used for this item"]
}}

Manual text:
{source_text}
""".strip()


def call_openai(prompt: str, model: str) -> str:
    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("OpenAI Python package is not installed. Run: pip install -r requirements.txt") from exc
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and fill in your key.")
    client = OpenAI()
    if hasattr(client, "responses"):
        response = client.responses.create(model=model, input=prompt)
        return response.output_text
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content or ""


def table(headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(
        f'<th style="background:#111;color:#fff;border:1px solid #111;padding:11px 12px;text-align:left;">{html_escape(h)}</th>'
        for h in headers
    )
    body = []
    for row in rows:
        cells = []
        for index, cell in enumerate(row):
            weight = "font-weight:700;" if index == 0 else ""
            cells.append(f'<td style="border:1px solid #d7d7d7;padding:10px 12px;{weight}vertical-align:top;">{html_escape(cell)}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<table style="border-collapse:collapse;border:1px solid #111;font-size:14px;" border="0" width="100%" cellspacing="0" cellpadding="0"><thead><tr>{th}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def section(title: str, body: str) -> str:
    return f'<table style="margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody><tr><td style="border-left:5px solid #111;padding-left:15px;padding-bottom:12px;"><h2 style="margin:0;font-size:18px;color:#111;text-transform:uppercase;font-weight:800;">{html_escape(title)}</h2></td></tr><tr><td style="padding-top:18px;">{body}</td></tr></tbody></table>'


def product_html(item: dict[str, Any], brand: str) -> str:
    overview = item.get("overview_paragraphs") or []
    features = item.get("features") or []
    specs = item.get("specifications") or []
    accessories = item.get("accessories") or []
    ordering = item.get("ordering_rows") or []

    parts = [
        '<!-- Atomfair Complete Product HTML - Full-English Release -->',
        '<div style="width:100%;background:#ffffff;padding:0;" align="center">',
        '<table style="width:100%;font-family:Arial,Helvetica,sans-serif;color:#333;line-height:1.58;background:#fff;" border="0" width="100%" cellspacing="0" cellpadding="0"><tbody>',
        f'<tr><td style="padding:38px 20px;border-bottom:4px solid #111;"><h1 style="margin:0;font-size:26px;color:#111;font-weight:800;text-transform:uppercase;">{html_escape(item.get("english_name"))}</h1><div style="margin-top:8px;font-size:14px;color:#333;">Product Type: {html_escape(item.get("product_type"))}</div><div class="model" style="margin-top:10px;font-size:15px;color:#333;font-weight:700;">Atomfair Model: {html_escape(item.get("atomfair_model"))}</div><div style="margin-top:15px;display:inline-block;background:#111;color:#fff;padding:6px 15px;font-size:13px;font-weight:bold;letter-spacing:.6px;text-transform:uppercase;">Research-grade laboratory instrument</div></td></tr><tr><td style="padding:38px 20px;">',
    ]
    parts.append(section("Product Overview", "".join(f'<p style="margin:0 0 14px 0;font-size:15px;color:#444;text-align:justify;">{html_escape(p)}</p>' for p in overview)))
    parts.append(section("Key Features and Advantages", '<ul style="margin:0;padding-left:22px;font-size:14px;color:#444;line-height:1.85;">' + "".join(f'<li style="margin-bottom:9px;">{html_escape(f)}</li>' for f in features) + "</ul>"))
    parts.append(section("Technical Specifications", table(["Parameter", "Specification / Available Values"], [[s.get("parameter", ""), s.get("value", "")] for s in specs])))
    if accessories:
        parts.append(section("Included and Compatible Accessories", table(["Accessory / Module", "Reference Code", "Specification", "Compatibility / Use"], [[a.get("name", ""), a.get("reference_code", ""), a.get("specification", ""), a.get("compatibility", "")] for a in accessories])))
    if ordering:
        parts.append(section("Atomfair Product Ordering and Configuration Table", table(["Unique Atomfair Order Model", "Source Model / Item", "Key Specification", "Primary Application"], [[o.get("order_model", ""), o.get("source_model", ""), o.get("key_specification", ""), o.get("application", "")] for o in ordering])))
    parts.append(f'<table style="background:#f7f7f7;border:1px solid #e0e0e0;margin-bottom:34px;" border="0" width="100%" cellspacing="0" cellpadding="22"><tbody><tr><td style="font-size:14px;color:#333;"><div style="margin-bottom:10px;"><strong>Data Handling Standard:</strong> All source-supported parameters, specifications, dimensions, capacities and compatible accessory information are preserved in structured tables.</div><div><strong>Ordering Standard:</strong> Different specifications, configurations and accessories must not be merged into one order line.</div></td></tr></tbody></table></td></tr><tr><td style="padding:25px 20px;background:#111;text-align:center;"><div style="color:#fff;font-size:20px;font-weight:bold;margin-bottom:8px;letter-spacing:1px;">TAILORED SOLUTIONS FOR RESEARCH</div><div style="color:#ddd;font-size:13px;margin-bottom:18px;">For bulk orders, OEM requirements, accessory matching, platform selection or configuration confirmation, contact our engineering sales team.</div><div style="display:inline-block;background:#fff;color:#111;padding:12px 35px;font-weight:800;font-size:13px;text-transform:uppercase;letter-spacing:1px;border-radius:2px;">EMAIL: inquiry@atomfair.com</div></td></tr><tr><td style="padding:28px 20px;text-align:center;font-size:12px;color:#888;letter-spacing:1px;"><div style="margin-bottom:5px;text-transform:uppercase;"><strong>Supplier:</strong> {html_escape(brand)}</div><div style="text-transform:uppercase;"><strong>Brand:</strong> {html_escape(brand.upper())}&reg;</div></td></tr></tbody></table></div>')
    return "".join(parts)


def validate_items(items: list[dict[str, Any]], model_prefix: str) -> None:
    seen_models: set[str] = set()
    required = ["chinese_name", "atomfair_model", "english_name", "category", "product_type", "overview_paragraphs", "features", "specifications"]
    for index, item in enumerate(items, 1):
        missing = [field for field in required if not item.get(field)]
        if missing:
            raise ValueError(f"Item {index} is missing required fields: {', '.join(missing)}")
        model = str(item.get("atomfair_model", "")).strip()
        if not model.startswith(f"{model_prefix}-"):
            raise ValueError(f"Item {index} model must start with {model_prefix}-: {model}")
        if model in seen_models:
            raise ValueError(f"Duplicate model generated: {model}")
        seen_models.add(model)

        english_text = "\n".join([
            str(item.get("english_name", "")),
            str(item.get("category", "")),
            str(item.get("product_type", "")),
            "\n".join(map(str, item.get("overview_paragraphs") or [])),
            "\n".join(map(str, item.get("features") or [])),
        ])
        if cjk_exists(english_text):
            raise ValueError(f"English fields contain Chinese characters for model {model}")
        forbidden = has_forbidden_phrase(english_text)
        if forbidden:
            raise ValueError(f"Forbidden workflow phrase found for model {model}: {forbidden}")


def make_records(items: list[dict[str, Any]], brand: str) -> list[dict[str, str]]:
    records = []
    for item in items:
        code = product_html(item, brand)
        if cjk_exists(code):
            raise ValueError(f"HTML contains Chinese characters for model {item.get('atomfair_model')}. Regenerate or edit the source output.")
        overview = " ".join(item.get("overview_paragraphs") or [])
        row = {header: "" for header in HEADERS}
        row.update({
            "来源": "",
            "商品中文名称": item.get("chinese_name", ""),
            "型号": item.get("atomfair_model", ""),
            "产品名称（英文）": item.get("english_name", ""),
            "简介": overview,
            "代码": code,
            "网站分类": item.get("category", ""),
        })
        if any(cjk_exists(str(row.get(header, ""))) for header in ["产品名称（英文）", "简介", "代码", "网站分类"]):
            raise ValueError(f"English upload fields contain Chinese characters for model {item.get('atomfair_model')}")
        forbidden = has_forbidden_phrase(row["简介"]) or has_forbidden_phrase(row["代码"])
        if forbidden:
            raise ValueError(f"Forbidden workflow phrase found in upload fields for model {item.get('atomfair_model')}: {forbidden}")
        records.append(row)
    return records


def write_excel(records: list[dict[str, str]], output_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"
    ws.append(HEADERS)
    for record in records:
        ws.append([record.get(header, "") for header in HEADERS])

    header_fill = PatternFill("solid", fgColor="111111")
    header_font = Font(color="FFFFFF", bold=True)
    thin = Side(style="thin", color="D9D9D9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    widths = [12, 24, 22, 36, 16, 60, 18, 80, 18, 14, 14, 18, 20, 18, 18, 12, 8, 12]
    for col_index, width in enumerate(widths, 1):
        ws.column_dimensions[ws.cell(1, col_index).column_letter].width = width
    for row in ws.iter_rows():
        for cell in row:
            cell.border = border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate full-English product HTML and Excel from product manuals.")
    parser.add_argument("--input", "-i", default="input", help="Manual file or folder. Supports .docx, .xlsx, .txt, .md and .csv.")
    parser.add_argument("--output", "-o", default="outputs/products.xlsx", help="Output XLSX path.")
    parser.add_argument("--records", default="outputs/products_records.json", help="Output JSON records path.")
    parser.add_argument("--brand", default=os.environ.get("BRAND_NAME", "Atomfair"), help="Brand name used in generated HTML.")
    parser.add_argument("--model-prefix", default=os.environ.get("MODEL_PREFIX", "AF"), help="Required model prefix.")
    parser.add_argument("--model", default=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"), help="OpenAI model name.")
    args = parser.parse_args()

    read_env_file(Path(".env"))
    input_path = Path(args.input)
    if input_path.is_dir():
        docx_files = sorted(p for p in input_path.iterdir() if p.suffix.lower() in SUPPORTED_EXTENSIONS and not p.name.startswith("~$"))
    else:
        docx_files = [input_path]
    if not docx_files:
        raise SystemExit("No .docx files found. Put manuals into input/ or pass --input path/to/manual.docx")

    all_items: list[dict[str, Any]] = []
    for docx_file in docx_files:
        source_text = extract_manual_text(docx_file)
        if not source_text.strip():
            raise SystemExit(f"No readable text or tables found in {docx_file}")
        prompt = build_prompt(source_text, args.brand, args.model_prefix)
        ai_text = call_openai(prompt, args.model)
        items = safe_json_from_text(ai_text)
        all_items.extend(items)

    validate_items(all_items, args.model_prefix)
    records = make_records(all_items, args.brand)
    records_path = Path(args.records)
    records_path.parent.mkdir(parents=True, exist_ok=True)
    records_path.write_text(json.dumps([{"sheetName": "Products", "records": records}], ensure_ascii=False, indent=2), encoding="utf-8")
    write_excel(records, Path(args.output))
    print(json.dumps({
        "input_files": [str(p) for p in docx_files],
        "items": len(records),
        "records": str(records_path),
        "excel": args.output,
        "source_column_blank": all(not r["来源"] for r in records),
        "html_cjk_issues": sum(1 for r in records if cjk_exists(r["代码"])),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
