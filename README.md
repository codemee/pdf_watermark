# pdf-watermark

為 PDF 的每一頁加入置中、半透明的對角文字浮水印。

## 直接執行

不需安裝即可從專案目錄執行：

```powershell
uvx . input.pdf
uvx . --text "Top Secret" input.pdf
```

## 安裝為 uv tool

```powershell
uv tool install .
pdf-watermark input.pdf
```

更新本機安裝：

```powershell
uv tool install . --force
```

可一次處理多個檔案；輸出預設位於原檔旁，檔名為
`<原始檔名>_wm.pdf`。
