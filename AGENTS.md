# Codex Instructions

This project converts laboratory product reports and manuals into upload-ready Excel files. Follow these instructions whenever the user supplies a new product report, catalog, manual, spreadsheet or product source file.

## Required Workflow

1. Read the source manual carefully before generating records.
2. Extract every product, product family, variant, specification, ordering row, module, accessory, consumable and spare part.
3. Generate full-English product HTML using the fixed Atomfair/Pipetting Series template style.
4. Export the upload Excel sheet with the fixed column order.
5. Validate the output against the source manual before reporting completion.

## Non-Negotiable Content Rules

- Keep the Excel `来源` column blank.
- Keep the Excel `是否上传` column blank.
- Keep the Excel `alt text`, `title` and `Caption` columns blank.
- HTML must contain no Chinese characters.
- Product names must follow the source manual. Do not invent product names.
- If the source product name or description contains the original manufacturer name, replace that manufacturer name with Atomfair or ATOMFAIR as appropriate.
- Do not invent product families, model meanings, volume ranges, temperature ranges, capacity ranges, dimensions, specifications, applications or compatibility.
- Do not manually generalize volume ranges, temperature ranges, capacities, speed ranges, accuracy tables or precision tables.
- Do not reuse a range/specification table from one product series for another product series.
- Each product family may use only its own source heading, source description and source parameter table.
- If a product has multiple specifications, capacities, ranges, channel counts, rotors, blocks, modules or configurations, each specification must become its own row with a unique Atomfair model.
- 8-channel, 12-channel, 16-channel and all other multichannel pipette variants must be preserved and split.
- Accessories and spare parts must not be omitted. Separately orderable accessories must become rows.
- Product Overview must be detailed, professional and source-supported. It may mention application scenarios only when they fit the product and source evidence.
- Product Overview must not include internal workflow language such as `listed separately`, `unified order model`, `source product name`, `this row is separated`, `independent ordering product` or similar phrases.

## Fixed HTML Style Rules

- Match the existing Atomfair/Pipetting Series HTML style.
- Use full-English HTML only.
- Use inline styles, Arial/Helvetica font, black section accents, black table headers, left-aligned cells and full-width tables.
- Keep section names consistent: `Product Overview`, `Key Features and Advantages`, `Technical Specifications`, accessory/configuration sections and ordering/configuration table sections.
- Do not switch to another HTML template, CSS class system or visible Chinese text.
- Keep the same bottom contact block and include `inquiry@atomfair.com`.
- Generated HTML must be visually consistent across batches: same structure, font behavior, table style, capitalization, alignment and footer.

## Excel Output Rules

Use the fixed upload columns:

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

The `代码` column contains the complete product HTML. The `简介` column contains professional English summary copy. Leave image and upload-control columns blank unless the user explicitly provides image assets and asks for image processing.

## Running The Generic Pipeline

```powershell
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

For one file:

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

The generic runner supports `.docx`, `.xlsx`, `.txt`, `.md` and `.csv`. If the manual is image-only or the extraction misses visual tables, use Codex visual/OCR review and manual verification rather than guessing.

## Verification Checklist

Before final delivery, check:

- No Chinese characters appear in HTML.
- `来源`, `是否上传`, `alt text`, `title` and `Caption` are blank for every row.
- Models are unique.
- Product rows are split by specification, capacity, range, channel count, configuration and accessory.
- Every source table row has a corresponding generated row when it represents a distinct orderable item.
- All product parameters, specifications, dimensions, ranges and accessories from the source are represented.
- Product Overview is professional product copy, not process commentary.
- HTML formatting matches the fixed Atomfair/Pipetting Series style, including black table headers, left alignment, consistent font and the bottom `inquiry@atomfair.com` contact block.
