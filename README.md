# Atomfair Product Manual Transformer

This repository converts laboratory product manuals, catalogs, source spreadsheets and product reports into upload-ready Excel files with full-English Atomfair product HTML.

It is designed for Codex-assisted production work: give Codex a product manual, follow `AGENTS.md`, and generate an Excel file that can be reviewed and uploaded.

## What The Workflow Does

1. Reads source manuals or product files.
2. Extracts every product, family, variant, specification, configuration, module, accessory, consumable and spare part.
3. Splits distinct specifications into separate upload rows with unique Atomfair models.
4. Generates full-English product HTML in the fixed Atomfair/Pipetting Series style.
5. Exports the fixed upload Excel columns.
6. Validates generated records before delivery.

## Fixed Upload Columns

```text
来源
商品中文名称
型号
产品名称（英文）
URL
简介
产品详情
代码
网站分类
主图
详情图
图片文件名
alt text
title
Caption
价格
💲
是否上传
```

The following columns must stay blank unless the user explicitly asks otherwise:

```text
来源
是否上传
alt text
title
Caption
```

## Non-Negotiable Output Rules

- HTML must contain no Chinese characters.
- Product names must follow the source manual. Do not invent product names.
- If a source product name or description contains the original manufacturer name, replace it with Atomfair or ATOMFAIR as appropriate.
- HTML page titles must not be prefixed with `ATOMFAIR®`; show the product name only.
- Excel `产品名称（英文）` must not be prefixed with `ATOMFAIR®`.
- `Atomfair Model` must appear inside the `Technical Specifications` table, not below the title.
- The `Atomfair Model` row must use the same table-cell font style as other specification rows.
- Use `µL` in customer-facing product names, summaries and HTML. Do not use `uL` or `UL` except inside fixed order/model codes.
- Use `°C` and `±` in customer-facing temperature and tolerance values. Do not use bare `C`, `deg C` or `+/-` in summaries or HTML.
- Preserve source product casing such as `HiPette-LTS`; do not force HTML product titles to all caps.
- Use professional sterilization wording such as `Fully autoclavable` or source-supported cycle details.
- Use `Product Family`, not `Source Product Family`, in customer-facing tables.
- When accuracy, precision, systematic error or random error values correspond to multiple test volumes, pair every value with its exact test volume. Do not rely on list order alone.
- If a page represents one single specification row, omit the `Atomfair Product Ordering and Configuration Table`.
- Keep ordering/comparison tables only when a page truly compares multiple configurations.
- Avoid repeating the same application scenario, selection guidance or parameter list across `Product Overview`, `Key Features and Advantages`, and note blocks.
- Backend category, tags and HTML source must describe only the product shown on that page. Do not include unrelated product-category terms.
- Accessories and spare parts must not be omitted.

## Install

```powershell
git clone https://github.com/orange23456/transform.git
cd transform
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`, then fill in your OpenAI key:

```text
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4.1-mini
BRAND_NAME=Atomfair
MODEL_PREFIX=AF
```

## Run

Put manuals into `input/`, then run:

```powershell
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

For one file:

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

Or use:

```powershell
.\run.ps1
```

Supported input types:

```text
.docx
.xlsx
.txt
.md
.csv
```

## Optional Style Reference

If you have a known-good upload workbook, pass it as a style reference:

```powershell
.\.venv\Scripts\python.exe main.py `
  --input "C:\path\to\manual.docx" `
  --output outputs\manual_products.xlsx `
  --style-reference "C:\path\to\approved_upload_style.xlsx" `
  --style-sheet "Pipetting Series"
```

When `--style-reference` is provided, the output copies the column widths, row heights, fills, borders, wrapping and table behavior from the reference sheet.

Without a reference workbook, the generator uses the built-in light-blue banded upload-table format.

## Use With Codex

Open this repository in Codex and provide a product manual. Ask Codex:

```text
Follow AGENTS.md and generate the final upload-ready Excel.
Use the fixed Atomfair/Pipetting Series HTML template and Excel format.
Do not omit any product, variant, specification, accessory or spare part.
```

For image-only manuals or screenshots where text extraction misses visual tables, use visual/OCR review and manual verification instead of guessing.

## Output Files

By default:

```text
outputs/products.xlsx
outputs/products_records.json
```

`products_records.json` contains generated row data for audit and reruns.

## Verification

Before delivery, verify:

- HTML has no Chinese characters.
- Models are unique.
- Required blank columns are blank.
- Product rows are split by specification, capacity, range, channel count, configuration and accessory.
- All source parameters, specifications, dimensions, ranges and accessories are represented.
- Product Overview is professional product copy, not process commentary.
- No unrelated product-category terms appear in backend categories, tags or HTML source.
- Microliter units use `µL`, not `uL`.
- Error/accuracy/precision values are paired with their exact test volumes.
- Single-specification pages do not repeat the same data in an ordering table.
- HTML formatting matches the fixed Atomfair/Pipetting Series style and includes `inquiry@atomfair.com`.

Manual review is still required before upload. Always compare the output against the source manual.
