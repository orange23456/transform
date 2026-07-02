import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const recordsPath = process.argv[2] || path.join(__dirname, "html_records.json");
const outputDir = process.argv[3] || path.join(__dirname, "outputs", "dalong_all_series");
const outputPath = path.join(outputDir, "大龙全系列产品.xlsx");
const desktopPath = "C:/Users/hz-user/Desktop/大龙全系列产品.xlsx";
const desktopFallbackPath = `C:/Users/hz-user/Desktop/大龙全系列产品_${new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19)}.xlsx`;
const headers = ["来源", "商品中文名称", "型号", "产品名称（英文）", "URL", "简介", "产品详情", "代码", "网站分类", "主图", "详情图", "图片文件名", "alt text", "title", "Caption", "价格", "💲", "是否上传"];
const widths = [90, 190, 140, 280, 120, 460, 140, 560, 130, 100, 100, 140, 160, 140, 140, 90, 70, 100];

const payload = JSON.parse(await fs.readFile(recordsPath, "utf8"));
const workbook = Workbook.create();

function tableName(sheetName, index) {
  const base = sheetName.replace(/[^A-Za-z0-9_]/g, "").slice(0, 18) || `Products${index + 1}`;
  return `${base}Table`;
}

for (const [index, group] of payload.entries()) {
  const sheetName = group.sheetName.slice(0, 31);
  const sheet = workbook.worksheets.add(sheetName);
  sheet.showGridLines = false;

  const records = group.records || [];
  const rows = [headers, ...records.map((record) => headers.map((header) => record[header] ?? ""))];
  const used = sheet.getRangeByIndexes(0, 0, rows.length, headers.length);
  used.values = rows;
  used.format.wrapText = true;
  used.format.borders = { preset: "all", style: "thin", color: "#D9D9D9" };

  sheet.getRange("A1:R1").format = {
    fill: "#111111",
    font: { bold: true, color: "#FFFFFF" },
    horizontalAlignment: "center",
    verticalAlignment: "center",
  };
  sheet.getRange("A1:R1").format.rowHeightPx = 30;

  if (records.length > 0) {
    sheet.getRangeByIndexes(1, 0, records.length, headers.length).format.verticalAlignment = "top";
    sheet.getRangeByIndexes(1, 0, records.length, headers.length).format.rowHeightPx = 96;
  }

  widths.forEach((width, columnIndex) => {
    sheet.getRangeByIndexes(0, columnIndex, rows.length, 1).format.columnWidthPx = width;
  });
  sheet.freezePanes.freezeRows(1);
  sheet.tables.add(`A1:R${rows.length}`, true, tableName(group.sheetName, index));
}

await fs.mkdir(outputDir, { recursive: true });

for (const group of payload) {
  const sheetName = group.sheetName.slice(0, 31);
  const rowsToRender = Math.min((group.records?.length || 0) + 1, 8);
  const preview = await workbook.render({ sheetName, range: `A1:H${rowsToRender}`, scale: 1, format: "png" });
  await fs.writeFile(path.join(outputDir, `preview_${sheetName}.png`), new Uint8Array(await preview.arrayBuffer()));
}

for (const group of payload) {
  const sheetName = group.sheetName.slice(0, 31);
  const rowsToCheck = Math.min((group.records?.length || 0) + 1, 4);
  const check = await workbook.inspect({
    kind: "table",
    range: `${sheetName}!A1:R${rowsToCheck}`,
    include: "values",
    tableMaxRows: 4,
    tableMaxCols: 18,
    tableMaxCellChars: 70,
    maxChars: 5000,
  });
  console.log(check.ndjson);
}

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  maxChars: 2000,
});
console.log(errors.ndjson);

const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);

let copiedDesktopPath = desktopPath;
try {
  await fs.copyFile(outputPath, desktopPath);
} catch (error) {
  if (error && error.code === "EBUSY") {
    copiedDesktopPath = desktopFallbackPath;
    await fs.copyFile(outputPath, copiedDesktopPath);
  } else {
    throw error;
  }
}

console.log(JSON.stringify({
  outputPath,
  desktopPath: copiedDesktopPath,
  sheets: payload.map((group) => ({ name: group.sheetName, rows: group.records?.length || 0 })),
}, null, 2));
process.exit(0);
