@echo off
chcp 65001 > nul
title SERP 排名追蹤器 - 友善介面
mode con cols=80 lines=35
color 0A

:MAIN_MENU
cls
echo ======================================================
echo              SERP 排名追蹤器 - 友善介面
echo ======================================================
echo.
echo  請選擇要執行的操作:
echo.
echo  [1] 開始新的搜尋
echo  [2] 查看使用說明
echo  [3] 設定 SERP API 金鑰
echo  [4] 設定 Scrapingdog API 金鑰
echo  [5] 設定 Apify API 金鑰
echo  [6] 退出程式
echo.
echo ======================================================
echo.
set /p CHOICE=請輸入選項 (1-6):

if "%CHOICE%"=="1" goto SELECT_API
if "%CHOICE%"=="2" goto SHOW_HELP
if "%CHOICE%"=="3" goto SET_SERPAPI_KEY
if "%CHOICE%"=="4" goto SET_SCRAPINGDOG_KEY
if "%CHOICE%"=="5" goto SET_APIFY_KEY
if "%CHOICE%"=="6" goto EXIT
goto MAIN_MENU

:SELECT_API
cls
echo ======================================================
echo                 選擇 API 服務
echo ======================================================
echo.
echo  請選擇要使用的 API 服務:
echo.
echo  [1] SERP API (推薦)
echo      - 穩定可靠的 Google 搜尋 API
echo      - 免費方案每月 100 次查詢
echo      - 支援多地區搜尋 (US/TW/HK)
echo.
echo  [2] Scrapingdog API
echo      - 使用 Scrapingdog Google Search API
echo      - 提供免費試用方案
echo      - 支援多地區搜尋 (US/TW/HK)
echo.
echo  [3] Apify API
echo      - 使用 Apify Google Search Scraper
echo      - 需要 APIFY_API_TOKEN 環境變數
echo      - 適合大量爬取需求
echo.
echo  [4] 返回主選單
echo.
echo ======================================================
echo.
set /p API_CHOICE=請選擇 API (1-4):

if "%API_CHOICE%"=="1" (
    set USE_API=SERP
    goto START_SEARCH
)
if "%API_CHOICE%"=="2" (
    set USE_API=SCRAPINGDOG
    goto START_SEARCH
)
if "%API_CHOICE%"=="3" (
    set USE_API=APIFY
    goto RUN_APIFY
)
if "%API_CHOICE%"=="4" goto MAIN_MENU
goto SELECT_API

:START_SEARCH
cls
echo ======================================================
echo                 設定搜尋參數
echo ======================================================
echo.
echo  請選擇搜尋地區 (可多選):
echo.
echo  [1] 美國 (US) - 英文
echo  [2] 台灣 (TW) - 繁體中文
echo  [3] 香港 (HK) - 繁體中文
echo  [4] 全部地區
echo  [5] 返回主選單
echo.
echo  提示: 可以輸入多個數字，例如 "12" 代表選擇美國和台灣
echo ======================================================
echo.
set /p REGION_CHOICE=請選擇地區 (1-5): 

set REGIONS=
if "%REGION_CHOICE%"=="5" goto MAIN_MENU
if "%REGION_CHOICE%"=="4" set REGIONS=US TW HK& goto SET_DOMAIN

set HAS_REGION=0
echo %REGION_CHOICE% | findstr "1" > nul
if not errorlevel 1 (
    set REGIONS=%REGIONS% US
    set HAS_REGION=1
)

echo %REGION_CHOICE% | findstr "2" > nul
if not errorlevel 1 (
    set REGIONS=%REGIONS% TW
    set HAS_REGION=1
)

echo %REGION_CHOICE% | findstr "3" > nul
if not errorlevel 1 (
    set REGIONS=%REGIONS% HK
    set HAS_REGION=1
)

if %HAS_REGION%==0 (
    echo.
    echo 錯誤: 請至少選擇一個地區!
    timeout /t 2 /nobreak > nul
    goto START_SEARCH
)

:SET_DOMAIN
cls
echo ======================================================
echo                 設定目標網域
echo ======================================================
echo.
echo  請輸入要追蹤的目標網域:
echo  (直接按 Enter 使用預設值: mall.sfworldwide.com)
echo.
echo ======================================================
echo.
set /p TARGET_DOMAIN=目標網域: 

if "%TARGET_DOMAIN%"=="" set TARGET_DOMAIN=mall.sfworldwide.com

:CONFIRM_SETTINGS
cls
echo ======================================================
echo                 確認搜尋設定
echo ======================================================
echo.
echo  搜尋地區: %REGIONS%
echo  目標網域: %TARGET_DOMAIN%
echo  關鍵字檔: keywords.csv
echo.
echo  [1] 開始搜尋
echo  [2] 重新設定
echo  [3] 返回主選單
echo.
echo ======================================================
echo.
set /p CONFIRM=請選擇 (1-3): 

if "%CONFIRM%"=="1" goto RUN_SEARCH
if "%CONFIRM%"=="2" goto START_SEARCH
if "%CONFIRM%"=="3" goto MAIN_MENU
goto CONFIRM_SETTINGS

:RUN_SEARCH
cls
echo ======================================================
echo                 正在執行搜尋...
echo ======================================================
echo.
echo  搜尋地區: %REGIONS%
echo  目標網域: %TARGET_DOMAIN%
echo  使用 API: %USE_API%
echo.
echo  開始執行爬蟲程式...
echo  注意：
if "%USE_API%"=="SERP" (
    echo  1. 此程式使用SERP API獲取Google搜尋結果
    echo  2. 免費方案每月可查詢100次，請謹慎使用
) else if "%USE_API%"=="SCRAPINGDOG" (
    echo  1. 此程式使用Scrapingdog API獲取Google搜尋結果
    echo  2. 提供免費試用方案，請謹慎使用
)
echo  3. 請稍候，程式正在執行中...
echo.
echo ======================================================
echo.

if "%USE_API%"=="SERP" (
    python serp_api_crawler.py --regions %REGIONS% --domain %TARGET_DOMAIN%
) else if "%USE_API%"=="SCRAPINGDOG" (
    python scrapingdog_crawler.py --regions %REGIONS% --domain %TARGET_DOMAIN%
)

echo.
echo ======================================================
echo.
echo  搜尋完成！
echo  結果已保存到 results 資料夾中
echo.
echo  [1] 返回主選單
echo  [2] 退出程式
echo.
echo ======================================================
echo.
set /p AFTER_RUN=請選擇 (1-2):

if "%AFTER_RUN%"=="1" goto MAIN_MENU
goto EXIT

:RUN_APIFY
cls
echo ======================================================
echo              正在執行 Apify 爬蟲...
echo ======================================================
echo.
echo  開始執行 Apify 爬蟲程式...
echo  注意：
echo  1. 此程式使用 Apify Google Search Scraper
echo  2. 需要已設定 APIFY_API_TOKEN 環境變數
echo  3. 請稍候，程式正在執行中...
echo.
echo ======================================================
echo.

python apify_crawler.py

echo.
echo ======================================================
echo.
echo  搜尋完成！
echo  結果已保存到 results 資料夾中
echo.
echo  [1] 返回主選單
echo  [2] 退出程式
echo.
echo ======================================================
echo.
set /p AFTER_RUN=請選擇 (1-2):

if "%AFTER_RUN%"=="1" goto MAIN_MENU
goto EXIT

:SHOW_HELP
cls
echo ======================================================
echo                    使用說明
echo ======================================================
echo.
echo  SERP 排名追蹤器使用說明:
echo.
echo  1. 本程式用於追蹤網站在Google搜尋結果中的排名
echo  2. 支援三種 API 服務:
echo     - SERP API: 穩定可靠，免費方案每月100次查詢
echo     - Scrapingdog API: 提供免費試用方案
echo     - Apify API: 適合大量爬取需求
echo.
echo  搜尋地區說明 (SERP API):
echo   - 美國(US): 使用英文搜尋，google.com
echo   - 台灣(TW): 使用繁體中文搜尋，google.com.tw
echo   - 香港(HK): 使用繁體中文搜尋，google.com.hk
echo.
echo  關鍵字檔案:
echo   - 預設使用 keywords.csv 檔案
echo   - 第一欄必須是 "keyword"，每行一個關鍵字
echo.
echo  結果檔案:
echo   - 結果保存在 results 資料夾中
echo   - CSV檔案包含關鍵字、排名、網址等資訊
echo.
echo ======================================================
echo.
echo  按任意鍵返回主選單...
pause > nul
goto MAIN_MENU

:SET_SERPAPI_KEY
cls
echo ======================================================
echo               設定 SERP API 金鑰
echo ======================================================
echo.
echo  SERP API 金鑰用於向 serpapi.com 服務發送請求
echo  免費方案每月可查詢100次
echo.
echo  請輸入您的 SERP API 金鑰:
echo  (可從 https://serpapi.com 獲取)
echo.
echo ======================================================
echo.
set /p NEW_API_KEY=SERP API 金鑰:

if "%NEW_API_KEY%"=="" (
    echo.
    echo 未輸入金鑰，保持原有設定
    timeout /t 2 /nobreak > nul
    goto MAIN_MENU
)

echo 正在更新 config.py 中的 API 金鑰...
powershell -Command "(Get-Content config.py) -replace '^SERPAPI_KEY = .*$', 'SERPAPI_KEY = \"%NEW_API_KEY%\"' | Set-Content config.py"

echo.
echo API 金鑰已更新！
timeout /t 2 /nobreak > nul
goto MAIN_MENU

:SET_SCRAPINGDOG_KEY
cls
echo ======================================================
echo            設定 Scrapingdog API 金鑰
echo ======================================================
echo.
echo  Scrapingdog API 金鑰用於向 scrapingdog.com 服務發送請求
echo  提供免費試用方案
echo.
echo  請輸入您的 Scrapingdog API 金鑰:
echo  (可從 https://www.scrapingdog.com 獲取)
echo.
echo ======================================================
echo.
set /p NEW_SCRAPINGDOG_KEY=Scrapingdog API 金鑰:

if "%NEW_SCRAPINGDOG_KEY%"=="" (
    echo.
    echo 未輸入金鑰，保持原有設定
    timeout /t 2 /nobreak > nul
    goto MAIN_MENU
)

echo 正在更新 config.py 中的 API 金鑰...
powershell -Command "(Get-Content config.py) -replace '^SCRAPINGDOG_API_KEY = .*$', 'SCRAPINGDOG_API_KEY = \"%NEW_SCRAPINGDOG_KEY%\"' | Set-Content config.py"

echo.
echo API 金鑰已更新！
timeout /t 2 /nobreak > nul
goto MAIN_MENU

:SET_APIFY_KEY
cls
echo ======================================================
echo               設定 Apify API 金鑰
echo ======================================================
echo.
echo  Apify API 金鑰用於使用 Apify 爬蟲服務
echo  需要設定為系統環境變數 APIFY_API_TOKEN
echo.
echo  請輸入您的 Apify API 金鑰:
echo  (可從 https://apify.com 獲取)
echo.
echo ======================================================
echo.
set /p NEW_APIFY_KEY=Apify API 金鑰:

if "%NEW_APIFY_KEY%"=="" (
    echo.
    echo 未輸入金鑰，保持原有設定
    timeout /t 2 /nobreak > nul
    goto MAIN_MENU
)

echo 正在設定環境變數...
setx APIFY_API_TOKEN "%NEW_APIFY_KEY%"

echo.
echo Apify API 金鑰已設定！
echo 注意: 請重新啟動此程式以套用新的環境變數
timeout /t 3 /nobreak > nul
goto MAIN_MENU

:EXIT
cls
echo ======================================================
echo              感謝使用 SERP 排名追蹤器
echo ======================================================
echo.
echo  程式已退出，再見！
echo.
timeout /t 2 /nobreak > nul
exit 