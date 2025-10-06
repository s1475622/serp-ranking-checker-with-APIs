import pandas as pd
import glob

def analyze_and_output():
    """分析搜尋結果並輸出簡潔格式"""
    # 取得最新的結果檔案
    results_files = glob.glob('results/apify_results_*.csv')
    if not results_files:
        print("找不到搜尋結果檔案！")
        return
    
    latest_file = max(results_files)
    print(f"分析檔案: {latest_file}")
    print("=" * 80)
    
    # 讀取CSV檔案
    df = pd.read_csv(latest_file)
    
    # 分析目標網域
    target_domain = 'mall.sfworldwide.com'
    domain_results = df[df['url'].str.contains(target_domain, na=False)]
    
    if len(domain_results) > 0:
        print(f"找到 {target_domain} 的排名:")
        print("-" * 50)
        for _, row in domain_results.iterrows():
            print(f"{row['keyword']} - 排名{row['position']} - {row['url']}")
    else:
        print(f"在搜尋結果中未找到 {target_domain}")
        print(f"搜尋的關鍵字: {', '.join(df['keyword'].unique())}")
        print(f"每個關鍵字取得約 {len(df)} 筆結果")
        
        # 顯示摘要統計
        print("\n搜尋結果摘要:")
        print("-" * 50)
        for keyword in df['keyword'].unique():
            keyword_results = df[df['keyword'] == keyword]
            print(f"{keyword}: {len(keyword_results)} 筆結果")
            
            # 顯示前3名
            top3 = keyword_results.head(3)
            for _, row in top3.iterrows():
                url = row['url']
                if len(url) > 60:
                    url = url[:60] + "..."
                print(f"  排名{row['position']}: {url}")
            print()

if __name__ == "__main__":
    analyze_and_output() 