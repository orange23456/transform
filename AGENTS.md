# Codex Instructions

This project converts laboratory product reports, manuals and source spreadsheets into upload-ready Excel files. Follow this workflow whenever a user supplies a new product report, catalog, manual, spreadsheet or product source file.

## Required Workflow

1. Read the source manual carefully before generating records.
2. Extract every product, product family, variant, specification, ordering row, module, accessory, consumable and spare part.
3. Generate full-English product HTML using the fixed Atomfair/Pipetting Series template style.
4. Export the upload Excel sheet with the fixed column order and the approved Pipetting Series-style formatting.
5. Validate the output against the source manual before reporting completion.

## Non-Negotiable Content Rules

- Keep the Excel `来源` column blank.
- Keep the Excel `是否上传` column blank.
- Keep the Excel `alt text`, `title` and `Caption` columns blank.
- HTML must contain no Chinese characters.
- Product names must follow the source manual. Do not invent product names.
- HTML page titles must not be prefixed with `ATOMFAIR®`; show the product name only.
- Excel `产品名称（英文）` must not be prefixed with `ATOMFAIR®`.
- Put `Atomfair Model` inside the `Technical Specifications` table, not as a separate line below the HTML title.
- The `Atomfair Model` row must use the same table-cell font style as other specification rows; do not make it bold, larger or visually separated.
- Use the micro symbol `µL` in customer-facing product names, summaries and HTML; do not use `uL` or `UL` except inside fixed order/model codes.
- Use `°C` and `±` in customer-facing temperature and tolerance values; do not use bare `C`, `deg C` or `+/-` in summaries or HTML.
- Preserve source product casing such as `HiPette-LTS`; do not force HTML product titles to all caps.
- Use professional sterilization wording such as `Fully autoclavable` or source-supported cycle details. Do not write vague phrasing such as `Full high-temperature sterilization supported`.
- Use `Product Family`, not `Source Product Family`, in customer-facing technical or ordering tables.
- When accuracy, precision, systematic error or random error values correspond to multiple test volumes, pair every value with its exact test volume. Do not rely on list order alone.
- If a page represents one single specification row, omit the `Atomfair Product Ordering and Configuration Table` because it duplicates `Technical Specifications`. Keep ordering/comparison tables only when the page truly compares multiple configurations.
- Avoid repeating the same application scenario, selection guidance or parameter list across `Product Overview`, `Key Features and Advantages`, and note blocks.
- Backend categories, tags and HTML source must describe only the product shown on that page. Do not include unrelated category or product terms, such as battery materials, centrifugation, distillation/evaporation, electrophoresis, spectrophotometry, electrochemistry, heating/stirring, mixing/shaking or other cross-category wording, unless the current source product is actually that product.
- If the source product name or description contains the original manufacturer name, replace that manufacturer name with Atomfair or ATOMFAIR as appropriate.
- Do not invent product families, model meanings, volume ranges, temperature ranges, capacity ranges, dimensions, specifications, applications or compatibility.
- Do not manually generalize volume ranges, temperature ranges, capacities, speed ranges, accuracy tables or precision tables.
- Do not reuse a range/specification table from one product series for another product series.
- Each product family may use only its own source heading, source description and source parameter table.
- If a product has multiple specifications, capacities, ranges, channel counts, rotors, blocks, modules or configurations, each specification must become its own row with a unique Atomfair model.
- 8-channel, 12-channel, 16-channel and all other multichannel pipette variants must be preserved and split.
- Accessories and spare parts must not be omitted. Separately orderable accessories must become rows.
- Product Overview must be detailed, professional and source-supported. It may mention application scenarios only when they fit the product and source evidence.
- Product Overview must not include internal workflow language such as `listed separately`, `separate upload row`, `unified order model`, `source product name`, `this row is separated`, `independent ordering product`, `saved as a separate row` or similar phrases.
- Do not write phrases implying that accessories or data are saved as separate upload rows. The product page already represents the complete data for that row.

## Fixed HTML Template Rules

- Match the existing Atomfair/Pipetting Series HTML style.
- Use full-English HTML only.
- Use inline styles, Arial/Helvetica font, black section accents, black table headers, left-aligned cells and full-width tables.
- Keep the `h1` style at `font-size:26px` and the main wrapper/table structure consistent.
- Keep section names consistent: `Product Overview`, `Key Features and Advantages`, `Technical Specifications`, accessory/configuration sections and ordering/configuration table sections.
- Do not switch to another HTML template, CSS class system or visible Chinese text.
- Keep the same bottom contact block and include `inquiry@atomfair.com`.
- Generated HTML must be visually consistent across batches: same structure, font behavior, table style, capitalization, alignment and footer.

## Fixed Excel Output Rules

Use the fixed upload columns, in this exact order:

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

Excel formatting must match the approved Pipetting Series style:

- Use the same column widths, row heights, wrap settings, borders, fills and table object behavior as the Pipetting Series reference when a reference workbook is provided.
- If no reference workbook is provided, use the built-in light-blue banded upload-table style.
- Do not randomly switch to a dark header, plain white table or another color system.
- When the user points to a reference workbook, copy styles from the `Pipetting Series` sheet.

## Running The Generic Pipeline

```powershell
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

For one file:

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

To copy Excel style from a known-good workbook:

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx --style-reference "C:\path\to\大龙产品可上架版last.xlsx" --style-sheet "Pipetting Series"
```

The generic runner supports `.docx`, `.xlsx`, `.txt`, `.md` and `.csv`. If the manual is image-only or extraction misses visual tables, use Codex visual/OCR review and manual verification rather than guessing.

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
- Excel formatting matches the approved Pipetting Series-style upload workbook.
