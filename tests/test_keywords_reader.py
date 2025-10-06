import pandas as pd
import chardet

def detect_encoding(file_path):
    """檢測檔案編碼"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def read_keywords_file():
    """讀取關鍵字檔案並處理編碼問題"""
    file_path = "keywords.csv"
    
    # 嘗試檢測編碼
    print("正在檢測檔案編碼...")
    try:
        detected_encoding = detect_encoding(file_path)
        print(f"檢測到的編碼: {detected_encoding}")
    except Exception as e:
        print(f"編碼檢測失敗: {e}")
        detected_encoding = None
    
    # 嘗試不同的編碼讀取檔案
    encodings_to_try = ['utf-8', 'big5', 'gb2312', 'cp950', 'utf-8-sig']
    if detected_encoding:
        encodings_to_try.insert(0, detected_encoding)
    
    df = None
    successful_encoding = None
    
    for encoding in encodings_to_try:
        try:
            print(f"嘗試使用編碼: {encoding}")
            df = pd.read_csv(file_path, encoding=encoding)
            successful_encoding = encoding
            print(f"✅ 成功使用編碼: {encoding}")
            break
        except Exception as e:
            print(f"❌ 編碼 {encoding} 失敗: {e}")
            continue
    
    if df is None:
        print("❌ 無法讀取檔案，所有編碼都失敗")
        return None, None
    
    return df, successful_encoding

def display_keywords():
    """顯示關鍵字列表"""
    df, encoding = read_keywords_file()
    
    if df is None:
        return
    
    print(f"\n📋 關鍵字檔案內容 (使用編碼: {encoding})")
    print("=" * 60)
    
    # 顯示檔案資訊
    print(f"總共關鍵字數量: {len(df)}")
    print(f"欄位: {list(df.columns)}")
    
    if 'keyword' in df.columns:
        print("\n🔍 關鍵字列表:")
        print("-" * 40)
        for i, keyword in enumerate(df['keyword'], 1):
            print(f"{i:2d}. {keyword}")
        
        print(f"\n🎯 目標網域: {df['domain'].iloc[0] if 'domain' in df.columns else '未指定'}")
        
        # 顯示一些統計資訊
        print(f"\n📊 統計資訊:")
        print(f"   - 最短關鍵字長度: {df['keyword'].str.len().min()}")
        print(f"   - 最長關鍵字長度: {df['keyword'].str.len().max()}")
        print(f"   - 平均關鍵字長度: {df['keyword'].str.len().mean():.1f}")
        
        return df
    else:
        print("❌ 找不到 'keyword' 欄位")
        print("檔案內容預覽:")
        print(df.head())
        return df

if __name__ == "__main__":
    print("🚀 關鍵字檔案讀取器")
    print("=" * 50)
    
    keywords_df = display_keywords()
    
    if keywords_df is not None:
        print(f"\n✅ 檔案讀取完成！共 {len(keywords_df)} 個關鍵字")
        print("💡 注意: 此程式只讀取和顯示關鍵字，不會啟動 Apify")
    else:
        print("❌ 檔案讀取失敗") 