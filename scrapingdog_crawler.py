import os
import time
import pandas as pd
import argparse
import traceback
import sys
import requests
from datetime import datetime
import config

class ScrapingdogCrawler:
    def __init__(self, api_key=None):
        print("[INFO] 初始化Scrapingdog API爬蟲...")
        # 如果未提供API密鑰，嘗試從環境變數或配置文件獲取
        self.api_key = api_key or os.environ.get("SCRAPINGDOG_API_KEY") or config.SCRAPINGDOG_API_KEY

        if not self.api_key:
            print("[警告] 未設置SCRAPINGDOG_API_KEY！請在config.py中設置或使用--api_key參數提供")
            print("您可以在 https://www.scrapingdog.com 註冊獲取API密鑰")
            print("[提示] Scrapingdog提供免費試用方案")

    def search_keyword(self, keyword, domain, region='US', max_results=100):
        """使用Scrapingdog API搜索關鍵字並找到網域排名（支援分頁以獲取100個結果）"""
        try:
            region_config = config.ALL_REGIONS[region]
            language = region_config["lang"]
            country = region_config["country"].lower()

            print(f"\n[INFO] 搜索關鍵字 '{keyword}' （地區: {region}, 語言: {language}, 國家: {country}）...")

            all_organic_results = []
            current_page = 0
            page = 1

            # 由於 Google 限制，需要分頁獲取結果
            # 每次請求約返回 10 個結果，需要多次請求來獲取 100 個
            # 優化：找到目標網域後立即停止，節省 API 配額
            found_target = False

            while len(all_organic_results) < max_results and not found_target:
                params = {
                    "api_key": self.api_key,
                    "query": keyword,
                    "country": country,
                    "results": 10,  # 每頁請求 10 個結果
                    "page": current_page  # 頁碼（從0開始）
                }

                # 添加語言參數
                if language == "en":
                    params["language"] = "en"
                elif language == "zh-TW":
                    params["language"] = "zh-TW"

                print(f"[INFO] 發送API請求（第 {page} 頁，頁碼: {current_page}）...")
                response = requests.get("https://api.scrapingdog.com/google", params=params, timeout=30)

                if response.status_code != 200:
                    print(f"[錯誤] API請求失敗：HTTP {response.status_code}")
                    print(f"回應內容: {response.text}")

                    # 檢查是否為API配額限制錯誤
                    if response.status_code == 429 or "rate limit" in response.text.lower() or "quota" in response.text.lower():
                        print(f"[錯誤] API配額已達限制")
                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'position': -2,
                            'url': '',
                            'region': region,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'error': 'API配額已達限制'
                        }
                    else:
                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'position': -2,
                            'url': '',
                            'region': region,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'error': f'API請求失敗：HTTP {response.status_code}'
                        }

                results = response.json()

                # 檢查API回應中是否包含錯誤訊息
                if "error" in results:
                    error_msg = results["error"]
                    print(f"[錯誤] API回應錯誤: {error_msg}")

                    # 檢查是否為配額限制
                    if "rate limit" in error_msg.lower() or "quota" in error_msg.lower() or "credits" in error_msg.lower():
                        print(f"[錯誤] API配額已達限制")
                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'position': -2,
                            'url': '',
                            'region': region,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'error': 'API配額已達限制'
                        }
                    else:
                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'position': -2,
                            'url': '',
                            'region': region,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'error': error_msg
                        }

                # 檢索本頁的有機搜尋結果
                organic_results = results.get("organic_results", [])

                if not organic_results:
                    print(f"[INFO] 第 {page} 頁沒有更多結果")
                    break

                # 檢查本頁是否有目標網域（提前終止優化）
                for idx, result in enumerate(organic_results):
                    # 計算全局排名位置
                    global_position = len(all_organic_results) + 1
                    result['global_position'] = global_position

                    all_organic_results.append(result)

                    # 立即檢查是否為目標網域
                    link = result.get("link", "")
                    if domain in link:
                        position = global_position
                        title = result.get("title", "")
                        snippet = result.get("snippet", "")

                        print(f"[INFO] 第 {page} 頁收到 {len(organic_results)} 個結果")
                        print(f"[成功] 找到目標網站！排名: {position}")
                        print(f"[優化] 提前終止搜尋，節省了 {10 - page} 頁的 API 請求")
                        print(f"標題: {title}")
                        print(f"網址: {link}")

                        found_target = True

                        return {
                            'keyword': keyword,
                            'domain': domain,
                            'position': position,
                            'url': link,
                            'title': title,
                            'snippet': snippet,
                            'region': region,
                            'date': datetime.now().strftime('%Y-%m-%d')
                        }

                print(f"[INFO] 第 {page} 頁收到 {len(organic_results)} 個結果，總計: {len(all_organic_results)}")

                # 檢查是否還有下一頁
                # 只有在達到最大結果數量時才停止
                if len(all_organic_results) >= max_results:
                    print(f"[INFO] 已到達最大結果數量")
                    break

                # 準備下一頁
                current_page += 1
                page += 1

                # 短暫延遲避免請求過快
                time.sleep(1)

            print(f"[INFO] 總共搜尋了 {page} 頁，收到 {len(all_organic_results)} 個有機搜尋結果")
            print(f"[INFO] 在前{len(all_organic_results)}個結果中未找到目標網站 {domain}")
            return {
                'keyword': keyword,
                'domain': domain,
                'position': -1,  # 未找到
                'url': '',
                'region': region,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'error': f"目標網站未在前{len(all_organic_results)}個結果中"
            }

        except Exception as e:
            print(f"[錯誤] 搜索過程失敗 - {str(e)}")
            traceback.print_exc()
            return {
                'keyword': keyword,
                'domain': domain,
                'position': -2,  # 錯誤代碼
                'url': '',
                'region': region,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'error': str(e)
            }

    def process_keywords_file(self, filename='keywords.csv', domain=None):
        """處理關鍵字文件"""
        try:
            if not self.api_key:
                print("[錯誤] 未設置API密鑰，無法繼續執行")
                return

            print(f"\n[INFO] 讀取關鍵字文件: {filename}")

            # 嘗試多種編碼讀取文件
            encodings = ['utf-8', 'big5', 'cp950', 'gb18030', 'utf-8-sig']
            df = None

            for encoding in encodings:
                try:
                    df = pd.read_csv(filename, encoding=encoding)
                    print(f"[INFO] 成功使用 {encoding} 編碼讀取文件")
                    break
                except UnicodeDecodeError:
                    continue

            if df is None:
                print("[錯誤] 無法讀取關鍵字文件，請檢查文件編碼")
                return

            print(f"[INFO] 找到 {len(df)} 個關鍵字等待處理")
            results = []
            api_limit_reached = False

            os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)

            if domain:
                print(f"[INFO] 命令行指定目標網域: {domain}")

            for index, row in df.iterrows():
                keyword = row['keyword']
                target_domain = domain if domain else row.get('domain', config.TARGET_DOMAIN)

                for region in config.SELECTED_REGIONS:
                    result = self.search_keyword(keyword, target_domain, region)
                    results.append(result)

                    # 檢查是否達到API配額限制
                    if result.get('position') == -2 and result.get('error') and 'API配額已達限制' in result.get('error'):
                        print("\n" + "="*60)
                        print("[警告] API配額已達限制，停止爬取並保存已完成的結果")
                        print("="*60 + "\n")
                        api_limit_reached = True
                        break

                    # 降低API請求頻率，防止超出限額
                    if index < len(df) - 1 or region != config.SELECTED_REGIONS[-1]:
                        delay = config.SCRAPINGDOG_DELAY_BETWEEN_REQUESTS
                        print(f"[INFO] 等待 {delay} 秒後繼續下一個搜索...")
                        time.sleep(delay)

                # 如果達到配額限制，跳出外層循環
                if api_limit_reached:
                    # 標記剩餘未爬取的關鍵字
                    remaining_keywords = []
                    for remaining_index in range(index, len(df)):
                        remaining_row = df.iloc[remaining_index]
                        remaining_keyword = remaining_row['keyword']
                        remaining_domain = domain if domain else remaining_row.get('domain', config.TARGET_DOMAIN)

                        # 檢查這個關鍵字是否已經有部分區域被爬取
                        for region in config.SELECTED_REGIONS:
                            # 檢查是否已在results中
                            already_crawled = any(
                                r['keyword'] == remaining_keyword and r['region'] == region
                                for r in results
                            )

                            if not already_crawled:
                                remaining_keywords.append({
                                    'keyword': remaining_keyword,
                                    'domain': remaining_domain,
                                    'position': -3,  # 新的狀態碼：未爬取
                                    'url': '',
                                    'region': region,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'error': '未爬取（API配額已達限制）'
                                })

                    results.extend(remaining_keywords)
                    break

            results_df = pd.DataFrame(results)

            output_file = os.path.join(
                config.OUTPUT_FOLDER,
                f'scrapingdog_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{config.OUTPUT_FILE_FORMAT}'
            )

            if config.OUTPUT_FILE_FORMAT == 'csv':
                results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
            else:
                results_df.to_excel(output_file, index=False)

            # 根據API限制情況顯示不同的完成訊息
            if api_limit_reached:
                print(f"\n[警告] API配額已達限制，部分結果已保存至: {output_file}")
            else:
                print(f"\n[成功] 搜索完成！結果已保存至: {output_file}")

            print(f"[統計] 總關鍵字數: {len(df)}")

            # 計算排名統計
            ranked_results = results_df[results_df['position'] > 0]
            not_found = results_df[results_df['position'] == -1]
            errors = results_df[results_df['position'] == -2]
            not_crawled = results_df[results_df['position'] == -3]

            print(f"[統計] 有排名的關鍵字: {len(ranked_results)}")
            print(f"[統計] 未找到排名的關鍵字: {len(not_found)}")
            print(f"[統計] 發生錯誤的關鍵字: {len(errors)}")
            print(f"[統計] 未爬取的關鍵字: {len(not_crawled)}")

            # 計算排名分布
            if len(ranked_results) > 0:
                top10 = ranked_results[ranked_results['position'] <= 10]
                top30 = ranked_results[(ranked_results['position'] > 10) & (ranked_results['position'] <= 30)]
                top100 = ranked_results[(ranked_results['position'] > 30) & (ranked_results['position'] <= 100)]

                print(f"[統計] 排名前10位的關鍵字: {len(top10)}")
                print(f"[統計] 排名11-30位的關鍵字: {len(top30)}")
                print(f"[統計] 排名31-100位的關鍵字: {len(top100)}")

            return results_df

        except Exception as e:
            print(f"[錯誤] 處理關鍵字文件失敗 - {str(e)}")
            traceback.print_exc()
            sys.exit(1)

def main():
    try:
        print("[INFO] 啟動程序...")
        parser = argparse.ArgumentParser(description='Scrapingdog API排名追蹤器')
        parser.add_argument('--regions', nargs='+', choices=['US', 'TW', 'HK'],
                          default=['US'], help='搜索區域')
        parser.add_argument('--domain', type=str, help='目標網域')
        parser.add_argument('--keywords_file', type=str, default='keywords.csv',
                          help='關鍵字文件路徑')
        parser.add_argument('--api_key', type=str, help='Scrapingdog API 密鑰')

        print("[INFO] 解析命令行參數...")
        args = parser.parse_args()
        print(f"[INFO] 搜索區域: {args.regions}")
        print(f"[INFO] 目標網域: {args.domain}")
        print(f"[INFO] 關鍵字文件: {args.keywords_file}")

        config.SELECTED_REGIONS = args.regions

        print("[INFO] 初始化Scrapingdog API爬蟲...")
        crawler = ScrapingdogCrawler(api_key=args.api_key)
        try:
            print("[INFO] 開始處理關鍵字...")
            crawler.process_keywords_file(args.keywords_file, args.domain)
        except Exception as e:
            print(f"[錯誤] 關鍵字處理失敗: {str(e)}")
            print("[錯誤] 詳細錯誤信息:")
            traceback.print_exc()
    except Exception as e:
        print(f"[錯誤] 程序執行失敗: {str(e)}")
        print("[錯誤] 詳細錯誤信息:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
