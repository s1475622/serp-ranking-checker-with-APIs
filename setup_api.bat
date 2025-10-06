@echo off
chcp 65001 > nul
title SERP API Crawler Setup and Execution
echo ======================================================
echo          SERP API Crawler Setup and Execution
echo ======================================================
echo.
echo 開始安裝必要套件...
"C:\Users\user\AppData\Local\Programs\Python\Python313\python.exe" -m pip install requests pandas
echo.
echo 套件安裝完成！
echo.
echo 請輸入您的SERP API密鑰 (從https://serpapi.com獲取):
set /p API_KEY=SERP API密鑰: 
echo.
echo 開始執行爬蟲程式...
echo 注意：
echo 1. 此程式使用SERP API獲取Google搜尋結果，無需啟動瀏覽器
echo 2. 免費方案每月可查詢100次，請謹慎使用
echo 3. 搜尋結果會使用指定的語言和地區設定（例如：美國/英文）
echo 4. 結果將保存到results資料夾中
echo.
"C:\Users\user\AppData\Local\Programs\Python\Python313\python.exe" serp_api_crawler.py --regions US --domain agiledisplaysolutions.com --api_key %API_KEY%
echo.
echo 程式執行完畢，請查看 results 資料夾中的結果檔案！
echo 按任意鍵結束...
pause > nul 