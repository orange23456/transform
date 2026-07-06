# Product Manual to Upload Excel

这个仓库用于把实验室产品报告、产品手册或产品资料转换成可上传的 Excel。流程会先抽取产品、规格、型号、参数和配件，再生成全英文 Atomfair HTML，最后导出固定格式的 Excel。

## 标准流程

1. 把产品报告或手册放进 `input/`。
2. 运行生成器。
3. 检查 `outputs/products.xlsx` 和 `outputs/products_records.json`。
4. 对照原始手册复核产品、规格、参数、配件和型号拆分。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py --input input --output outputs\products.xlsx
```

也可以直接运行：

```powershell
.\run.ps1
```

或双击：

```text
run.bat
```

## 单个文件

```powershell
.\.venv\Scripts\python.exe main.py --input "C:\path\to\manual.docx" --output outputs\manual_products.xlsx
```

支持 `.docx`、`.xlsx`、`.txt`、`.md`、`.csv`。

## 环境变量

复制 `.env.example` 为 `.env`，填入 API key：

```text
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4.1-mini
BRAND_NAME=Atomfair
MODEL_PREFIX=AF
```

## 必须保持一致的输出效果

- Excel 列顺序固定，不能改列名、不能少列。
- `来源`、`是否上传`、`alt text`、`title`、`Caption` 必须全部为空。
- HTML 必须是全英文，不能出现中文字符。
- HTML 模板固定为 Atomfair/Pipetting Series 风格：Arial 字体、黑色表头、左对齐、全宽表格、同样的 section 标题格式和底部联系信息。
- 底部必须保留 `inquiry@atomfair.com`。
- 不同批次生成出来的 HTML 结构、字体、大小写、表格效果和 Excel 效果必须一致。

## 内容规则

- 产品名按手册原文来，不自己编名；原厂商品牌只替换成 Atomfair。
- 同一个产品只要规格、容量、量程、通道数、模块、转子、配置不同，就拆成独立行，并给唯一 Atomfair 型号。
- 8 道、12 道、16 道等多通道移液器必须保留并拆分。
- 配件、耗材、模块、电极、转子、适配器、支架、线缆、备件都不能漏。
- 不允许人工概括量程、温度范围、容量、速度范围、精度表。
- 不允许把一个系列的参数表套到另一个系列。
- Product Overview 要专业、详细、严谨，可以写应用场景，但必须符合产品类型和原始资料。
- Product Overview 不能出现内部流程话术，例如 `listed separately`、`unified order model`、`source product name`、`this row is separated`。

## Codex 使用方式

如果你在 Codex 中使用这个仓库，直接把新的产品手册给 Codex，并要求：

```text
按 AGENTS.md 的标准流程生成最终可上传 Excel。
```

Codex 应先读原始手册，完整提取产品和规格，再生成 HTML 与 Excel，并在交付前做一致性检查。

## 内置检查

`main.py` 会检查：

- HTML 是否含中文。
- 关键英文字段是否含中文。
- 模型是否重复。
- 必须为空的列是否为空。
- Product Overview 和 HTML 是否含内部流程话术。

自动检查不能替代人工复核。上传前仍然要对照源手册确认每一条规格、参数、尺寸和配件都已覆盖。
