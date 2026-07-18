# pdf-watermark 實作細節

[English](implementation.en.md) | 繁體中文

## 專案結構

| 路徑 | 用途 |
|---|---|
| `src/pdf_watermark/__init__.py` | 浮水印產生與 PDF 合併的核心邏輯 |
| `src/pdf_watermark/cli.py` | 命令列參數解析與多檔案處理 |
| `src/pdf_watermark/__main__.py` | 支援 `python -m pdf_watermark` |
| `create_test_pdf.py` | 產生含多種頁面尺寸的人工測試檔 |

## 處理流程

1. `cli.main()` 使用 `argparse` 解析輸入檔案與 `--text`。
2. 每個輸入路徑會依序傳給 `add_watermark()`。
3. `pypdf.PdfReader` 讀取原始 PDF，逐頁取得 `mediabox` 的寬與高。
4. `_create_watermark_page()` 使用 ReportLab 在記憶體中產生同尺寸的單頁 PDF。
5. 原始頁面先加入 `PdfWriter`，再以 `merge_page()` 將浮水印疊加到 writer 所管理的頁面。
6. 所有頁面處理完成後，輸出為 `<原始檔名>_wm.pdf`。

浮水印頁使用 `io.BytesIO`，因此合併過程不需要建立暫存 PDF。

## 浮水印版面

- 字體大小為頁面短邊的五分之一：`min(width, height) / 5`。
- 畫布原點先移到頁面中央，再旋轉 45 度。
- `drawCentredString()` 讓文字在旋轉後的水平軸上置中。
- 填色為黑色，透明度為 15%。
- 每頁個別建立浮水印，因此同一份文件可以混用 A4、Letter、A3 等尺寸。

## 字型處理

所有浮水印文字都使用套件隨附的 `NotoSansTC-Regular.ttf`。`importlib.resources` 會以套件資源方式定位字型，`TTFont` 則將實際使用的字形子集嵌入浮水印 PDF。合併後的頁面因此不依賴渲染環境安裝相同字型。

字型只會在程序中註冊一次，避免處理多頁或多檔案時重複解析。字型採用 SIL Open Font License 1.1，授權全文隨套件置於 `src/pdf_watermark/fonts/OFL.txt`。

## 輸出與錯誤行為

- 未指定輸出路徑時，輸出會放在輸入檔旁，並加入 `_wm` 後綴。
- 公開的 Python API `add_watermark()` 可透過 `output_path` 指定其他位置。
- CLI 會依序處理多個檔案；若讀取、合併或寫入發生例外，程式會停止並由命令列顯示錯誤。
- 核心函式不會修改原始輸入檔。

## 已知限制

- CLI 尚未提供輸出路徑、角度、透明度、顏色與字體選項。
- 版面尺寸以 `mediabox` 為準，特殊的 `cropbox` 或頁面旋轉設定可能需要額外處理。
- 內嵌字型可避免系統字型相依，但會使輸出檔案稍微增大。
- 加密、損壞或權限受限的 PDF 可能無法處理。

## 驗證方式

```powershell
uv build
uv run python -m unittest discover -s tests
uv run create_test_pdf.py
uv run pdf-watermark --text "機密 Confidential" test.pdf
```

單元測試會檢查輸出頁面的 Noto Sans TC 字型資源是否包含內嵌的 `/FontFile2`。建置應產生 wheel 與 source distribution；功能測試應產生 `test_wm.pdf`，並保留三頁不同的頁面尺寸。
