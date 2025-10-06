# SERP 排名追蹤器

一個功能完整的Google搜尋排名追蹤工具，支援多地區、多API方法，提供圖形化介面和命令行介面。

## 主要特點

✨ **雙介面設計**
- 🖥️ 圖形化介面（GUI）- 直觀易用，即時顯示進度
- ⌨️ 命令行介面（CLI）- 互動式選單，適合自動化

🌍 **多地區支援**
- 美國 (US) - google.com
- 台灣 (TW) - google.com.tw
- 香港 (HK) - google.com.hk

🔌 **三種API方法**
1. SERP API（推薦）- 穩定可靠，免費每月100次查詢
2. Scrapingdog API（備用）- 提供免費試用
3. Apify Crawler（備用）- 適合大量爬取

## 快速開始

### 方法 1：圖形化介面（推薦新手）
```bash
# 直接執行
run_gui.bat
```
1. 啟動圖形化界面
2. 在視窗中配置API金鑰、搜尋地區、目標網域
3. 選擇關鍵字檔案
4. 點擊「開始搜尋」

### 方法 2：命令行介面（適合進階用戶）
```bash
# 互動式選單
easy_run.bat
```
1. 從主選單選擇功能
2. 按照提示輸入設定
3. 自動執行並儲存結果

## 安裝步驟

### 1. 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2. 設定 API Keys（重要！）
```bash
# 步驟 1: 複製環境變數範本
copy .env.example .env

# 步驟 2: 編輯 .env 檔案，填入您的 API Keys
notepad .env
```

在 `.env` 檔案中設定：
```bash
# SERP API Keys（支援多組，用逗號分隔）
SERPAPI_KEYS=your_key1,your_key2,your_key3

# Scrapingdog API Key
SCRAPINGDOG_API_KEY=your_scrapingdog_key

# Apify API Token
APIFY_API_TOKEN=your_apify_token
```

### 3. 執行設置腳本（可選）
```bash
setup_api.bat
```

> ⚠️ **安全提醒**
> - `.env` 檔案包含您的 API Keys，請勿上傳到 Git 或公開分享
> - `.env` 已在 `.gitignore` 中，正常情況不會被提交
> - 如需分享專案，請只分享 `.env.example` 範本檔案

### 4. 準備關鍵字檔案
建立或編輯 `keywords.csv`，格式如下：
```csv
keyword
digital signage
high brightness display
interactive kiosk
```

**注意**：GUI模式只需要 `keyword` 欄位，CLI模式需要 `keyword` 和 `domain` 欄位。

## 使用指南

### 圖形化介面（GUI）

#### 主要功能
- ✅ 直觀的圖形化操作界面
- ✅ 即時顯示搜尋進度和日誌
- ✅ 自動儲存和載入設定
- ✅ 支援所有API方法切換
- ✅ 內建關鍵字檔案選擇器
- ✅ 可同時選擇多個搜尋地區

#### 操作步驟
1. **啟動程式**
   ```bash
   run_gui.bat
   ```

2. **配置設定**
   - **API 服務**：選擇 SERP API / Scrapingdog / Apify
   - **API 金鑰**：輸入對應的API金鑰
   - **搜尋地區**：勾選一個或多個地區（US / TW / HK）
   - **目標網域**：輸入要追蹤的網域（例如：example.com）
   - **關鍵字檔案**：點擊「瀏覽」選擇 keywords.csv
   - **請求延遲**：設定API請求間隔秒數

3. **執行搜尋**
   - 點擊「開始搜尋」按鈕
   - 在「執行紀錄」區即時查看進度
   - 可隨時點擊「停止」中斷執行

4. **查看結果**
   - 完成後會顯示結果檔案路徑
   - 點擊「開啟結果資料夾」快速查看
   - 結果儲存在 `results/` 資料夾

### 命令行介面（CLI）

#### 主要功能
- ⌨️ 互動式選單界面，操作簡單
- ⌨️ 可輕鬆選擇多個搜尋地區
- ⌨️ 提供詳細使用說明
- ⌨️ 整合所有功能於單一程式

#### 操作步驟
1. **啟動選單**
   ```bash
   easy_run.bat
   ```

2. **選擇功能**
   - 開始新的搜尋
   - 查看使用說明
   - 設定 SERP API 金鑰
   - 退出程式

3. **設定搜尋參數**
   - 選擇搜尋地區（可多選）
   - 輸入目標網域
   - 確認設定並執行

4. **查看結果**
   - 結果自動儲存在 `results/` 資料夾
   - 檔名格式：`serp_results_YYYYMMDD_HHMMSS.csv`

## API 服務說明

### SERP API（推薦）

#### 優點
- ✅ 更穩定可靠，不會被Google封鎖
- ✅ 不需要啟動瀏覽器
- ✅ 不需要手動解決驗證碼
- ✅ 處理速度更快
- ✅ 支援多組API金鑰自動切換

#### 申請與設定
1. **註冊獲取API密鑰**
   - 訪問 [https://serpapi.com](https://serpapi.com) 註冊賬號
   - 免費方案提供每月100次查詢
   - 複製API密鑰

2. **設定環境變數**
   ```bash
   # 在 .env 檔案中設定（支援多組，用逗號分隔）
   SERPAPI_KEYS=your_key1,your_key2,your_key3
   ```

3. **使用方式**
   - **GUI**：在介面中選擇「SERP API」並輸入金鑰
   - **CLI**：執行 `easy_run.bat` 並選擇設定選項
   - **命令行**：
     ```bash
     python serp_api_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY
     ```

#### 命令行參數
- `--regions` - 搜尋地區（US、TW、HK）
- `--domain` - 目標網域
- `--keywords_file` - 關鍵字檔案路徑
- `--api_key` - SERP API密鑰

### Scrapingdog API（備用方案）

#### 優點
- 支援分頁獲取最多100個搜尋結果
- 自動優化：找到目標網域後立即停止，節省API配額
- 不需要啟動瀏覽器
- 提供免費試用方案

#### 申請與設定
1. **註冊獲取API密鑰**
   - 訪問 [https://www.scrapingdog.com](https://www.scrapingdog.com) 註冊賬號
   - 複製API密鑰

2. **設定環境變數**
   ```bash
   # 在 .env 檔案中設定
   SCRAPINGDOG_API_KEY=your_scrapingdog_key
   ```

3. **使用方式**
   - **GUI**：在介面中選擇「Scrapingdog API」並輸入金鑰
   - **CLI**：執行 `easy_run.bat`
   - **命令行**：
     ```bash
     python scrapingdog_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY
     ```

### Apify Crawler（備用方案）

#### 優點
- 使用Apify的Google Search Scraper服務
- 適合大量爬取需求
- 不需要啟動瀏覽器

#### 申請與設定
1. **註冊獲取API令牌**
   - 訪問 [https://apify.com](https://apify.com) 註冊賬號
   - 複製API令牌

2. **設定環境變數**
   ```bash
   # 在 .env 檔案中設定
   APIFY_API_TOKEN=your_apify_token
   ```

3. **使用方式**
   - **GUI**：在介面中選擇「Apify API」並輸入金鑰
   - **CLI**：執行 `easy_run.bat`
   - **命令行**：
     ```bash
     python apify_crawler.py
     ```

## 進階配置

### 環境變數設定（.env 檔案）

**重要：API Keys 統一在 `.env` 檔案中設定**

```bash
# SERP API Keys（支援多組，用逗號分隔，達到限制時自動切換）
SERPAPI_KEYS=your_key1,your_key2,your_key3

# Scrapingdog API Key
SCRAPINGDOG_API_KEY=your_scrapingdog_key

# Apify API Token
APIFY_API_TOKEN=your_apify_token
```

> 💡 **提示**：API Keys 從 `config.py` 移至 `.env` 以提升安全性

### 程式設定（config.py 檔案）

```python
# 搜尋區域配置
ALL_REGIONS = {
    'US': {'lang': 'en', 'country': 'us', 'domain': 'google.com'},
    'TW': {'lang': 'zh-TW', 'country': 'tw', 'domain': 'google.com.tw'},
    'HK': {'lang': 'zh-TW', 'country': 'hk', 'domain': 'google.com.hk'}
}

# 預設搜尋設定
SELECTED_REGIONS = ['TW']  # 預設搜尋台灣
TARGET_DOMAIN = 'mall.sfworldwide.com'  # 預設目標網域

# API 請求延遲（秒）
API_DELAY_BETWEEN_REQUESTS = 5
SCRAPINGDOG_DELAY_BETWEEN_REQUESTS = 5

# 輸出設定
OUTPUT_FOLDER = 'results'
OUTPUT_FILE_FORMAT = 'csv'  # 或 'excel'
```

### 新增搜尋地區

若要新增其他國家/地區，在 `config.py` 中新增：

```python
'JP': {'lang': 'ja', 'country': 'jp', 'domain': 'google.co.jp'}
```

## 輸出結果說明

### 結果檔案格式

結果以CSV格式儲存在 `results/` 資料夾，包含以下欄位：

| 欄位 | 說明 |
|------|------|
| `keyword` | 搜尋關鍵字 |
| `region` | 搜尋地區（US/TW/HK） |
| `rank` | 排名位置 |
| `url` | 找到的網址 |
| `title` | 頁面標題 |
| `snippet` | 搜尋結果摘要 |

### 排名數值說明

- **1-100**：實際排名位置（數字越小排名越前）
- **-1**：前100個結果中未找到目標網站
- **-2**：搜尋過程發生錯誤

### 檔案命名規則

```
results/serp_results_YYYYMMDD_HHMMSS.csv
```

範例：`serp_results_20250106_143022.csv`

### 分析結果

使用內建分析工具：
```bash
analyze_ranks.bat
```

## 專案結構

```
SERP Crawler/
├── 📄 設定檔案
│   ├── .env                 # API Keys（不會上傳到Git）
│   ├── .env.example         # 環境變數範本
│   ├── .gitignore          # Git 忽略檔案
│   ├── config.py           # 程式配置檔案
│   ├── requirements.txt    # Python 依賴套件
│   └── gui_settings.json   # GUI 設定儲存
│
├── 📝 文件
│   ├── README.md           # 主要說明文件（本檔案）
│   └── CLAUDE.md           # AI 開發文件
│
├── 🚀 執行檔
│   ├── run_gui.bat         # 啟動圖形化界面（推薦）
│   ├── easy_run.bat        # 啟動命令行互動式選單
│   ├── setup_api.bat       # 首次安裝和環境設置
│   ├── analyze_ranks.bat   # 分析排名結果
│   └── run_test.bat        # 執行測試
│
├── 💻 主程式
│   ├── gui_app.py              # GUI 圖形化介面
│   ├── serp_api_crawler.py     # SERP API 爬蟲
│   ├── scrapingdog_crawler.py  # Scrapingdog 爬蟲
│   ├── apify_crawler.py        # Apify 爬蟲
│   ├── keywords_manager.py     # 關鍵字管理
│   └── rank_analyzer.py        # 排名分析工具
│
├── 🧪 測試檔案
│   └── tests/
│       ├── test_apify_crawler.py
│       ├── test_keywords_reader.py
│       ├── serp_api_test.py
│       └── test_keywords.csv
│
├── 📊 資料檔案
│   ├── keywords.csv        # 關鍵字檔案（輸入）
│   └── results/           # 搜尋結果（輸出）
│       └── archive/       # 歷史結果
│
├── 📚 文件目錄
│   └── docs/
│       ├── README.md
│       └── images/        # 截圖和圖片
│
└── 📦 歷史檔案
    └── archive/           # 舊版檔案

## 測試

### 執行測試
```bash
run_test.bat
```

### 測試檔案
- `tests/test_apify_crawler.py` - 測試 Apify 爬蟲
- `tests/test_keywords_reader.py` - 測試關鍵字讀取器
- `tests/serp_api_test.py` - 測試 SERP API 爬蟲

## 技術特點

### 智慧編碼處理
- ✅ 自動偵測系統編碼
- ✅ 支援 UTF-8, Big5, GBK 等多種編碼
- ✅ 中文輸出不會亂碼

### GUI 功能特點
- ✅ 設定自動儲存到 `gui_settings.json`
- ✅ 即時顯示搜尋進度和日誌
- ✅ 支援中斷執行（停止按鈕）
- ✅ 快速開啟結果資料夾
- ✅ 統一網域管理（keywords.csv 不需要 domain 欄位）

### API 金鑰管理
- ✅ 支援多組 SERP API 金鑰自動切換
- ✅ 安全儲存在 .env 檔案（不會上傳到 Git）
- ✅ 可在 GUI 或 CLI 中輸入

## 常見問題（FAQ）

### 一般問題

<details>
<summary><b>Q: GUI 看不到執行過程怎麼辦？</b></summary>

點擊「測試輸出」驗證功能，確認執行紀錄區在視窗下方。
</details>

<details>
<summary><b>Q: 中文顯示亂碼？</b></summary>

程式已自動處理編碼問題，支援 UTF-8、Big5、GBK 等多種編碼格式。
</details>

<details>
<summary><b>Q: keywords.csv 需要 domain 欄位嗎？</b></summary>

- **GUI 模式**：不需要，只要 `keyword` 欄位即可
- **CLI 模式**：需要 `keyword` 和 `domain` 欄位
</details>

<details>
<summary><b>Q: GUI 設定會保留嗎？</b></summary>

會自動儲存到 `gui_settings.json`，下次開啟會自動載入。
</details>

<details>
<summary><b>Q: 執行中可以停止嗎？</b></summary>

可以，點擊「停止」按鈕即可中斷執行。
</details>

<details>
<summary><b>Q: 結果儲存在哪裡？</b></summary>

`results/` 資料夾，點擊「開啟結果資料夾」可快速開啟。
</details>

### API 相關問題

<details>
<summary><b>Q: SERP API 報錯「無效的API密鑰」</b></summary>

- 確認已正確複製 API 密鑰（無多餘空格）
- 確認 API 密鑰未過期或用量未超限
- 檢查 `.env` 檔案格式是否正確
</details>

<details>
<summary><b>Q: 如何使用多組 SERP API 金鑰？</b></summary>

在 `.env` 檔案中用逗號分隔：
```bash
SERPAPI_KEYS=key1,key2,key3
```
系統會自動切換金鑰。
</details>

<details>
<summary><b>Q: Scrapingdog API 報錯</b></summary>

- 確認已正確設置 API 密鑰
- 確認 API 密鑰未過期或用量未超限
- 檢查網路連線是否正常
</details>

<details>
<summary><b>Q: Apify API 報錯</b></summary>

- 確認 `APIFY_API_TOKEN` 環境變數已正確設置
- 確認 API 令牌有效且有足夠配額
- 檢查 `.env` 檔案是否存在且格式正確
</details>

### 檔案相關問題

<details>
<summary><b>Q: 關鍵字文件格式錯誤</b></summary>

- **GUI 模式**：確保 CSV 包含 `keyword` 欄位
- **CLI 模式**：確保 CSV 包含 `keyword` 和 `domain` 欄位
- 確保文件使用 UTF-8 編碼儲存
</details>

<details>
<summary><b>Q: 如何查看歷史搜尋結果？</b></summary>

所有結果儲存在 `results/` 資料夾，檔名包含時間戳記，方便識別。
</details>

## 授權與貢獻

### 授權
本專案為私人專案，僅供內部使用。

### 問題回報
如遇到問題或有建議，請聯絡開發團隊。

---

**最後更新**：2025-01-06
**版本**：2.0
**作者**：Ming 