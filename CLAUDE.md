# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a production-ready SERP (Search Engine Results Page) ranking tracker that monitors keyword rankings on Google search results.

### System Architecture

**Three API Methods:**
1. **SERP API (recommended)** - Uses serpapi.com API service with multi-key support
2. **Scrapingdog API** - Uses scrapingdog.com API service with pagination
3. **Apify Crawler** - Uses Apify's Google Search Scraper actor

**Two User Interfaces:**
1. **GUI (Graphical User Interface)** - Full-featured tkinter-based GUI with:
   - Real-time progress logging
   - Auto-save/load settings (gui_settings.json)
   - All three API methods support
   - Multi-region selection
   - Unified domain management

2. **CLI (Command Line Interface)** - Interactive menu system (easy_run.bat) for:
   - Terminal-based operation
   - Step-by-step configuration
   - Simplified workflow

**Supported Regions:**
- US (google.com) - English
- TW (google.com.tw) - Traditional Chinese
- HK (google.com.hk) - Traditional Chinese

**Key Features:**
- Multi-region support with localized searches
- Smart encoding detection (UTF-8, Big5, GBK)
- Automatic API key rotation (SERP API)
- Real-time progress tracking
- CSV output with detailed ranking data

## Common Development Commands

### Quick Start Scripts

#### Production Use
```bash
run_gui.bat           # Launch GUI (recommended for end users)
easy_run.bat          # Launch CLI interactive menu
```

#### Development & Testing
```bash
run_test.bat          # Run all tests
analyze_ranks.bat     # Analyze ranking results
setup_api.bat         # Initial setup and dependency installation
```

#### Direct Script Execution
```bash
# SERP API crawler
python serp_api_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY

# Scrapingdog crawler
python scrapingdog_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY

# Apify crawler (requires APIFY_API_TOKEN in .env)
python apify_crawler.py
```

### Testing
All test files are in `tests/` folder:
- `tests/test_apify_crawler.py` - Apify crawler tests
- `tests/test_keywords_reader.py` - Keywords file reader tests
- `tests/serp_api_test.py` - SERP API crawler tests
- `tests/test_keywords.csv` - Test data

## Architecture

### Core Components

#### 1. User Interfaces

**GUI Application** (`gui_app.py`)
- Full-featured tkinter-based graphical interface
- **Real-time features:**
  - Live progress logging with auto-scroll
  - Thread-based execution (non-blocking UI)
  - Stop button to interrupt running searches
- **Settings management:**
  - Auto-save to `gui_settings.json`
  - Auto-load on startup
  - Persists: API method, keys, regions, domain, delays
- **User experience:**
  - Built-in keyword file browser
  - Quick access to results folder
  - Unified domain management (keywords.csv doesn't need domain column)

**CLI Menu System** (`easy_run.bat`)
- Interactive command-line menu
- Step-by-step configuration prompts
- Simplified operation for terminal users
- Integrated with all three API methods

#### 2. Crawlers

**SERP API Crawler** (`serp_api_crawler.py`)
- **Primary features:**
  - Uses serpapi.com for reliable Google search results
  - Multi-key support with automatic rotation
  - Configurable request delays
- **Multi-region support:**
  - US (google.com)
  - TW (google.com.tw)
  - HK (google.com.hk)
- **CLI arguments:** `--regions`, `--domain`, `--keywords_file`, `--api_key`

**Scrapingdog Crawler** (`scrapingdog_crawler.py`)
- Pagination support (up to 100 results)
- Smart optimization: stops when target domain found
- API quota management

**Apify Crawler** (`apify_crawler.py`)
- Uses Apify's Google Search Scraper actor
- Requires `APIFY_API_TOKEN` in `.env`
- Suitable for bulk scraping

#### 3. Utilities

**Configuration** (`config.py`)
- **Environment variables:** Loads API keys from `.env` file
- **Region definitions:** Language, country, domain mappings
- **Default settings:** Regions, delays, output formats
- **Multi-key support:** SERP API keys with comma separation

**Keyword Management** (`keywords_manager.py`)
- **Input format:**
  - GUI mode: CSV with `keyword` column only
  - CLI mode: CSV with `keyword` and `domain` columns
- **Encoding support:** UTF-8, Big5, GBK auto-detection

**Rank Analyzer** (`rank_analyzer.py`)
- Processes CSV results from `results/` folder
- Generates summary statistics
- Command: `analyze_ranks.bat`

### Data Flow

#### GUI Flow
```
1. Startup → Load gui_settings.json (if exists)
2. User configures:
   - API method (SERP/Scrapingdog/Apify)
   - API key
   - Regions (US/TW/HK - multi-select)
   - Target domain
   - Keywords file path
   - Request delay
3. Click "Start Search" → Save settings to gui_settings.json
4. Background thread executes selected crawler
5. Real-time progress → Text widget with auto-scroll
6. Results → results/serp_results_YYYYMMDD_HHMMSS.csv
7. Completion → Show file path, enable "Open Results Folder"
```

#### CLI Flow
```
1. Launch easy_run.bat → Interactive menu
2. User selects:
   - Start new search
   - View instructions
   - Configure SERP API key
   - Exit
3. If "Start new search":
   - Select regions (comma-separated: 1,2,3)
   - Enter target domain
   - Confirm settings
4. Load keywords from keywords.csv
5. Execute crawler for each keyword × region
6. Display progress in terminal
7. Save results to results/ folder
8. Show completion message
```

#### Direct Script Flow
```python
# Example: SERP API
python serp_api_crawler.py \
  --regions US TW HK \
  --domain example.com \
  --keywords_file keywords.csv \
  --api_key YOUR_KEY

# Flow:
1. Parse command-line arguments
2. Load keywords from CSV
3. Initialize API client
4. For each keyword × region:
   - Call API
   - Parse results
   - Extract ranking
5. Write to results/serp_results_YYYYMMDD_HHMMSS.csv
```

## Configuration Management

### Environment Variables (.env file)

**IMPORTANT: All API keys are stored in `.env` (not committed to Git)**

```bash
# SERP API - Multiple keys supported (comma-separated)
SERPAPI_KEYS=key1,key2,key3

# Scrapingdog API
SCRAPINGDOG_API_KEY=your_key

# Apify API
APIFY_API_TOKEN=your_token
```

**Multi-key rotation (SERP API only):**
- System automatically rotates to next key when quota exceeded
- Backward compatible: `SERPAPI_KEY = SERPAPI_KEYS[0]`

### Program Configuration (config.py)

```python
# Region definitions
ALL_REGIONS = {
    'US': {'lang': 'en', 'country': 'us', 'domain': 'google.com'},
    'TW': {'lang': 'zh-TW', 'country': 'tw', 'domain': 'google.com.tw'},
    'HK': {'lang': 'zh-TW', 'country': 'hk', 'domain': 'google.com.hk'}
}

# Default settings
SELECTED_REGIONS = ['TW']
TARGET_DOMAIN = 'mall.sfworldwide.com'

# API delays (seconds)
API_DELAY_BETWEEN_REQUESTS = 5
SCRAPINGDOG_DELAY_BETWEEN_REQUESTS = 5

# Output settings
OUTPUT_FOLDER = 'results'
OUTPUT_FILE_FORMAT = 'csv'  # or 'excel'
```

### Command Line Arguments

All crawlers support these patterns:

**SERP API Crawler:**
```bash
python serp_api_crawler.py \
  --regions US TW HK \
  --domain example.com \
  --keywords_file keywords.csv \
  --api_key YOUR_KEY  # Optional if set in .env
```

**Scrapingdog Crawler:**
```bash
python scrapingdog_crawler.py \
  --regions US TW \
  --domain example.com \
  --keywords_file keywords.csv \
  --api_key YOUR_KEY \
  --delay 5  # Optional delay in seconds
```

**Apify Crawler:**
```bash
python apify_crawler.py
# No arguments needed, uses .env and config.py
```

## Output Format

### CSV Structure
Results saved in `results/serp_results_YYYYMMDD_HHMMSS.csv`:

| Column | Type | Description |
|--------|------|-------------|
| `keyword` | string | Search keyword |
| `region` | string | Search region (US/TW/HK) |
| `rank` | int | Ranking position |
| `url` | string | Found URL |
| `title` | string | Page title |
| `snippet` | string | Search result snippet |

### Rank Values
- **1-100**: Actual ranking position (lower is better)
- **-1**: Not found in top 100 results
- **-2**: Search error occurred

### Generated Files
```
results/
├── serp_results_20250106_143022.csv  # Timestamped results
├── serp_results_20250105_091544.csv
└── archive/                           # Old results (manual move)

gui_settings.json                      # GUI configuration (auto-saved)

keywords.csv                           # Input file
```

### Keywords CSV Format

**GUI Mode (domain from GUI):**
```csv
keyword
digital signage
high brightness display
interactive kiosk
```

**CLI Mode (domain per keyword):**
```csv
keyword,domain
digital signage,agiledisplaysolutions.com
high brightness display,agiledisplaysolutions.com
interactive kiosk,agiledisplaysolutions.com
```

## Development Guide

### Adding New Regions

1. **Add region definition in `config.py`:**
   ```python
   ALL_REGIONS = {
       'US': {'lang': 'en', 'country': 'us', 'domain': 'google.com'},
       'TW': {'lang': 'zh-TW', 'country': 'tw', 'domain': 'google.com.tw'},
       'HK': {'lang': 'zh-TW', 'country': 'hk', 'domain': 'google.com.hk'},
       'JP': {'lang': 'ja', 'country': 'jp', 'domain': 'google.co.jp'},  # New
   }
   ```

2. **Update GUI (`gui_app.py`):**
   - Add checkbox in region selection frame
   - Update region code mapping

3. **Test with all three API methods**

### Modifying GUI

**Architecture:**
- Framework: tkinter with ttk styling
- Threading: `threading.Thread` for non-blocking crawler execution
- Settings: JSON serialization to `gui_settings.json`

**Key components:**
- `SERPCrawlerGUI` class in `gui_app.py`
- Real-time logging: Text widget with custom stream redirection
- Stop mechanism: Thread-safe flag checked during execution

**Adding new features:**
1. Add UI elements in `__init__` or separate methods
2. Update `save_settings()` and `load_settings()` if needed
3. Ensure thread-safe operations for background tasks

### Testing Strategy

**Test structure:**
```
tests/
├── test_apify_crawler.py      # Apify integration tests
├── test_keywords_reader.py    # CSV parsing tests
├── serp_api_test.py          # SERP API integration tests
└── test_keywords.csv         # Test data
```

**Running tests:**
```bash
# All tests
run_test.bat

# Individual crawler
python -m pytest tests/test_apify_crawler.py

# Specific test
python -m pytest tests/serp_api_test.py::test_search_ranking
```

**Adding new tests:**
1. Create test file in `tests/` folder
2. Use pytest framework
3. Include in `run_test.bat`

### Common Development Tasks

**Debugging GUI:**
- Add print statements (will appear in log widget)
- Check `gui_settings.json` for settings persistence
- Test with `--debug` flag if implemented

**Debugging Crawlers:**
- Run directly with command-line arguments
- Check API responses in console
- Verify `.env` file loading

**Code Style:**
- Follow existing patterns in codebase
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Troubleshooting

### Common Issues

**Issue: "API key invalid" error**
- Solution: Check `.env` file format (no spaces around `=`)
- Verify key hasn't expired
- Ensure `.env` is in project root

**Issue: GUI doesn't show progress**
- Solution: Click "Test Output" button to verify logging
- Check if crawler thread started (check console for errors)
- Restart application

**Issue: Chinese characters garbled**
- Solution: System auto-detects encoding
- Ensure keywords.csv saved as UTF-8
- Check console encoding settings

**Issue: Keywords file not found**
- Solution: Use absolute path or place in project root
- Verify file permissions
- Check file name matches exactly

**Issue: Results folder empty**
- Solution: Check for errors in console/GUI log
- Verify API key is valid
- Ensure keywords.csv format is correct

**Issue: Multi-key rotation not working**
- Solution: Check `.env` format: `SERPAPI_KEYS=key1,key2,key3`
- No spaces before/after commas
- At least one valid key required

### Best Practices

**API Key Management:**
- ✅ Store in `.env` file only
- ✅ Never commit `.env` to Git
- ✅ Use multiple keys for higher quota
- ❌ Don't hardcode in scripts
- ❌ Don't share in public repositories

**Keywords File:**
- ✅ Use UTF-8 encoding
- ✅ One keyword per line
- ✅ Keep under 100 keywords per run
- ❌ Don't include special characters in domain
- ❌ Don't use very long keywords (>100 chars)

**Rate Limiting:**
- ✅ Use recommended delays (5 seconds)
- ✅ Monitor API quota usage
- ✅ Spread searches over time
- ❌ Don't set delay < 2 seconds
- ❌ Don't run multiple instances simultaneously

**Results Management:**
- ✅ Check results/ folder regularly
- ✅ Archive old results
- ✅ Verify rankings manually for important keywords
- ✅ Compare results over time

## Project File Structure

```
C:\Users\user\OneDrive\Ming\Vibe Coding\2. Completed\SERP Crawler\
│
├── 📄 Configuration
│   ├── .env                      # API keys (DO NOT COMMIT)
│   ├── .env.example              # Template for API keys
│   ├── .gitignore               # Git ignore rules
│   ├── config.py                # Program configuration
│   ├── gui_settings.json        # GUI settings (auto-generated)
│   └── requirements.txt         # Python dependencies
│
├── 📝 Documentation
│   ├── README.md                # User documentation (Chinese)
│   ├── CLAUDE.md                # Developer documentation (this file)
│   └── docs/                    # Additional documentation
│       ├── README.md
│       └── images/
│
├── 🚀 Executables
│   ├── run_gui.bat              # Launch GUI
│   ├── easy_run.bat             # Launch CLI menu
│   ├── setup_api.bat            # Setup script
│   ├── analyze_ranks.bat        # Rank analysis
│   └── run_test.bat             # Run tests
│
├── 💻 Source Code
│   ├── gui_app.py               # GUI application
│   ├── serp_api_crawler.py      # SERP API crawler
│   ├── scrapingdog_crawler.py   # Scrapingdog crawler
│   ├── apify_crawler.py         # Apify crawler
│   ├── keywords_manager.py      # Keywords CSV handler
│   └── rank_analyzer.py         # Results analyzer
│
├── 🧪 Tests
│   └── tests/
│       ├── __init__.py
│       ├── test_apify_crawler.py
│       ├── test_keywords_reader.py
│       ├── serp_api_test.py
│       └── test_keywords.csv
│
├── 📊 Data
│   ├── keywords.csv             # Input keywords
│   └── results/                 # Output results
│       ├── serp_results_*.csv
│       └── archive/
│
└── 📦 Archive
    └── archive/                 # Old files/versions
        └── README_GUI.md
```

## Version History

- **v2.0** (2025-01-06): Complete rewrite with GUI and multi-API support
- **v1.x**: Initial CLI-only versions

## Maintainer Notes

**When updating this file:**
- Keep synchronized with README.md
- Update version history
- Document breaking changes
- Add migration guides if needed

**Before deploying:**
- Run all tests: `run_test.bat`
- Test GUI with all three API methods
- Verify CLI menu works
- Check .env.example is up to date
- Ensure .gitignore covers sensitive files