# pdf-watermark

為 PDF 的每一頁加入置中、半透明的對角文字浮水印。

[English](https://github.com/codemee/pdf_watermark/blob/main/README.en.md) | 繁體中文

## 功能

- 支援單一或多個 PDF 檔案。
- 每一頁會依原始頁面尺寸個別產生浮水印。
- 可自訂浮水印文字，並支援中文文字。
- 長文字會依頁面可用的對角寬度自動縮小，避免超出頁面。
- 內嵌 Noto Sans TC 字型子集，不依賴閱讀器的系統字型。
- 原始檔案不會被覆寫。

## 系統需求

- Windows、macOS 或 Linux
- Python 3.12 或更新版本
- [uv](https://docs.astral.sh/uv/)

## 從 PyPI 安裝（建議）

本專案在 PyPI 上的套件名稱是 [`pdfcwm`](https://pypi.org/project/pdfcwm/)，安裝後的命令仍是 `pdf-watermark`。未指定版本時，uv 會安裝最新版本：

```console
uv tool install pdfcwm
pdf-watermark input.pdf
```

不安裝、直接執行：

```console
uvx --from pdfcwm pdf-watermark input.pdf
```

更新至最新版：

```console
uv tool upgrade pdfcwm
```

### 安裝特定版本（補充）

例如安裝 `0.0.5`：

```console
uv tool install pdfcwm@0.0.5
```

## 不使用 Git：下載最新版 ZIP 後執行

此 repository 為 public。以下網址會由 [GitHub Latest Release](https://github.com/codemee/pdf_watermark/releases/latest) 自動指向最新正式版本，不需要安裝或使用 Git。

Windows PowerShell：

```powershell
Invoke-WebRequest `
  https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip `
  -OutFile pdf-watermark-source.zip
Expand-Archive pdf-watermark-source.zip -DestinationPath pdf-watermark-source
Set-Location pdf-watermark-source\pdf_watermark
```

macOS 或 Linux：

```sh
curl -L https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip \
  -o pdf-watermark-source.zip
unzip pdf-watermark-source.zip -d pdf-watermark-source
cd pdf-watermark-source/pdf_watermark
```

也可以在任何平台的 GitHub 頁面選擇 **Code > Download ZIP**，解壓後進入專案目錄。

不需安裝即可執行：

```console
uvx --from . pdf-watermark input.pdf
uvx --from . pdf-watermark --text "Top Secret" input.pdf
```

若要永久安裝 `pdf-watermark` 指令：

```console
uv tool install .
pdf-watermark input.pdf
```

也可以不手動下載或解壓，直接從 ZIP URL 安裝：

```console
uv tool install "pdfcwm @ https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip"
pdf-watermark input.pdf
```

以上方式都不需要 Git。uv 仍會透過 HTTPS 下載 Python 與 Python 套件相依項目。

若已安裝，使用相同網址更新至最新正式版本：

```console
uv tool install --force "pdfcwm @ https://github.com/codemee/pdf_watermark/releases/latest/download/pdf-watermark-source.zip"
```

## 使用 Git 安裝預設分支最新內容

```console
uv tool install git+https://github.com/codemee/pdf_watermark.git
pdf-watermark input.pdf
```

此方式取得預設分支的最新內容，可能包含尚未正式發布的變更。若已安裝，使用以下指令更新：

```console
uv tool install --force git+https://github.com/codemee/pdf_watermark.git
```

此安裝方式需要系統上有 Git。若只想更新以 ZIP URL 安裝的版本，也可重新執行對應的 `uv tool install` 指令並加上 `--force`。

## 使用方式

使用預設文字 `Confidential`：

```console
pdf-watermark input.pdf
```

指定文字：

```console
pdf-watermark --text "機密文件" input.pdf
```

一次處理多個檔案：

```console
pdf-watermark file1.pdf file2.pdf
```

可一次處理多個檔案；輸出預設位於原檔旁，檔名為
`<原始檔名>_wm.pdf`。

## 開發與驗證

```console
uv sync
uv run create_test_pdf.py
uv run pdf-watermark --text "機密 Confidential" test.pdf
```

`test.pdf` 包含 A4、Letter 與 A3 三種頁面尺寸，產生的 `test_wm.pdf` 可用於人工檢查結果。

## 實作細節

請參閱[實作細節解說](https://github.com/codemee/pdf_watermark/blob/main/docs/implementation.zh-TW.md)。

## 字型授權

本專案隨附的 Noto Sans TC 由 Google Fonts 提供，採用 SIL Open Font License 1.1；完整條款位於 `src/pdf_watermark/fonts/OFL.txt`。
