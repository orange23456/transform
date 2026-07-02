# Product HTML to Excel Generator

这个项目用于把产品资料整理成商品 HTML，并进一步输出 Excel 上传表。

## 当前标准流程

1. 根据产品资料生成完整英文 HTML。
2. HTML 中保留产品参数、规格、尺寸、配置、配件等信息。
3. 不同规格、不同配置、不同配件单独生成唯一型号。
4. 再把同一套内容同步输出到 Excel。
5. Excel 的 `来源` 列保持空白。

## 重要规则

- HTML 必须全英文。
- 产品名以资料/手册为准，不自行乱取名。
- 如果资料里的产品名包含原厂商信息，替换为 Atomfair。
- 型号按照 Atomfair 统一规则生成。
- Product Overview 可以适当扩写，但必须严谨，不能虚构功能或参数。
- 配件也必须作为独立商品行输出。

## 主要文件

- `build_excel_from_html.mjs`：把记录 JSON 输出为 Excel。
- `build_temp_distill_full.py`：温控系列、蒸馏系列生成脚本。
- `build_product_collection_full.py`：产品集生成脚本。
- `build_pipetting_full.py`：移液系列生成脚本。
- `build_centrifuge_full.py`：离心系列生成脚本。
- `build_new_series_full.py`：混匀、摇床、电泳等系列生成脚本。
- `build_spectro_echem_full.py`：分光光度计、电化学系列生成脚本。

## 使用方式

在 Codex 或已配置好依赖的本机环境中运行对应脚本，例如：

```powershell
python build_temp_distill_full.py
node build_excel_from_html.mjs temperature_control_series_full_records.json outputs\temperature_control_series_full
node build_excel_from_html.mjs distillation_series_full_records.json outputs\distillation_series_full
```

也可以运行：

```powershell
.\一键生成.ps1
```

## 下载使用

别人可以在 GitHub 页面点击：

```text
Code -> Download ZIP
```

或者使用：

```powershell
git clone https://github.com/orange23456/-Excel.git
```

## 注意

本项目没有上传 `outputs`、`generated_html_full`、图片抽取缓存和 `node_modules`，这些属于运行中间产物或本机依赖。

