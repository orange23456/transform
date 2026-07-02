一键流程

双击“一键生成.bat”（或运行“一键生成.ps1”），流程会自动完成三步：

1. 运行 C:\Users\hz-user\Documents\HTML生成 里的 HTML 生成前置脚本
2. 从刚生成的 HTML/Word 代码文件抽取产品记录
3. 立即生成 Excel，并同步一份到桌面

当前已接入的前置脚本：
- gen_heating_stirring.py -> 加热搅拌全部产品
- gen_distillation.py -> 蒸馏系列全部产品

为避免原输出文件被 Word 占用导致失败，前置脚本会被调度到这里输出：
- C:\Users\hz-user\Desktop\全自动\generated_html

温控系列当前没有独立前置脚本，仍从 C:\Users\hz-user\Desktop\大龙\温控系列全部产品 读取已有代码文件。

生成结果：
- C:\Users\hz-user\Desktop\全自动\outputs\dalong_all_series\大龙全系列产品.xlsx
- C:\Users\hz-user\Desktop\大龙全系列产品.xlsx
