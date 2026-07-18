# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 使用 Python 環境管理

使用 uv 管理 Python 執行環境:

- 必要時使用 `uv init` 初始化資料夾
- 使用 `uv add` 加入套件，不要使用 pip
- 使用 `uv run` 執行 Python 腳本檔

## 常用指令

```bash
# 加浮水印（預設文字 "Confidential"）
uvx . <input.pdf>

# 指定浮水印文字
uvx . --text "Top Secret" <input.pdf>

# 同時處理多個檔案
uvx . file1.pdf file2.pdf

# 安裝為全域 uv tool
uv tool install .

# 產生測試用 PDF（含 A4、Letter、A3 三種頁面尺寸）
uv run create_test_pdf.py

# 加入新套件
uv add <package>
```

## 架構說明

| 檔案 | 用途 |
|---|---|
| `src/pdf_watermark/` | 主程式套件；提供 CLI 與可匯入的 `add_watermark()` 函式 |
| `create_test_pdf.py` | 產生測試用多尺寸 PDF，不屬於核心功能 |

### 浮水印流程（`src/pdf_watermark/__init__.py`）

1. `pypdf.PdfReader` 讀取原始 PDF，逐頁取得 `mediabox` 尺寸。
2. `_create_watermark_page(width, height, text)` 用 **reportlab** 在記憶體（`io.BytesIO`）產生與該頁等尺寸的單頁 PDF，內含 45° 斜角、置中、半透明灰色文字。
3. `page.merge_page(wm_page)` 將浮水印疊加到原始頁面。
4. 輸出檔名為 `<原始檔名>_wm.pdf`，存放於同目錄。

每頁獨立產生浮水印頁，因此可正確處理同一 PDF 內頁面尺寸不一致的情況。
