# API Key 管理遷移說明

## 📌 重要更新

自 V3 版本起，所有 API Keys 已從 `config.py` 遷移至 `.env` 檔案，以提升安全性。

## 🔄 改變內容

### 之前（V2 及更早版本）
```python
# config.py
SERPAPI_KEYS = [
    "your_key_1",
    "your_key_2",
]
SCRAPINGDOG_API_KEY = "your_key"
```

### 現在（V3+）
```bash
# .env
SERPAPI_KEYS=your_key_1,your_key_2,your_key_3
SCRAPINGDOG_API_KEY=your_key
APIFY_API_TOKEN=your_token
```

## ✅ GUI 自動連動

### GUI 更新功能

當您在 GUI 中更新 API Keys 時：

1. **自動寫入 .env 檔案**
   - 不再寫入 config.py
   - 直接更新 `.env` 檔案內容

2. **立即生效**
   - 更新當前程序的環境變數
   - 重新載入 config 模組
   - 無需重啟程式

3. **支援多組 SERP API Keys**
   - 在 GUI 中每行輸入一組 key
   - 自動轉換為逗號分隔格式存入 .env
   - 當一組達到限制時自動切換

### 測試更新功能

```bash
# 執行測試腳本
python tests/test_env_update.py
```

## 🔒 安全性改進

### 為什麼要遷移？

1. **避免意外洩露**
   - `.env` 在 `.gitignore` 中，不會被提交到 Git
   - `config.py` 是程式碼檔案，容易被意外提交

2. **符合最佳實踐**
   - 環境變數是管理機密資訊的標準做法
   - 與業界標準一致（Twelve-Factor App）

3. **易於管理**
   - 集中管理所有機密資訊
   - 使用 `.env.example` 作為範本

### 安全檢查清單

- [ ] 確認 `.env` 存在且包含您的 API Keys
- [ ] 確認 `.env` 已在 `.gitignore` 中
- [ ] 確認 `config.py` 不再包含寫死的 API Keys
- [ ] 如果之前有提交包含 keys 的 config.py，考慮更換 API Keys

## 🛠️ 遷移步驟

如果您是從舊版本升級：

### 1. 建立 .env 檔案

```bash
# 複製範本
copy .env.example .env
```

### 2. 從 config.py 複製 Keys 到 .env

舊的 `config.py`:
```python
SERPAPI_KEYS = ["key1", "key2", "key3"]
SCRAPINGDOG_API_KEY = "your_key"
```

新的 `.env`:
```bash
SERPAPI_KEYS=key1,key2,key3
SCRAPINGDOG_API_KEY=your_key
```

### 3. 更新 config.py

確保您的 `config.py` 包含環境變數載入代碼：

```python
import os
from dotenv import load_dotenv
load_dotenv()

serpapi_keys_str = os.getenv('SERPAPI_KEYS', '')
SERPAPI_KEYS = [key.strip() for key in serpapi_keys_str.split(',') if key.strip()]

SCRAPINGDOG_API_KEY = os.getenv('SCRAPINGDOG_API_KEY', '')
```

### 4. 測試

```bash
python tests/test_env_update.py
```

## 💡 常見問題

### Q: GUI 更新後，命令行程式會讀到新的 key 嗎？

**A:** 會的！GUI 更新 `.env` 後：
- 新啟動的命令行程式會讀到新值
- GUI 本身立即生效（有重新載入機制）

### Q: 我可以直接編輯 .env 檔案嗎？

**A:** 可以！兩種方式都可以：
1. 使用 GUI 的「更新」按鈕
2. 直接用文字編輯器編輯 `.env`

### Q: 舊的 config.py 設定會怎樣？

**A:** `config.py` 現在從 `.env` 讀取，不再使用寫死的值。

### Q: 多組 SERP API Keys 如何切換？

**A:** 自動切換！當一組達到限制時，程式會自動使用下一組。

## 📝 相關檔案

- `.env` - 實際的 API Keys（不要提交到 Git）
- `.env.example` - 範本檔案（可以提交）
- `config.py` - 從 .env 讀取配置
- `gui_app.py` - GUI 更新功能實作
- `tests/test_env_update.py` - 測試腳本

## 🔗 更多資訊

- [Twelve-Factor App 方法論](https://12factor.net/config)
- [python-dotenv 文件](https://pypi.org/project/python-dotenv/)
