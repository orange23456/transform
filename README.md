# Product Manual to Upload-Ready Excel

This repository converts laboratory product manuals, catalogs, reports and source spreadsheets into upload-ready Excel files with Atomfair product HTML.

## What The Workflow Does

1. Read the source manual carefully.
2. Extract every product, product family, variant, specification, ordering row, module, accessory, consumable and spare part.
3. Split different specifications, capacities, ranges, channel counts, rotors, blocks, modules and configurations into separate product rows.
4. Generate full-English product HTML using the fixed Atomfair/Pipetting Series template style.
5. Export the upload Excel sheet in the fixed column order and approved blue-banded format.
6. Validate the output before delivery.

## Required Output Rules

- `来源` stays blank.
- `是否上传` stays blank.
- `alt text`, `title` and `Caption` stay blank.
- HTML must contain no Chinese characters.
- Product names must follow the source manual. Do not invent product names.
- Original manufacturer names are replaced with Atomfair or ATOMFAIR when they appear.
- HTML page titles must not be prefixed with `ATOMFAIR®`; show the product name only.
- Excel `产品名称（英文）` must not be prefixed with `ATOMFAIR®`.
- `Atomfair Model` must appear inside the `Technical Specifications` table.
- The `Atomfair Model` row must use the same table-cell font style as other specification rows.
- Backend categories, tags and HTML source must only describe the product shown on that page. Do not include unrelated product-family terms.
- Accessories, spare parts, modules, electrodes, adapters, cables and consumables are products too and must not be omitted.
- Product Overview must be detailed, professional and source-supported.
- Product Overview and HTML must not include internal workflow language such as `listed separately`, `separate upload row`, `source product name`, `unified order model` or similar phrases.

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

You can also run:

```powershell
.\run.ps1
```

or double-click:

```text
run.bat
```

Supported input types: `.docx`, `.xlsx`, `.txt`, `.md` and `.csv`.

## Match The Pipetting Series Excel Format

If you have a known-good workbook, pass it as a style reference:

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

Open this repository in Codex and provide a product manual. Ask:

```text
Follow AGENTS.md and generate the final upload-ready Excel. Use the fixed Atomfair/Pipetting Series HTML template and Excel format.
```

Codex should read the manual, extract all products and accessories, split product rows by specification, generate full-English HTML, export Excel in the fixed column order, and verify the result against the source manual.

For image-only manuals or screenshots where text extraction misses tables, use visual/OCR review and manual verification instead of guessing.

## Output Files

By default:

```text
outputs/products.xlsx
outputs/products_records.json
```

`products_records.json` contains generated row data for audit and reruns.

## Verification

The generator checks:

- HTML has no Chinese characters.
- English fields have no Chinese characters.
- Model numbers are unique.
- Required blank columns are blank.
- Forbidden internal workflow phrases do not appear in Product Overview or HTML.
- Forbidden unrelated product-category pollution terms do not appear in generated backend or HTML text.

Manual review is still required before upload. Always compare the output against the source manual to confirm every specification, range, dimension, accessory and ordering row is covered.
