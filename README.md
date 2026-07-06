# Product Manual to HTML and Excel Generator

This repository turns laboratory product manuals into upload-ready Excel sheets. The workflow is:

1. Read the supplied product report or manual.
2. Extract every product, specification, ordering model and accessory.
3. Generate full-English ecommerce HTML for each row.
4. Export an Excel file with the required upload columns.

The current generic runner supports `.docx`, `.xlsx`, `.txt`, `.md` and `.csv` input files.

## Required Standard

- The Excel `来源` column must stay blank.
- HTML must be English only. Chinese text is allowed only in `商品中文名称`.
- Product names must follow the source manual. If the source name contains another manufacturer's brand, replace that brand with `Atomfair`.
- Do not invent product names, ranges, parameters, dimensions or applications.
- Do not borrow range tables or specification tables from another product family.
- Each product family must use only its own source tables and source description.
- Different specifications must be split into separate rows, including capacity, volume range, channel count, temperature range, rotor, block, module and configuration differences.
- 8-channel, 12-channel, 16-channel and other multichannel variants must not be missed or merged.
- Every separately orderable accessory, adapter, module, electrode, rotor, rack, block, cable or spare part must be included.
- Product Overview should be detailed and professional, with supported application scenarios when appropriate.
- Product Overview must not contain internal workflow language such as "listed separately", "unified order model" or "keeps the source product name".
- The bottom contact section of the HTML uses the Atomfair template and `inquiry@atomfair.com`.

## Quick Start

1. Download or clone this repository.
2. Install Python 3.10 or newer.
3. Copy `.env.example` to `.env`.
4. Fill in your OpenAI API key:

```text
OPENAI_API_KEY=sk-your-key-here
```

5. Put product manuals into the `input/` folder.
6. Run `run.bat`, `run.ps1`, or the command below:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

The generated files will be saved to:

```text
outputs/products.xlsx
outputs/products_records.json
```

## Process One File

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

## Configuration

Use `.env` or command-line options:

```text
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4.1-mini
BRAND_NAME=Atomfair
MODEL_PREFIX=AF
```

Command-line example:

```powershell
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx --brand Atomfair --model-prefix AF --model gpt-4.1-mini
```

## Built-In Validation

The runner stops with an error if it detects:

- Chinese characters in generated HTML or English upload fields.
- Duplicate generated models.
- Missing required product fields.
- Generated models that do not start with the configured prefix.
- Internal workflow phrases in Product Overview or HTML.

This validation does not replace manual review. Before upload, open the Excel and compare the generated rows against the source manual, especially range tables, specification tables and accessory lists.

## Repository Files

- `main.py`: generic product-manual-to-Excel runner.
- `AGENTS.md`: Codex operating instructions for this workflow.
- `requirements.txt`: Python dependencies.
- `run.bat`: Windows one-click runner.
- `run.ps1`: PowerShell runner.
- `input/`: place manuals here.
- `outputs/`: generated Excel and JSON files.
- `build_*`, `verify_*`, `*_records.json`: historical series-specific scripts and records from earlier product batches.

## Clone

```powershell
git clone https://github.com/orange23456/transform.git
```
