"""
SERP 排名追蹤器 - GUI 版本 V3
- 使用 pack 佈局確保所有元件都能顯示
- API Keys 儲存至 .env 檔案（而非 config.py）
- 支援即時更新環境變數
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import threading
import os
import json
from datetime import datetime
import config
import locale


class SERPTrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SERP 排名追蹤器")

        # 取得螢幕尺寸並設定視窗大小
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 900
        window_height = min(850, int(screen_height * 0.9))

        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(True, True)

        # 設定樣式
        style = ttk.Style()
        style.theme_use('clam')

        # 執行中的旗標
        self.running = False

        # 設定檔案路徑
        self.settings_file = "gui_settings.json"

        self.create_widgets()
        self.load_saved_settings()

    def create_widgets(self):
        # 主容器
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 標題
        title_label = ttk.Label(
            main_frame,
            text="SERP 排名追蹤器",
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=10)

        # 建立左右兩欄佈局（使用 PanedWindow 實現比例分配）
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # 左側：設定區域（60%）
        left_container = ttk.Frame(paned)
        paned.add(left_container, weight=60)

        # 建立 Canvas 和 Scrollbar 實現捲動
        left_canvas = tk.Canvas(left_container)
        left_scrollbar = ttk.Scrollbar(left_container, orient="vertical", command=left_canvas.yview)

        left_frame = ttk.Frame(left_canvas)

        # 建立視窗並保存 window id
        canvas_window = left_canvas.create_window((0, 0), window=left_frame, anchor="nw")

        def configure_scroll_region(event=None):
            left_canvas.configure(scrollregion=left_canvas.bbox("all"))

        def configure_canvas_width(event=None):
            # 當 canvas 寬度改變時，調整內部 frame 的寬度
            canvas_width = event.width if event else left_canvas.winfo_width()
            left_canvas.itemconfig(canvas_window, width=canvas_width)

        left_frame.bind("<Configure>", configure_scroll_region)
        left_canvas.bind("<Configure>", configure_canvas_width)

        left_canvas.configure(yscrollcommand=left_scrollbar.set)

        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 滑鼠滾輪支援
        def _on_mousewheel(event):
            left_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        left_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 右側：執行紀錄（40%）
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=40)

        # === 左側設定區域 ===

        # API 選擇區域
        api_frame = ttk.LabelFrame(left_frame, text="API 服務選擇", padding="10")
        api_frame.pack(fill=tk.X, pady=5)

        self.api_var = tk.StringVar(value="SERP")

        ttk.Radiobutton(
            api_frame,
            text="SERP API (推薦 - 穩定可靠，免費每月100次)",
            variable=self.api_var,
            value="SERP"
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            api_frame,
            text="Scrapingdog API (提供免費試用)",
            variable=self.api_var,
            value="SCRAPINGDOG"
        ).pack(anchor=tk.W, pady=2)

        ttk.Radiobutton(
            api_frame,
            text="Apify API (適合大量爬取)",
            variable=self.api_var,
            value="APIFY"
        ).pack(anchor=tk.W, pady=2)

        # 地區選擇
        region_frame = ttk.LabelFrame(left_frame, text="搜尋地區", padding="10")
        region_frame.pack(fill=tk.X, pady=5)

        self.region_us = tk.BooleanVar(value=False)
        self.region_tw = tk.BooleanVar(value=True)
        self.region_hk = tk.BooleanVar(value=False)

        region_inner = ttk.Frame(region_frame)
        region_inner.pack(fill=tk.X)

        ttk.Checkbutton(
            region_inner,
            text="美國 (US) - 英文",
            variable=self.region_us
        ).pack(side=tk.LEFT, padx=10)

        ttk.Checkbutton(
            region_inner,
            text="台灣 (TW) - 繁體中文",
            variable=self.region_tw
        ).pack(side=tk.LEFT, padx=10)

        ttk.Checkbutton(
            region_inner,
            text="香港 (HK) - 繁體中文",
            variable=self.region_hk
        ).pack(side=tk.LEFT, padx=10)

        # 目標網域設定
        domain_frame = ttk.LabelFrame(left_frame, text="目標網域", padding="10")
        domain_frame.pack(fill=tk.X, pady=5)

        domain_inner = ttk.Frame(domain_frame)
        domain_inner.pack(fill=tk.X)

        ttk.Label(domain_inner, text="網域:").pack(side=tk.LEFT)
        self.domain_entry = ttk.Entry(domain_inner, width=60)
        self.domain_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.domain_entry.insert(0, config.TARGET_DOMAIN)

        ttk.Label(
            domain_frame,
            text="💡 提示: 所有關鍵字都會使用此網域進行排名追蹤",
            font=('Arial', 8),
            foreground='gray'
        ).pack(anchor=tk.W, pady=(5, 0))

        # 關鍵字檔案
        keywords_frame = ttk.LabelFrame(left_frame, text="關鍵字檔案", padding="10")
        keywords_frame.pack(fill=tk.X, pady=5)

        keywords_inner = ttk.Frame(keywords_frame)
        keywords_inner.pack(fill=tk.X)

        ttk.Label(keywords_inner, text="檔案:").pack(side=tk.LEFT)
        self.keywords_entry = ttk.Entry(keywords_inner, width=50)
        self.keywords_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.keywords_entry.insert(0, "keywords.csv")

        ttk.Button(
            keywords_inner,
            text="瀏覽...",
            command=self.browse_keywords_file
        ).pack(side=tk.LEFT, padx=5)

        # API 金鑰設定（儲存至 .env 檔案）
        api_key_frame = ttk.LabelFrame(left_frame, text="API 金鑰設定（存入 .env）", padding="10")
        api_key_frame.pack(fill=tk.X, pady=5)

        # SERP API Keys (支援多組)
        serp_label_frame = ttk.Frame(api_key_frame)
        serp_label_frame.pack(fill=tk.X, pady=2)
        ttk.Label(serp_label_frame, text="SERP API:", width=12).pack(side=tk.LEFT)
        ttk.Label(
            serp_label_frame,
            text="(支援多組，每行一組)",
            font=('Arial', 8),
            foreground='gray'
        ).pack(side=tk.LEFT, padx=5)

        # 使用 Text widget 支援多行輸入
        serp_text_frame = ttk.Frame(api_key_frame)
        serp_text_frame.pack(fill=tk.X, pady=2, padx=(0, 0))

        # 左側空白對齊
        ttk.Label(serp_text_frame, text="", width=12).pack(side=tk.LEFT)

        # Text widget 及 Scrollbar
        serp_inner_frame = ttk.Frame(serp_text_frame)
        serp_inner_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.serp_keys_text = tk.Text(serp_inner_frame, height=3, width=50, wrap=tk.NONE)
        serp_scrollbar = ttk.Scrollbar(serp_inner_frame, orient=tk.VERTICAL, command=self.serp_keys_text.yview)
        self.serp_keys_text.configure(yscrollcommand=serp_scrollbar.set)

        self.serp_keys_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        serp_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # 更新按鈕
        ttk.Button(
            serp_text_frame,
            text="更新",
            command=lambda: self.update_api_key("SERP"),
            width=8
        ).pack(side=tk.LEFT, padx=5)

        # Scrapingdog API Key
        scrapingdog_frame = ttk.Frame(api_key_frame)
        scrapingdog_frame.pack(fill=tk.X, pady=2)
        ttk.Label(scrapingdog_frame, text="Scrapingdog:", width=12).pack(side=tk.LEFT)
        self.scrapingdog_key_entry = ttk.Entry(scrapingdog_frame, width=50)
        self.scrapingdog_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(
            scrapingdog_frame,
            text="更新",
            command=lambda: self.update_api_key("SCRAPINGDOG"),
            width=8
        ).pack(side=tk.LEFT, padx=5)

        # Apify API Key
        apify_frame = ttk.Frame(api_key_frame)
        apify_frame.pack(fill=tk.X, pady=2)
        ttk.Label(apify_frame, text="Apify:", width=12).pack(side=tk.LEFT)
        self.apify_key_entry = ttk.Entry(apify_frame, width=50)
        self.apify_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(
            apify_frame,
            text="更新",
            command=lambda: self.update_api_key("APIFY"),
            width=8
        ).pack(side=tk.LEFT, padx=5)

        # 控制按鈕
        button_frame = ttk.Frame(left_frame, padding="10")
        button_frame.pack(fill=tk.X, pady=10)

        # 按鈕使用 grid 排列成兩列
        btn_frame_top = ttk.Frame(button_frame)
        btn_frame_top.pack(fill=tk.X, pady=2)

        btn_frame_bottom = ttk.Frame(button_frame)
        btn_frame_bottom.pack(fill=tk.X, pady=2)

        self.start_button = ttk.Button(
            btn_frame_top,
            text="開始搜尋",
            command=self.start_search
        )
        self.start_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.stop_button = ttk.Button(
            btn_frame_top,
            text="停止",
            command=self.stop_search,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        ttk.Button(
            btn_frame_bottom,
            text="開啟結果資料夾",
            command=self.open_results_folder
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        ttk.Button(
            btn_frame_bottom,
            text="測試輸出",
            command=self.test_output
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # === 右側執行紀錄區域 ===
        output_frame = ttk.LabelFrame(right_frame, text="執行紀錄", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            font=('Consolas', 9),
            bg='white'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def mask_api_key(self, key):
        """遮蔽 API key 的中間部分，只顯示前4和後4個字元"""
        if not key or len(key) <= 12:
            return key
        return f"{key[:6]}...{key[-6:]}"

    def load_saved_settings(self):
        """載入儲存的設定"""
        # 顯示歡迎訊息
        self.log_output("="*60)
        self.log_output("歡迎使用 SERP 排名追蹤器 GUI 版本")
        self.log_output("="*60)

        # 先載入 API 金鑰
        try:
            # 載入 SERP API Keys（支援多組）
            if hasattr(config, 'SERPAPI_KEYS'):
                keys = config.SERPAPI_KEYS
                if keys and isinstance(keys, list):
                    # 顯示遮蔽後的 keys
                    masked_keys = [self.mask_api_key(k) for k in keys if k]
                    self.serp_keys_text.delete(1.0, tk.END)
                    self.serp_keys_text.insert(1.0, '\n'.join(masked_keys))
                    self.log_output(f"✓ 已載入 {len(masked_keys)} 組 SERP API 金鑰")
            elif hasattr(config, 'SERPAPI_KEY'):
                # 向後兼容單一 key
                key = config.SERPAPI_KEY
                if key:
                    self.serp_keys_text.delete(1.0, tk.END)
                    self.serp_keys_text.insert(1.0, self.mask_api_key(key))
                    self.log_output("✓ 已載入 SERP API 金鑰")

            if hasattr(config, 'SCRAPINGDOG_API_KEY'):
                key = config.SCRAPINGDOG_API_KEY
                if key:
                    self.scrapingdog_key_entry.insert(0, self.mask_api_key(key))
                    self.log_output("✓ 已載入 Scrapingdog API 金鑰")

            # 載入 Apify API Token
            apify_token = os.environ.get('APIFY_API_TOKEN', '')
            if apify_token:
                self.apify_key_entry.insert(0, self.mask_api_key(apify_token))
                self.log_output("✓ 已載入 Apify API Token")

        except Exception as e:
            self.log_output(f"⚠ 載入 API 金鑰時發生錯誤: {str(e)}")

        # 載入 GUI 設定
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)

                # 恢復 API 選擇
                if 'api_type' in settings:
                    self.api_var.set(settings['api_type'])

                # 恢復地區選擇
                if 'regions' in settings:
                    self.region_us.set(settings['regions'].get('US', False))
                    self.region_tw.set(settings['regions'].get('TW', True))
                    self.region_hk.set(settings['regions'].get('HK', False))

                # 恢復目標網域
                if 'domain' in settings and settings['domain']:
                    self.domain_entry.delete(0, tk.END)
                    self.domain_entry.insert(0, settings['domain'])

                # 恢復關鍵字檔案
                if 'keywords_file' in settings and settings['keywords_file']:
                    self.keywords_entry.delete(0, tk.END)
                    self.keywords_entry.insert(0, settings['keywords_file'])

                self.log_output(f"✓ 已載入上次的設定 ({settings.get('last_updated', '')})")

            except Exception as e:
                self.log_output(f"⚠ 載入設定檔時發生錯誤: {str(e)}")
        else:
            self.log_output("ℹ 首次使用，使用預設設定")

        self.log_output("")
        self.log_output("💡 提示: 點擊「測試輸出」按鈕可測試即時輸出功能")
        self.log_output("="*60)

    def save_settings(self):
        """儲存目前的設定"""
        try:
            settings = {
                'api_type': self.api_var.get(),
                'regions': {
                    'US': self.region_us.get(),
                    'TW': self.region_tw.get(),
                    'HK': self.region_hk.get()
                },
                'domain': self.domain_entry.get().strip(),
                'keywords_file': self.keywords_entry.get().strip(),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)

            return True
        except Exception as e:
            self.log_output(f"儲存設定時發生錯誤: {str(e)}")
            return False

    def browse_keywords_file(self):
        """瀏覽選擇關鍵字檔案"""
        filename = filedialog.askopenfilename(
            title="選擇關鍵字檔案",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.keywords_entry.delete(0, tk.END)
            self.keywords_entry.insert(0, filename)

    def update_api_key(self, api_type):
        """更新 API 金鑰到 .env 檔案"""
        if api_type == "SERP":
            # 取得多行輸入的 API keys
            new_keys_text = self.serp_keys_text.get(1.0, tk.END).strip()
            if not new_keys_text:
                messagebox.showwarning("警告", "請輸入至少一組 SERP API 金鑰")
                return

            # 分割成多組 keys（每行一組）
            new_keys = [key.strip() for key in new_keys_text.split('\n') if key.strip()]

            # 組合成逗號分隔的字串
            keys_str = ','.join(new_keys)

            self._update_env_variable("SERPAPI_KEYS", keys_str, f"{len(new_keys)} 組 SERP API")

        elif api_type == "SCRAPINGDOG":
            new_key = self.scrapingdog_key_entry.get().strip()
            if not new_key:
                messagebox.showwarning("警告", "請輸入 Scrapingdog API 金鑰")
                return

            self._update_env_variable("SCRAPINGDOG_API_KEY", new_key, "Scrapingdog API")

        elif api_type == "APIFY":
            new_key = self.apify_key_entry.get().strip()
            if not new_key:
                messagebox.showwarning("警告", "請輸入 Apify API 金鑰")
                return

            self._update_env_variable("APIFY_API_TOKEN", new_key, "Apify API")

    def _update_env_variable(self, var_name, var_value, api_name):
        """更新環境變數到 .env 檔案"""
        try:
            env_file = '.env'

            # 讀取現有的 .env 檔案（如果存在）
            env_lines = []
            if os.path.exists(env_file):
                with open(env_file, 'r', encoding='utf-8') as f:
                    env_lines = f.readlines()

            # 尋找並更新對應的變數
            updated = False
            for i, line in enumerate(env_lines):
                # 跳過註解和空行
                if line.strip().startswith('#') or not line.strip():
                    continue

                # 檢查是否為目標變數
                if line.strip().startswith(f'{var_name}='):
                    env_lines[i] = f'{var_name}={var_value}\n'
                    updated = True
                    break

            # 如果沒找到，添加新的變數
            if not updated:
                # 確保檔案以換行結尾
                if env_lines and not env_lines[-1].endswith('\n'):
                    env_lines[-1] += '\n'
                env_lines.append(f'\n# {api_name} Key\n')
                env_lines.append(f'{var_name}={var_value}\n')

            # 寫回檔案
            with open(env_file, 'w', encoding='utf-8') as f:
                f.writelines(env_lines)

            # 更新當前程序的環境變數
            os.environ[var_name] = var_value

            # 重新載入 config 模組以讀取新的環境變數
            import importlib
            importlib.reload(config)

            messagebox.showinfo("成功", f"{api_name} 金鑰已更新到 .env 檔案！\n改變已立即生效。")
            self.log_output(f"✓ {api_name} 金鑰已更新到 .env")

        except Exception as e:
            messagebox.showerror("錯誤", f"更新失敗: {str(e)}")
            self.log_output(f"✗ {api_name} 金鑰更新失敗: {str(e)}")

    def get_selected_regions(self):
        """取得選擇的地區"""
        regions = []
        if self.region_us.get():
            regions.append('US')
        if self.region_tw.get():
            regions.append('TW')
        if self.region_hk.get():
            regions.append('HK')
        return regions

    def log_output(self, message):
        """記錄輸出訊息"""
        if not message or message.isspace():
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)
        self.output_text.update()
        self.root.update_idletasks()

    def start_search(self):
        """開始搜尋"""
        regions = self.get_selected_regions()
        if not regions:
            messagebox.showwarning("警告", "請至少選擇一個搜尋地區")
            return

        domain = self.domain_entry.get().strip()
        if not domain:
            messagebox.showwarning("警告", "請輸入目標網域")
            return

        keywords_file = self.keywords_entry.get().strip()
        if not os.path.exists(keywords_file):
            messagebox.showwarning("警告", f"關鍵字檔案不存在: {keywords_file}")
            return

        if self.save_settings():
            self.log_output("✓ 已儲存目前設定")

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.running = True

        self.output_text.delete(1.0, tk.END)

        thread = threading.Thread(target=self.run_crawler, args=(regions, domain, keywords_file))
        thread.daemon = True
        thread.start()

    def run_crawler(self, regions, domain, keywords_file):
        """執行爬蟲"""
        api_type = self.api_var.get()

        try:
            self.log_output(f"開始執行 {api_type} API 爬蟲...")
            self.log_output(f"搜尋地區: {', '.join(regions)}")
            self.log_output(f"目標網域: {domain}")
            self.log_output(f"關鍵字檔: {keywords_file}")
            self.log_output("-" * 60)

            if api_type == "APIFY":
                cmd = ['python', '-u', 'apify_crawler.py']
            elif api_type == "SCRAPINGDOG":
                cmd = ['python', '-u', 'scrapingdog_crawler.py',
                       '--regions'] + regions + ['--domain', domain]
                if keywords_file != "keywords.csv":
                    cmd.extend(['--keywords_file', keywords_file])
            else:
                cmd = ['python', '-u', 'serp_api_crawler.py',
                       '--regions'] + regions + ['--domain', domain]
                if keywords_file != "keywords.csv":
                    cmd.extend(['--keywords_file', keywords_file])

            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'

            # 使用 bytes 模式來避免編碼問題
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=0,
                env=env
            )

            # 準備多種編碼嘗試
            system_encoding = locale.getpreferredencoding()
            encodings_to_try = ['utf-8', system_encoding, 'cp950', 'big5', 'gbk']

            while True:
                if not self.running:
                    process.terminate()
                    self.log_output("使用者中止執行")
                    break

                line_bytes = process.stdout.readline()
                if not line_bytes and process.poll() is not None:
                    break

                if line_bytes:
                    # 嘗試多種編碼解碼
                    decoded = None
                    for encoding in encodings_to_try:
                        try:
                            decoded = line_bytes.decode(encoding).rstrip()
                            break
                        except (UnicodeDecodeError, AttributeError):
                            continue

                    # 如果都失敗，使用 replace 模式
                    if decoded is None:
                        decoded = line_bytes.decode('utf-8', errors='replace').rstrip()

                    if decoded:  # 只顯示非空行
                        self.log_output(decoded)
                    self.root.update_idletasks()

            return_code = process.poll()
            if return_code == 0:
                self.log_output("-" * 60)
                self.log_output("✓ 搜尋完成！結果已保存到 results 資料夾")
                messagebox.showinfo("完成", "搜尋完成！結果已保存到 results 資料夾")
            else:
                self.log_output(f"✗ 執行失敗，返回碼: {return_code}")
                messagebox.showerror("錯誤", "執行過程中發生錯誤，請查看執行紀錄")

        except Exception as e:
            self.log_output(f"✗ 發生錯誤: {str(e)}")
            messagebox.showerror("錯誤", f"執行失敗: {str(e)}")

        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.running = False

    def stop_search(self):
        """停止搜尋"""
        self.running = False
        self.log_output("正在停止...")

    def open_results_folder(self):
        """開啟結果資料夾"""
        results_folder = config.OUTPUT_FOLDER
        if os.path.exists(results_folder):
            os.startfile(results_folder)
        else:
            messagebox.showwarning("警告", f"結果資料夾不存在: {results_folder}")

    def test_output(self):
        """測試即時輸出功能"""
        try:
            self.output_text.delete(1.0, tk.END)
            self.log_output("開始測試即時輸出...")
            self.log_output(f"工作目錄: {os.getcwd()}")

            test_file = os.path.join('tests', 'test_output.py')
            if not os.path.exists(test_file):
                self.log_output("❌ 錯誤: tests\\test_output.py 檔案不存在！")
                return

            def run_test():
                try:
                    self.log_output("正在啟動測試程序...")

                    env = os.environ.copy()
                    env['PYTHONUNBUFFERED'] = '1'
                    env['PYTHONIOENCODING'] = 'utf-8'

                    process = subprocess.Popen(
                        ['python', '-u', test_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        encoding='utf-8',
                        errors='replace',
                        bufsize=0,
                        env=env
                    )

                    self.log_output("測試程序已啟動，等待輸出...")

                    while True:
                        line = process.stdout.readline()
                        if not line and process.poll() is not None:
                            break
                        if line:
                            self.log_output(f"[測試輸出] {line.rstrip()}")
                            self.root.update_idletasks()

                    stderr = process.stderr.read()
                    if stderr:
                        self.log_output(f"錯誤訊息: {stderr}")

                    return_code = process.poll()
                    self.log_output(f"測試程序結束，返回碼: {return_code}")

                    if return_code == 0:
                        self.log_output("✅ 測試完成！")
                    else:
                        self.log_output(f"❌ 測試失敗，返回碼: {return_code}")

                except Exception as e:
                    import traceback
                    self.log_output(f"❌ 測試失敗: {str(e)}")
                    self.log_output(f"詳細錯誤: {traceback.format_exc()}")

            thread = threading.Thread(target=run_test)
            thread.daemon = True
            thread.start()

        except Exception as e:
            import traceback
            self.log_output(f"❌ 啟動測試失敗: {str(e)}")
            self.log_output(f"詳細錯誤: {traceback.format_exc()}")


def main():
    root = tk.Tk()
    app = SERPTrackerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
