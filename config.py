# ?��?引�?設�?
ALL_REGIONS = {
    'US': {'lang': 'en', 'country': 'us', 'domain': 'google.com'},
    'TW': {'lang': 'zh-TW', 'country': 'tw', 'domain': 'google.com.tw'},
    'HK': {'lang': 'zh-TW', 'country': 'hk', 'domain': 'google.com.hk'}
}

# 使用?�可設�??��???
SELECTED_REGIONS = ['TW']  # ?�設?��?尋台??
TARGET_DOMAIN = 'mall.sfworldwide.com'  # ?�設?��?網�?

# ?�蟲設�? (?��?Selenium?��?)
DELAY_BETWEEN_REQUESTS = 8  # 每次請�??��?秒數 (增�???8 秒�??��?被檢測風??
MAX_PAGES_TO_SEARCH = 5    # 設�???5 ?��??�管使用�?num=100，Google 仍可?��??�顯�?
RESULTS_PER_PAGE = 10      # ?�設每�??�能顯示?��??�數

# 載入環境變數
import os
from dotenv import load_dotenv
load_dotenv()

# SERP API 設定 - 從環境變數讀取
# 支援多組 API keys，當第一組達到限制時會自動切換到下一組
# 在 .env 中設定: SERPAPI_KEYS=key1,key2,key3
serpapi_keys_str = os.getenv('SERPAPI_KEYS', '')
SERPAPI_KEYS = [key.strip() for key in serpapi_keys_str.split(',') if key.strip()]

# 向後兼容：如果程式使用 SERPAPI_KEY，則使用第一組
SERPAPI_KEY = SERPAPI_KEYS[0] if SERPAPI_KEYS else None

API_DELAY_BETWEEN_REQUESTS = 5  # API請求間延遲秒數，避免超過免費方案限制

# Scrapingdog API 設定 - 從環境變數讀取
SCRAPINGDOG_API_KEY = os.getenv('SCRAPINGDOG_API_KEY', '')
SCRAPINGDOG_DELAY_BETWEEN_REQUESTS = 5  # API請求間延遲秒數

# 輸出設�?
OUTPUT_FOLDER = 'results'
OUTPUT_FILE_FORMAT = 'csv'   # ?�選 'csv' ??'excel'

# ?�覽?�設�?(?��?Selenium?��?)
BROWSER_TYPE = 'chrome'     # 使用 Chrome ?�覽??
HEADLESS = False            # 禁用?�頭模�?，以便�??�解決�?證碼 
