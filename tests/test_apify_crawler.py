from apify_client import ApifyClient
import pandas as pd
from datetime import datetime
import os
import time
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Apify設定
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN', '')
if not APIFY_API_TOKEN:
    raise ValueError("請在 .env 檔案中設定 APIFY_API_TOKEN")
ACTOR_ID = "apify/google-search-scraper"  # 使用官方的Google搜尋爬蟲

# 目標網域
TARGET_DOMAIN = "mall.sfworldwide.com"

def read_keywords(file_path):
    """讀取關鍵字檔案"""
    df = pd.read_csv(file_path)
    return df['keyword'].tolist()

def search_google(client, keywords):
    """使用Apify執行Google搜尋"""
    all_results = []
    
    for keyword in keywords:
        print(f"\n正在搜尋關鍵字: {keyword}")
        
        # 使用官方Google搜尋爬蟲的輸入格式
        run_input = {
            "queries": keyword,  # 搜尋查詢字串
            "resultsPerPage": 100,  # 每頁結果數
            "maxPagesPerQuery": 10,  # 每個查詢的最大頁數
            "countryCode": "tw",  # 國家代碼
            "languageCode": "zh-TW",  # 語言代碼
            "customDataFunction": "",
            "includeUnfilteredResults": False,
            "saveHtml": False,
            "saveHtmlToKeyValueStore": False
        }

        print("正在啟動 Apify Actor...")
        try:
            run = client.actor(ACTOR_ID).call(run_input=run_input)
            
            # 取得結果
            print("正在取得搜尋結果...")
            keyword_results = []
            
            for item in client.dataset(run["defaultDatasetId"]).iterate_items():
                print(f"處理項目: {item.keys()}")  # 查看可用的欄位
                
                # 處理搜尋結果
                if "searchQuery" in item and "organicResults" in item:
                    organic_results = item.get("organicResults", [])
                    for i, result in enumerate(organic_results):
                        if len(keyword_results) < 100:  # 限制在100個結果內
                            keyword_results.append({
                                "keyword": keyword,
                                "title": result.get("title", ""),
                                "url": result.get("url", ""),
                                "position": i + 1,
                                "description": result.get("description", ""),
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                
                # 如果沒有organicResults，嘗試其他格式
                elif "results" in item and isinstance(item["results"], list):
                    for result in item["results"]:
                        if len(keyword_results) < 100:
                            keyword_results.append({
                                "keyword": keyword,
                                "title": result.get("title", ""),
                                "url": result.get("url", ""),
                                "position": result.get("position", len(keyword_results) + 1),
                                "description": result.get("description", ""),
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
            
            print(f"關鍵字 '{keyword}' 實際取得 {len(keyword_results)} 筆結果")
            all_results.extend(keyword_results)
            
        except Exception as e:
            print(f"搜尋關鍵字 '{keyword}' 時發生錯誤: {str(e)}")
            continue
        
        # 短暫延遲避免過於頻繁請求
        time.sleep(3)
    
    return all_results

def save_results(results):
    """儲存搜尋結果"""
    if not results:
        print("沒有搜尋結果可儲存")
        return
    
    # 建立results資料夾（如果不存在）
    os.makedirs("results", exist_ok=True)
    
    # 建立DataFrame
    df = pd.DataFrame(results)
    
    # 儲存完整結果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"results/apify_results_{timestamp}.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"搜尋結果已儲存至：{filename}")
    
    return filename

def main():
    print("開始執行Google搜尋爬蟲...")
    
    # 讀取關鍵字
    keywords = read_keywords("test_keywords.csv")
    print(f"讀取到 {len(keywords)} 個關鍵字: {keywords}")
    
    # 初始化Apify客戶端
    client = ApifyClient(APIFY_API_TOKEN)
    
    # 執行搜尋（先測試第一個關鍵字）
    print("開始執行搜尋...")
    results = search_google(client, keywords)
    
    # 儲存結果
    print("儲存搜尋結果...")
    filename = save_results(results)
    
    if results:
        print(f"總共取得 {len(results)} 筆搜尋結果")
    
    print("完成！")

if __name__ == "__main__":
    main() 