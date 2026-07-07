# Product Manual to Upload-Ready Excel

This repository turns laboratory product manuals, reports, catalogs and source spreadsheets into upload-ready Excel files.

It follows the same workflow used in the Codex conversation:

1. Read the source product manual.
2. Extract every product, specification, variant, module, accessory and spare part.
3. Generate full-English Atomfair product HTML.
4. Export an upload-ready Excel sheet.
5. Validate blank columns, English-only HTML, unique models and complete product splitting.

## What This Project Enforces

- `来源` stays blank.
- `是否上传` stays blank.
- `alt text`, `title` and `Caption` stay blank.
- HTML contains no Chinese characters.
- Product names follow the source manual.
- Original manufacturer names are replaced with Atomfair when they appear.
- Different specifications become different rows with unique Atomfair models.
- Accessories, electrodes, rotors, adapters, cables, modules, spare parts and consumables are not omitted.
- 8-channel, 12-channel, 16-channel and other multichannel variants are preserved.
- Product Overview is professional product copy, not internal workflow commentary.
- HTML must not include phrases such as `listed separately`, `separate upload row`, `source product name`, `unified order model` or similar.
- HTML uses the fixed Atomfair/Pipetting Series-style template.
- Excel uses the approved Pipetting Series-style upload format.

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

You can also use:

```powershell
.\run.ps1
```

or double-click:

```text
run.bat
```

Supported input types: `.docx`, `.xlsx`, `.txt`, `.md`, `.csv`.

## Match The Pipetting Series Excel Format

If you have a known-good workbook, pass it as a style reference:

```powershell
.\.venv\Scripts\python.exe main.py `
  --input "C:\path\to\manual.docx" `
  --output outputs\manual_products.xlsx `
  --style-reference "C:\path\to\大龙产品可上架版last.xlsx" `
  --style-sheet "Pipetting Series"
```

When `--style-reference` is provided, the output copies the column widths, row heights, fills, borders, wrapping and table behavior from the `Pipetting Series` sheet.

Without a reference workbook, the generator uses the built-in light-blue banded upload-table format.

## Use With Codex

Open this repository in Codex and provide a product manual. Ask:

```text
按 AGENTS.md 的标准流程生成最终可上传 Excel。HTML 模板和 Excel 格式都要按 Pipetting Series 标准。
```

Codex should:

- Read the manual carefully.
- Extract products, variants, specs and accessories.
- Split different specifications into separate rows.
- Generate full-English HTML.
- Export Excel in the fixed column order.
- Verify the result before delivery.

For image-only manuals or PDFs/screenshots where text extraction misses tables, Codex should visually inspect/OCR the pages and manually verify the product rows instead of guessing.

## Output Files

By default:

```text
outputs/products.xlsx
outputs/products_records.json
```

`products_records.json` contains the generated row data for audit and reruns.

## Verification

The generator checks:

- HTML has no Chinese characters.
- English fields have no Chinese characters.
- Model numbers are unique.
- Blank upload columns are blank.
- Forbidden internal workflow phrases do not appear in Product Overview or HTML.

Manual review is still required before upload. Always compare the output against the source manual to confirm every specification, range, dimension, accessory and ordering row is covered.
