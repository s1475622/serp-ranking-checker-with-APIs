import os
import csv
from datetime import datetime
from apify_client import ApifyClient
from dotenv import load_dotenv
from urllib.parse import urlparse

# 載入環境變數
load_dotenv()

class ApifySearchCrawler:
    def __init__(self):
        # 從環境變數獲取 Apify API token
        self.client = ApifyClient(os.getenv('APIFY_API_TOKEN'))
        
    def search(self, keywords, target_domain='mall.sfworldwide.com', country='tw', language='zh-TW', max_position=100):
        """
        使用 Apify 的 Google Search Results Scraper 執行搜尋
        找到目標網域後立即停止，節省 API 資源

        Args:
            keywords (list): 要搜尋的關鍵字列表
            target_domain (str): 要追蹤的目標網域
            country (str): 目標國家代碼 (預設為 'tw' 台灣)
            language (str): 搜尋語言代碼 (預設為 'zh-TW' 繁體中文)
            max_position (int): 最大搜尋排名位置 (預設 100)
        """
        domain_rankings = []  # 只記錄目標網域的排名

        for keyword in keywords:
            if keyword.strip() and not keyword.startswith('keyword'):  # 跳過標題行和空行
                print(f"\n正在搜尋關鍵字: {keyword}")

                # 設定 Google host 根據國家
                google_hosts = {
                    'tw': 'google.com.tw',
                    'hk': 'google.com.hk',
                    'us': 'google.com'
                }

                try:
                    # 逐頁搜尋，找到目標後立即停止
                    found_target = False
                    total_results_count = 0
                    max_pages = max_position // 10  # 計算需要的頁數

                    for page in range(1, max_pages + 1):
                        if found_target:
                            print(f"   ✓ 已找到目標，跳過剩餘 {max_pages - page + 1} 頁，節省 API 資源")
                            break

                        print(f"   正在搜尋第 {page} 頁...")

                        # 每次只請求 1 頁
                        run_input = {
                            "queries": keyword.strip(),
                            "countryCode": country,
                            "languageCode": language,
                            "maxPagesPerQuery": 1,  # 每次只抓 1 頁
                            "resultsPerPage": 10,
                            "mobileResults": False,
                            "saveHtml": False,
                            "includeUnfilteredResults": False,
                            "googleHost": google_hosts.get(country, "google.com"),
                            "startPage": page  # 指定起始頁碼
                        }

                        # 執行 Apify actor
                        run = self.client.actor("apify/google-search-scraper").call(run_input=run_input)

                        # 獲取結果
                        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                            if "organicResults" in item:
                                organic_count = len(item["organicResults"])
                                total_results_count += organic_count

                                for result in item["organicResults"]:
                                    # 取得網址的網域
                                    parsed_url = urlparse(result.get("url", ""))
                                    domain = parsed_url.netloc.lower()
                                    position = result.get("position", 0)

                                    # 如果超過100名就跳過
                                    if position > max_position:
                                        continue

                                    # 檢查是否為目標網域
                                    is_target = target_domain.lower() in domain
                                    if is_target and not found_target:
                                        found_target = True
                                        print(f"   ✓ 在第 {position} 名找到目標網域！")
                                        # 只記錄目標網域的排名
                                        domain_rankings.append({
                                            "keyword": keyword,
                                            "ranking": position,
                                            "url": result.get("url", "")
                                        })
                                        break  # 找到後立即跳出內層迴圈

                                if found_target:
                                    break  # 找到後跳出 dataset 迭代

                    print(f"   總共搜尋了 {total_results_count} 個結果")

                    if not found_target:
                        print(f"   ✗ 在前 {total_results_count} 名中未找到目標網域")
                        # 記錄未找到的情況
                        domain_rankings.append({
                            "keyword": keyword,
                            "ranking": "未找到",
                            "url": ""
                        })

                except Exception as e:
                    error_msg = str(e)
                    print(f"[錯誤] 搜尋關鍵字 '{keyword}' 時發生錯誤: {error_msg}")
                    # 記錄錯誤情況
                    domain_rankings.append({
                        "keyword": keyword,
                        "ranking": "錯誤",
                        "url": ""
                    })
                    continue

        return domain_rankings

    def save_results(self, domain_rankings, output_dir="results"):
        """
        將目標網域排名保存到 CSV 文件
        """
        if not domain_rankings:
            print("沒有結果可以保存")
            return

        # 確保輸出目錄存在
        os.makedirs(output_dir, exist_ok=True)

        # 生成時間戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 只保存目標網域排名（keyword, ranking, url）
        rankings_file = os.path.join(output_dir, f"domain_rankings_{timestamp}.csv")
        with open(rankings_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["keyword", "ranking", "url"])
            writer.writeheader()
            writer.writerows(domain_rankings)
        print(f"\n目標網域排名已保存到: {rankings_file}")
        return rankings_file

def main():
    # 嘗試不同的編碼讀取關鍵字
    encodings = ['utf-8-sig', 'utf-8', 'big5', 'cp950', 'gb18030']
    keywords = []

    # 使用測試檔案
    keywords_file = 'keywords_test.csv'

    for encoding in encodings:
        try:
            keywords = []  # 重置列表
            with open(keywords_file, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'keyword' in row and row['keyword'].strip():
                        keywords.append(row['keyword'])
                if keywords:  # 確保有讀到資料
                    print(f"成功使用 {encoding} 編碼讀取檔案")
                    break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"使用 {encoding} 讀取時發生錯誤: {str(e)}")
            continue
    
    if not keywords:
        print("無法讀取關鍵字檔案，請確認檔案編碼")
        return
    
    print(f"\n總共要搜尋 {len(keywords)} 個關鍵字")
    
    # 初始化爬蟲
    crawler = ApifySearchCrawler()

    # 執行搜尋
    domain_rankings = crawler.search(keywords)

    # 保存結果
    crawler.save_results(domain_rankings)

    # 顯示摘要報告
    print("\n搜尋完成！摘要報告：")
    ranked_keywords = sum(1 for r in domain_rankings if isinstance(r["ranking"], int))
    print(f"- 目標網域在 {ranked_keywords}/{len(keywords)} 個關鍵字中有排名")
    if ranked_keywords > 0:
        valid_rankings = [r["ranking"] for r in domain_rankings if isinstance(r["ranking"], int)]
        avg_position = sum(valid_rankings) / len(valid_rankings)
        print(f"- 平均排名位置: {avg_position:.1f}")
        best_ranking = min((r["ranking"], r["keyword"]) for r in domain_rankings if isinstance(r["ranking"], int))
        print(f"- 最佳排名: 第 {best_ranking[0]} 名 (關鍵字: {best_ranking[1]})")

if __name__ == "__main__":
    main() 