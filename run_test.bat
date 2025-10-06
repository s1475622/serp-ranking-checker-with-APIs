@echo off
echo 開始執行測試搜尋...
python tests\test_apify_crawler.py
echo.
echo 分析搜尋結果...
python rank_analyzer.py
pause 