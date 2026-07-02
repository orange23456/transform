# Product Manual to HTML and Excel Generator

This project converts product manuals into full-English product HTML and an Excel upload sheet.

## What It Does

- Reads `.docx` product manuals from the `input/` folder.
- Uses an OpenAI model to identify products, specifications, models, accessories and ordering rows.
- Generates full-English HTML for each product.
- Exports an Excel file with the required upload columns.
- Keeps the `来源` column blank.
- Gives every product specification and accessory a separate unique model.

## Quick Start

1. Download this repository from GitHub.
2. Install Python 3.10 or newer.
3. Copy `.env.example` to `.env`.
4. Fill in your OpenAI API key:

```text
OPENAI_API_KEY=sk-your-key-here
```

5. Put product manuals into the `input/` folder.
6. Double-click `run.bat`, or run:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -r requirements.txt
python main.py --input input --output outputs\products.xlsx
```

The generated Excel file will be saved to:

```text
outputs/products.xlsx
```

## Manual Command

```powershell
python main.py --input input --output outputs\products.xlsx
```

You can also process one file:

```powershell
python main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

## Standard Rules

- HTML must be English only.
- Product names follow the source manual.
- Original manufacturer or brand names are replaced with Atomfair.
- Each different specification, configuration, channel count, capacity and accessory must become a separate row.
- Product Overview can be expanded, but it must stay source-supported and rigorous.
- All parameters, specifications, dimensions, accessories and compatibility information should be preserved.
- The Excel `来源` column stays blank.

## Important Limitation

This generic version needs an OpenAI API key. Without AI, a program cannot reliably understand arbitrary new manuals, translate Chinese content into English, identify product/accessory boundaries and generate complete ecommerce HTML.

The older series-specific scripts are still included in this repository for previously generated product families.

## Main Files

- `main.py`: generic entry point for new manuals.
- `requirements.txt`: Python dependencies.
- `run.bat`: Windows one-click runner.
- `run.ps1`: PowerShell runner.
- `build_excel_from_html.mjs`: older Codex-specific Excel builder.
- `build_*_full.py`: historical series-specific generators.

## Download

```powershell
git clone https://github.com/orange23456/-Excel.git
```

Or use GitHub:

```text
Code -> Download ZIP
```

