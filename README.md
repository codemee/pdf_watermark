# pdf-watermark

為 PDF 的每一頁加入置中、半透明的對角文字浮水印。

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

可一次處理多個檔案；輸出預設位於原檔旁，檔名為
`<原始檔名>_wm.pdf`。
