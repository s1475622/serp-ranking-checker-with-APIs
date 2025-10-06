import pandas as pd
import glob
import os
from datetime import datetime

def analyze_rankings(results_file, target_domain='mall.sfworldwide.com'):
    """分析特定網域的搜尋排名"""
    # 讀取CSV檔案
    df = pd.read_csv(results_file)
    
    # 篩選出包含目標網域的資料
    domain_results = []
    
    # 遍歷每個關鍵字的搜尋結果
    for _, row in df.iterrows():
        keyword = row['keyword']
        position = row['position']
        url = row['url'] if pd.notna(row['url']) else ''
        
        # 只記錄目標網域的結果
        if target_domain in str(url):
            domain_results.append({
                'keyword': keyword,
                'position': position,
                'url': url
            })
    
    return domain_results

def main():
    # 取得最新的結果檔案
    results_files = glob.glob('results/apify_results_*.csv')
    if not results_files:
        print("找不到搜尋結果檔案！")
        return
    
    latest_file = max(results_files)
    
    # 分析排名
    rankings = analyze_rankings(latest_file)
    
    # 輸出結果
    print("\n搜尋結果分析")
    print("=" * 50)
    print("關鍵字 - 排名 - URL")
    print("-" * 50)
    
    for result in rankings:
        print(f"{result['keyword']} - {result['position']} - {result['url']}")

if __name__ == "__main__":
    main() 