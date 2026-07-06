# Codex Instructions

This project generates upload-ready Excel files from laboratory product manuals. Follow this workflow whenever the user supplies a new product report or manual.

## Workflow

1. Read the source manual carefully before generating records.
2. Extract all products, variants, specifications, ordering rows and accessories.
3. Generate full-English product HTML using the Atomfair template.
4. Export the Excel upload sheet.
5. Validate the output against the source manual before reporting completion.

## Non-Negotiable Rules

- Keep the Excel `来源` column blank.
- HTML must contain no Chinese characters.
- Product names follow the source manual. Replace original manufacturer names with Atomfair only when they appear in product names or descriptions.
- Do not invent product names, product families, ranges, dimensions, specifications, applications or model meanings.
- Do not manually generalize volume ranges, temperature ranges, capacities, speed ranges or accuracy tables.
- Do not reuse a range/specification table from one product series for another product series.
- If a product has multiple specifications, each specification must be its own row with a unique Atomfair model.
- 8-channel, 12-channel, 16-channel and other multichannel pipette variants must be preserved and split.
- Accessories and spare parts must not be omitted. Separately orderable accessories should become rows.
- Product Overview should be detailed, professional and source-supported. It may mention application scenarios only when they fit the product and source evidence.
- Product Overview must not include internal workflow language such as "listed separately", "unified order model", "source product name" or "this row is separated".
- Keep the existing HTML template style and bottom contact block, including `inquiry@atomfair.com`.

## Running The Generic Pipeline

```powershell
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

For one file:

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

The generic runner supports `.docx`, `.xlsx`, `.txt`, `.md` and `.csv`.

## Verification

After generation, check:

- No Chinese characters appear in HTML.
- `来源` is empty for every row.
- Models are unique.
- Product rows are split by specification and accessory.
- Every source table row has a corresponding generated row when it represents a distinct orderable item.
- Overview text is professional product copy, not process commentary.
