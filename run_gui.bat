@echo off
chcp 65001 > nul
title SERP 排名追蹤器 - GUI 版本

echo 正在啟動 SERP 排名追蹤器 GUI...
python gui_app.py

if errorlevel 1 (
    echo.
    echo 啟動失敗！請確認：
    echo 1. Python 已正確安裝
    echo 2. 所有必要的套件已安裝
    echo.
    pause
)
