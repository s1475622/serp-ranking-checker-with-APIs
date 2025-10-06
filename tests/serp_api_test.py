import requests
import pandas as pd
import os
import time
from datetime import datetime
import config

# SerpAPI 設定
API_KEY = config.SERPAPI_KEY  # 從配置文件讀取API金鑰
RESULTS_PER_PAGE = 100

def search_keyword(keyword, domain, region='us'):
    """使用SerpAPI搜索關鍵字並找到網域排名"""
    print(f"搜尋關鍵字: {keyword} (地區: {region})")
    
    params = {
        "engine": "google",
        "q": keyword,
        "api_key": API_KEY,
        "num": RESULTS_PER_PAGE,
        "gl": region.lower(),  # 地區
        "hl": "en"  # 語言
    }
    
    try:
        print("發送API請求...")
        response = requests.get("https://serpapi.com/search", params=params)
        
        if response.status_code != 200:
            print(f"API請求失敗：HTTP {response.status_code}")
            print(f"回應內容: {response.text}")
            return {
                'keyword': keyword,
                'domain': domain,
                'position': -2,  # 錯誤代碼
                'url': '',
                'error': f"API錯誤 {response.status_code}"
            }
        
        results = response.json()
        
        # 檢索所有有機搜尋結果
        organic_results = results.get("organic_results", [])
        print(f"收到 {len(organic_results)} 個有機搜尋結果")
        
        # 尋找目標網域
        for position, result in enumerate(organic_results, 1):
            link = result.get("link", "")
            if domain in link:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                print(f"找到目標網站！排名: {position}")
                print(f"標題: {title}")
                print(f"網址: {link}")
                
                return {
                    'keyword': keyword,
                    'domain': domain,
                    'position': position,
                    'url': link,
                    'title': title,
                    'snippet': snippet,
                    'date': datetime.now().strftime('%Y-%m-%d')
                }
        
        print(f"在前{RESULTS_PER_PAGE}個結果中未找到目標網站 {domain}")
        return {
            'keyword': keyword,
            'domain': domain,
            'position': -1,  # 未找到
            'url': '',
            'error': "目標網站未在搜尋結果中"
        }
        
    except Exception as e:
        print(f"搜索過程失敗 - {str(e)}")
        return {
            'keyword': keyword,
            'domain': domain,
            'position': -2,  # 錯誤代碼
            'url': '',
            'error': str(e)
        }

def process_keywords(keyword_file="keywords.csv", domain="agiledisplaysolutions.com", regions=["us"]):
    """處理關鍵字文件"""
    try:
        # 顯示API金鑰資訊（僅顯示前10位和後10位）
        key_length = len(API_KEY)
        print(f"使用API金鑰: {API_KEY[:10]}...{API_KEY[key_length-10:]} (總長度: {key_length})")
        
        # 讀取關鍵字文件
        df = pd.read_csv(keyword_file)
        print(f"找到 {len(df)} 個關鍵字待處理")
        results = []
        
        # 確保輸出目錄存在
        os.makedirs("results", exist_ok=True)
        
        # 處理每個關鍵字
        for index, row in df.iterrows():
            keyword = row['keyword']
            
            for region in regions:
                print(f"\n[{index + 1}/{len(df)}] 處理關鍵字: {keyword} (區域: {region})")
                result = search_keyword(keyword, domain, region)
                results.append(result)
                
                # 避免過快發送請求
                if index < len(df) - 1 or region != regions[-1]:
                    delay = 5
                    print(f"等待 {delay} 秒後繼續...")
                    time.sleep(delay)
        
        # 保存結果
        results_df = pd.DataFrame(results)
        output_file = f"results/serp_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results_df.to_csv(output_file, index=False)
        print(f"\n搜索完成！結果已保存至: {output_file}")
        
        # 統計結果
        ranked_results = results_df[results_df['position'] > 0]
        not_found = results_df[results_df['position'] == -1]
        errors = results_df[results_df['position'] == -2]
        
        print(f"總計: {len(results_df)} 個查詢")
        print(f"有排名的關鍵字: {len(ranked_results)}")
        print(f"未找到排名的關鍵字: {len(not_found)}")
        print(f"發生錯誤的關鍵字: {len(errors)}")
        
        # 排名分布
        if len(ranked_results) > 0:
            top10 = ranked_results[ranked_results['position'] <= 10]
            top30 = ranked_results[(ranked_results['position'] > 10) & (ranked_results['position'] <= 30)]
            top100 = ranked_results[(ranked_results['position'] > 30) & (ranked_results['position'] <= 100)]
            
            print(f"排名前10位的關鍵字: {len(top10)}")
            print(f"排名11-30位的關鍵字: {len(top30)}")
            print(f"排名31-100位的關鍵字: {len(top100)}")
    
    except Exception as e:
        print(f"處理關鍵字時出錯: {str(e)}")

if __name__ == "__main__":
    print("開始執行SERP API搜尋測試...")
    process_keywords(regions=["us"])
    print("\n測試完成！") 