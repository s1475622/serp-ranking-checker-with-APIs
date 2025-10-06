"""
測試 .env 檔案更新功能
"""
import os
import sys

# 將專案根目錄加入路徑
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_env_reading():
    """測試從 .env 讀取 API keys"""
    print("=" * 60)
    print("測試從 .env 讀取 API Keys")
    print("=" * 60)

    # 載入環境變數
    from dotenv import load_dotenv
    load_dotenv()

    # 測試讀取
    serpapi_keys = os.getenv('SERPAPI_KEYS', '')
    scrapingdog_key = os.getenv('SCRAPINGDOG_API_KEY', '')
    apify_token = os.getenv('APIFY_API_TOKEN', '')

    print(f"\n[OK] SERPAPI_KEYS: {serpapi_keys[:50]}..." if serpapi_keys else "[FAIL] SERPAPI_KEYS not set")
    print(f"[OK] SCRAPINGDOG_API_KEY: {scrapingdog_key[:20]}..." if scrapingdog_key else "[FAIL] SCRAPINGDOG_API_KEY not set")
    print(f"[OK] APIFY_API_TOKEN: {apify_token[:30]}..." if apify_token else "[FAIL] APIFY_API_TOKEN not set")

    # 測試 config.py 讀取
    print("\n" + "=" * 60)
    print("測試 config.py 從環境變數讀取")
    print("=" * 60)

    import config

    if hasattr(config, 'SERPAPI_KEYS') and config.SERPAPI_KEYS:
        print(f"\n[OK] config.SERPAPI_KEYS: {len(config.SERPAPI_KEYS)} keys loaded")
        for i, key in enumerate(config.SERPAPI_KEYS, 1):
            print(f"  Key {i}: {key[:20]}...{key[-10:]}")
    else:
        print("\n[FAIL] config.SERPAPI_KEYS not set or empty")

    if hasattr(config, 'SCRAPINGDOG_API_KEY') and config.SCRAPINGDOG_API_KEY:
        key = config.SCRAPINGDOG_API_KEY
        print(f"[OK] config.SCRAPINGDOG_API_KEY: {key[:10]}...{key[-5:]}")
    else:
        print("[FAIL] config.SCRAPINGDOG_API_KEY not set or empty")

    print("\n" + "=" * 60)
    print("測試完成")
    print("=" * 60)

if __name__ == "__main__":
    test_env_reading()
