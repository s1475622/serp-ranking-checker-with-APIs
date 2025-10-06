# SERP 排名追蹤器

這個工具用於追蹤關鍵字在Google搜尋結果中的排名位置。提供三種API方法和圖形化操作介面：
1. 使用SERP API（推薦）
2. 使用Scrapingdog API（備用方案）
3. 使用Apify爬蟲（備用方案）

## 快速開始

### 圖形化介面（最簡單）
1. 執行 `run_gui.bat` 啟動完整的圖形化界面
2. 在視窗中配置所有設定
3. 點擊按鈕開始搜尋

### 命令行介面（互動式選單）
1. 執行 `easy_run.bat` 使用互動式選單
2. 從主選單中選擇需要的功能
3. 按照提示完成設定

### 首次安裝

1. **安裝依賴套件**
   ```bash
   pip install -r requirements.txt
   ```

2. **設定 API Keys（重要！）**
   ```bash
   # 複製環境變數範本
   copy .env.example .env

   # 編輯 .env 檔案，填入您的 API Keys
   notepad .env
   ```

3. **執行設置腳本**（可選）
   ```bash
   setup_api.bat
   ```

> ⚠️ **安全提醒**：
> - `.env` 檔案包含您的 API Keys，請勿上傳到 Git 或公開分享
> - `.env` 已在 `.gitignore` 中，正常情況不會被提交
> - 如需分享專案，請只分享 `.env.example` 範本檔案

## 圖形化介面（GUI）

### 特點
- 完整的圖形化操作界面
- 即時顯示搜尋進度和結果
- 儲存和載入設定
- 支援所有API方法切換
- 內建關鍵字編輯器
- 自動保存設定

### 使用方法
1. 執行 `run_gui.bat`
2. 在GUI中設定：
   - 選擇API方法（SERP API / Scrapingdog / Apify）
   - 輸入API金鑰
   - 選擇搜尋地區（可多選）
   - 設定目標網域
   - 選擇關鍵字檔案
   - 設定請求延遲時間
3. 點擊「開始搜尋」按鈕
4. 即時查看搜尋進度
5. 完成後結果會自動儲存並顯示路徑

## 命令行介面（CLI）

### 特點
- 互動式選單界面，操作簡單
- 可輕鬆選擇多個搜尋地區
- 提供詳細使用說明
- 整合所有功能於一個程式中

### 使用方法
1. 執行 `easy_run.bat`
2. 從主選單中選擇需要的功能：
   - 開始新的搜尋
   - 查看使用說明
   - 設定 SERP API 金鑰
   - 退出程式
3. 搜尋設定中可以：
   - 選擇單個或多個搜尋地區（美國、台灣、香港）
   - 輸入要追蹤的目標網域
   - 確認設定並執行搜尋
4. 結果會保存在 `results` 資料夾中

## SERP API 版本（推薦）

### 特點
- 更穩定可靠，不會被Google封鎖
- 不需要啟動瀏覽器
- 不需要手動解決驗證碼
- 處理速度更快

### 使用方法
1. 註冊獲取SERP API密鑰
   - 訪問 https://serpapi.com 註冊賬號
   - 免費方案提供每月100次查詢
   - 複製API密鑰備用

2. 運行程序
   - 執行 `setup_api.bat` 進行首次安裝和設置
   - 或使用 `easy_run.bat` 的互動式選單執行

3. 輸入API密鑰
   - 在提示處輸入您的SERP API密鑰
   - 或者您可以直接在`config.py`中設置`SERPAPI_KEY`

4. 查看結果
   - 結果將保存在`results`資料夾中
   - 檔案名格式為`serp_results_YYYYMMDD_HHMMSS.csv`

### 命令行選項
```
python serp_api_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_API_KEY
```
- `--regions`: 要搜索的地區（US、TW、HK）
- `--domain`: 目標網域
- `--keywords_file`: 關鍵字檔案路徑
- `--api_key`: SERP API密鑰

## Scrapingdog API 版本（備用方案）

### 特點
- 使用Scrapingdog API服務
- 支援分頁獲取最多100個搜尋結果
- 自動優化：找到目標網域後立即停止，節省API配額
- 不需要啟動瀏覽器

### 使用方法
1. 註冊獲取Scrapingdog API密鑰
   - 訪問 https://www.scrapingdog.com 註冊賬號
   - 提供免費試用方案
   - 複製API密鑰備用

2. 設置API密鑰
   - 在`config.py`中設置`SCRAPINGDOG_API_KEY`
   - 或使用`--api_key`參數提供

3. 運行程序
   - 使用 `easy_run.bat` 的互動式選單執行
   - 或直接執行：`python scrapingdog_crawler.py --regions US TW --domain example.com`

## Apify 爬蟲版本（備用方案）

### 特點
- 使用Apify的Google Search Scraper服務
- 不需要啟動瀏覽器
- 需要APIFY_API_TOKEN環境變數

### 使用方法
1. 註冊獲取Apify API令牌
   - 訪問 https://apify.com 註冊賬號
   - 複製API令牌備用

2. 設置環境變數
   - 設置`APIFY_API_TOKEN`環境變數

3. 運行程序
   - 使用 `easy_run.bat` 的互動式選單執行
   - 或直接執行：`python apify_crawler.py`

## 配置設定

### API Keys 配置（.env 檔案）

**重要：API Keys 現在統一在 `.env` 檔案中設定**

```bash
# SERP API Keys（支援多組，用逗號分隔）
SERPAPI_KEYS=your_key1,your_key2,your_key3

# Scrapingdog API Key
SCRAPINGDOG_API_KEY=your_scrapingdog_key

# Apify API Token
APIFY_API_TOKEN=your_apify_token
```

### 其他設定（config.py 檔案）

```python
# 搜尋區域
SELECTED_REGIONS = ['TW']  # 預設搜尋台灣

# 目標網域
TARGET_DOMAIN = 'mall.sfworldwide.com'

# API 請求延遲
API_DELAY_BETWEEN_REQUESTS = 5
SCRAPINGDOG_DELAY_BETWEEN_REQUESTS = 5

# 輸出設置
OUTPUT_FOLDER = 'results'
OUTPUT_FILE_FORMAT = 'csv'  # 或 'excel'
```

> 💡 **提示**：API Keys 已從 `config.py` 移至 `.env` 以提升安全性

## 專案結構

```
SERP Crawler/
├── .env.example          # 環境變數範本
├── .gitignore           # Git 忽略檔案
├── README.md            # 主要說明文件
├── CLAUDE.md            # AI 開發文件
├── requirements.txt     # Python 依賴套件
│
├── 執行檔
│   ├── run_gui.bat          # 啟動圖形化界面（推薦）
│   ├── easy_run.bat         # 啟動命令行互動式選單
│   ├── setup_api.bat        # 首次安裝和環境設置
│   ├── analyze_ranks.bat    # 分析排名結果
│   └── run_test.bat         # 執行測試
│
├── 主程式
│   ├── gui_app.py              # GUI 圖形化介面
│   ├── serp_api_crawler.py     # SERP API 爬蟲
│   ├── scrapingdog_crawler.py  # Scrapingdog 爬蟲
│   ├── apify_crawler.py        # Apify 爬蟲
│   ├── keywords_manager.py     # 關鍵字管理
│   ├── rank_analyzer.py        # 排名分析
│   └── config.py               # 配置檔案
│
├── tests/               # 測試檔案
│   ├── __init__.py
│   ├── test_apify_crawler.py
│   ├── test_keywords_reader.py
│   ├── serp_api_test.py
│   ├── test_output.py
│   └── test_keywords.csv
│
├── docs/                # 文件目錄
│   ├── README.md
│   └── images/         # 截圖和圖片
│
├── results/             # 搜尋結果輸出
│   └── archive/        # 歷史結果
│
├── archive/             # 歷史檔案
│   └── README_GUI.md   # 舊版 GUI 說明
│
└── keywords.csv         # 關鍵字檔案
```

## 執行檔說明

- `run_gui.bat` - 啟動圖形化界面（推薦）
- `easy_run.bat` - 啟動命令行互動式選單
- `setup_api.bat` - 首次安裝和環境設置
- `analyze_ranks.bat` - 分析排名結果
- `run_test.bat` - 執行測試

## 關鍵字文件格式

關鍵字文件應為CSV格式，包含以下列：
```
keyword,domain
digital signage,agiledisplaysolutions.com
high brightness display,agiledisplaysolutions.com
...
```

## 測試

測試檔案位於 `tests/` 資料夾：
- `tests/test_apify_crawler.py` - 測試 Apify 爬蟲
- `tests/test_keywords_reader.py` - 測試關鍵字讀取器
- `tests/serp_api_test.py` - 測試 SERP API 爬蟲

執行 `run_test.bat` 來運行所有測試

## 排名結果說明

- 正數值（1-100）：實際排名位置
- -1：關鍵字在前100個結果中未找到目標網站
- -2：搜索過程出錯

## GUI 詳細功能說明

### 介面元件

#### API 服務選擇
- **SERP API（推薦）**：穩定可靠，免費每月 100 次查詢
- **Scrapingdog API**：提供免費試用方案
- **Apify API**：適合大量爬取需求

#### 搜尋地區
- **美國 (US)**：英文搜尋，google.com
- **台灣 (TW)**：繁體中文搜尋，google.com.tw
- **香港 (HK)**：繁體中文搜尋，google.com.hk
- 可同時選擇多個地區

#### 目標網域
- 所有關鍵字都使用此網域進行排名追蹤
- keywords.csv 不需要 domain 欄位
- 更換網域只需修改此欄位

#### 控制按鈕
- **開始搜尋**：開始執行爬蟲
- **停止**：中斷執行（執行中才可用）
- **開啟結果資料夾**：快速開啟 results 資料夾
- **測試輸出**：測試即時輸出功能

### 使用技巧

#### 1. 設定會自動儲存
每次點擊「開始搜尋」時，會自動儲存設定到 `gui_settings.json`

#### 2. 網域管理
- 不需要在 keywords.csv 中設定 domain
- 所有關鍵字共用 GUI 中設定的網域

#### 3. 即時監控
- 執行紀錄會即時顯示進度
- 可以看到每個關鍵字的搜尋狀態

#### 4. 多地區搜尋
- 可同時勾選多個地區
- 結果會分別記錄

### 智慧編碼處理
- 自動偵測系統編碼
- 支援 UTF-8, Big5, GBK 等多種編碼
- 中文輸出不會亂碼

## 常見問題

### 一般問題

**Q: 看不到執行過程怎麼辦？**
A: 點擊「測試輸出」驗證功能，確認執行紀錄區在視窗下方

**Q: 中文顯示亂碼？**
A: 程式已自動處理編碼問題，支援多種編碼格式

**Q: keywords.csv 需要 domain 欄位嗎？**
A: GUI 模式不需要，只要 `keyword` 欄位即可。命令行模式需要 `keyword` 和 `domain` 欄位。

**Q: 設定會保留嗎？**
A: 會自動儲存到 `gui_settings.json`

**Q: 執行中可以停止嗎？**
A: 可以，點擊「停止」按鈕即可中斷

**Q: 結果儲存在哪裡？**
A: `results/` 資料夾，點擊「開啟結果資料夾」可快速開啟

### API 相關問題

1. **SERP API報錯"無效的API密鑰"**
   - 確認您已正確複製API密鑰
   - 確認API密鑰未過期或用量未超限

2. **Scrapingdog API報錯**
   - 確認您已正確設置API密鑰
   - 確認API密鑰未過期或用量未超限

3. **Apify API報錯**
   - 確認APIFY_API_TOKEN環境變數已正確設置
   - 確認API令牌有效且有足夠配額

4. **關鍵字文件格式錯誤**
   - GUI模式：確保CSV文件包含`keyword`列
   - 命令行模式：確保CSV文件包含`keyword`和`domain`列
   - 確保文件使用UTF-8編碼 