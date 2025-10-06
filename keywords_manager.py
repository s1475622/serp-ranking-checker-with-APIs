import pandas as pd
import chardet
from datetime import datetime

class KeywordsManager:
    def __init__(self, keywords_file="keywords.csv"):
        self.keywords_file = keywords_file
        self.keywords_df = None
        self.target_domain = None
        self.keywords_list = []
        
    def detect_encoding(self):
        """檢測檔案編碼"""
        with open(self.keywords_file, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            return result['encoding']
    
    def load_keywords(self):
        """載入關鍵字檔案"""
        print("🔍 正在載入關鍵字檔案...")
        
        try:
            # 檢測並使用正確編碼
            encoding = self.detect_encoding()
            print(f"   檢測到編碼: {encoding}")
            
            # 讀取檔案
            self.keywords_df = pd.read_csv(self.keywords_file, encoding=encoding)
            
            # 提取關鍵字和目標網域
            if 'keyword' in self.keywords_df.columns:
                self.keywords_list = self.keywords_df['keyword'].tolist()
                print(f"   ✅ 成功載入 {len(self.keywords_list)} 個關鍵字")
                
                if 'domain' in self.keywords_df.columns:
                    self.target_domain = self.keywords_df['domain'].iloc[0]
                    print(f"   🎯 目標網域: {self.target_domain}")
                
                return True
            else:
                print("   ❌ 找不到 'keyword' 欄位")
                return False
                
        except Exception as e:
            print(f"   ❌ 載入失敗: {e}")
            return False
    
    def get_keywords_summary(self):
        """取得關鍵字摘要資訊"""
        if not self.keywords_list:
            return None
            
        return {
            'total_keywords': len(self.keywords_list),
            'target_domain': self.target_domain,
            'keywords': self.keywords_list,
            'categories': self.categorize_keywords()
        }
    
    def categorize_keywords(self):
        """將關鍵字分類"""
        categories = {
            '益生菌相關': [],
            '魚油相關': [],
            '葡萄糖胺相關': [],
            '滴雞精/雞精相關': [],
            '靈芝相關': [],
            '葉黃素相關': [],
            '保久乳相關': [],
            '四物飲相關': [],
            '其他': []
        }
        
        for keyword in self.keywords_list:
            if '益生菌' in keyword:
                categories['益生菌相關'].append(keyword)
            elif '魚油' in keyword:
                categories['魚油相關'].append(keyword)
            elif '葡萄糖胺' in keyword:
                categories['葡萄糖胺相關'].append(keyword)
            elif '雞精' in keyword:
                categories['滴雞精/雞精相關'].append(keyword)
            elif '靈芝' in keyword:
                categories['靈芝相關'].append(keyword)
            elif '葉黃素' in keyword:
                categories['葉黃素相關'].append(keyword)
            elif '保久乳' in keyword:
                categories['保久乳相關'].append(keyword)
            elif '四物' in keyword:
                categories['四物飲相關'].append(keyword)
            else:
                categories['其他'].append(keyword)
        
        # 移除空分類
        return {k: v for k, v in categories.items() if v}
    
    def display_keywords_analysis(self):
        """顯示關鍵字分析"""
        if not self.load_keywords():
            return
        
        print("\n" + "="*60)
        print("📊 關鍵字分析報告")
        print("="*60)
        
        summary = self.get_keywords_summary()
        
        print(f"📈 總計: {summary['total_keywords']} 個關鍵字")
        print(f"🎯 目標網域: {summary['target_domain']}")
        
        print(f"\n🏷️  關鍵字分類:")
        for category, keywords in summary['categories'].items():
            print(f"\n   📁 {category} ({len(keywords)}個):")
            for i, keyword in enumerate(keywords, 1):
                print(f"      {i:2d}. {keyword}")
        
        print(f"\n📋 完整關鍵字列表:")
        print("-"*40)
        for i, keyword in enumerate(self.keywords_list, 1):
            print(f"{i:2d}. {keyword}")
        
        print(f"\n📊 統計資訊:")
        keyword_lengths = [len(k) for k in self.keywords_list]
        print(f"   - 最短關鍵字: {min(keyword_lengths)} 字")
        print(f"   - 最長關鍵字: {max(keyword_lengths)} 字")
        print(f"   - 平均長度: {sum(keyword_lengths)/len(keyword_lengths):.1f} 字")
        
        return summary

def prepare_search_plan(keywords_manager):
    """準備搜尋計劃（不執行）"""
    print("\n" + "="*60)
    print("🚀 搜尋計劃準備")
    print("="*60)
    
    summary = keywords_manager.get_keywords_summary()
    if not summary:
        print("❌ 無法建立搜尋計劃，關鍵字載入失敗")
        return
    
    print(f"📋 將要搜尋的關鍵字數量: {summary['total_keywords']}")
    print(f"🎯 目標網域: {summary['target_domain']}")
    print(f"📊 預計取得結果數: {summary['total_keywords'] * 100} 筆 (每個關鍵字100筆)")
    
    print(f"\n⚙️  搜尋設定:")
    print(f"   - 每個關鍵字取得前100名結果")
    print(f"   - 地區設定: 台灣 (TW)")
    print(f"   - 語言設定: 繁體中文 (zh-TW)")
    print(f"   - 結果格式: CSV")
    
    print(f"\n🕐 預估時間:")
    print(f"   - 每個關鍵字約需 30-60 秒")
    print(f"   - 總計約需 {summary['total_keywords'] * 0.75:.0f}-{summary['total_keywords'] * 1:.0f} 分鐘")
    
    print(f"\n💡 注意事項:")
    print(f"   - 此程式目前僅分析關鍵字，未啟動 Apify")
    print(f"   - 如需執行搜尋，請另外呼叫搜尋功能")
    print(f"   - 建議分批執行以避免API限制")

if __name__ == "__main__":
    print("🚀 關鍵字管理系統")
    print("="*50)
    
    # 建立關鍵字管理器
    km = KeywordsManager()
    
    # 顯示分析結果
    summary = km.display_keywords_analysis()
    
    if summary:
        # 準備搜尋計劃
        prepare_search_plan(km)
        
        print(f"\n✅ 關鍵字分析完成！")
        print(f"💡 準備就緒，可以開始搜尋分析")
    else:
        print("❌ 關鍵字管理系統初始化失敗") 