"""測試輸出是否能即時顯示"""
import time
import sys

print("[INFO] 開始測試...")
sys.stdout.flush()

for i in range(1, 6):
    print(f"[INFO] 第 {i} 行輸出")
    sys.stdout.flush()
    time.sleep(1)

print("[INFO] 測試完成！")
sys.stdout.flush()
