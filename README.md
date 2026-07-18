# pdf-watermark

為 PDF 的每一頁加入置中、半透明的對角文字浮水印。

[English](README.en.md) | 繁體中文

## 功能

- 支援單一或多個 PDF 檔案。
- 每一頁會依原始頁面尺寸個別產生浮水印。
- 可自訂浮水印文字，並支援中文文字。
- 內嵌 Noto Sans TC 字型子集，不依賴閱讀器的系統字型。
- 原始檔案不會被覆寫。

## 系統需求

- Python 3.14 或更新版本
- [uv](https://docs.astral.sh/uv/)

## 直接執行

不需安裝即可從專案目錄執行：

```powershell
uvx . input.pdf
uvx . --text "Top Secret" input.pdf
```

## 安裝最新版本

```powershell
uv tool install git+https://github.com/codemee/pdf_watermark.git@latest
pdf-watermark input.pdf
```

`latest` 標籤會隨每次正式版本更新。若已安裝，使用以下指令更新至最新版本：

```powershell
uv tool install --force git+https://github.com/codemee/pdf_watermark.git@latest
```

此 repository 為 private 時，安裝者必須具有 GitHub 存取權限，且 Git 已設定可用的認證。

## 使用方式

使用預設文字 `Confidential`：

```powershell
pdf-watermark input.pdf
```

指定文字：

```powershell
pdf-watermark --text "機密文件" input.pdf
```

一次處理多個檔案：

```powershell
pdf-watermark file1.pdf file2.pdf
```

可一次處理多個檔案；輸出預設位於原檔旁，檔名為
`<原始檔名>_wm.pdf`。

## 開發與驗證

```powershell
uv sync
uv run create_test_pdf.py
uv run pdf-watermark --text "機密 Confidential" test.pdf
```

`test.pdf` 包含 A4、Letter 與 A3 三種頁面尺寸，產生的 `test_wm.pdf` 可用於人工檢查結果。

## 實作細節

請參閱[實作細節解說](docs/implementation.zh-TW.md)。

## 字型授權

本專案隨附的 Noto Sans TC 由 Google Fonts 提供，採用 SIL Open Font License 1.1；完整條款位於 `src/pdf_watermark/fonts/OFL.txt`。
