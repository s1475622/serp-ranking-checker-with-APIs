# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a SERP (Search Engine Results Page) ranking tracker that monitors keyword rankings on Google search results. It provides three API methods and two user interfaces:

**API Methods:**
1. SERP API (recommended) - Uses serpapi.com API service
2. Scrapingdog API - Uses scrapingdog.com API service
3. Apify Crawler - Uses Apify's Google Search Scraper

**User Interfaces:**
1. GUI (Graphical User Interface) - Full-featured tkinter-based GUI with real-time progress
2. CLI (Command Line Interface) - Interactive menu system for terminal use

The system supports multiple regions (US, TW, HK) and tracks domain rankings across different Google localizations.

## Common Development Commands

### Running the Application
- `run_gui.bat` - Launch the graphical user interface (recommended for users)
- `easy_run.bat` - Interactive CLI menu system for terminal operation
- `analyze_ranks.bat` - Run rank analysis tool on results

### Testing
- `run_test.bat` - Run tests
- Test files are located in the `tests/` folder:
  - `tests/test_apify_crawler.py` - Test Apify crawler
  - `tests/test_keywords_reader.py` - Test keywords file reader
  - `tests/serp_api_test.py` - Test SERP API crawler

### Setup
- `setup_api.bat` - Initial setup and installation for SERP API version

## Architecture

### Core Components

#### User Interfaces
1. **GUI Application** (`gui_app.py`):
   - Full-featured tkinter-based graphical interface
   - Real-time progress display and logging
   - Settings persistence with JSON storage
   - Supports all three API methods
   - Built-in keyword file selector
   - Configurable request delays and region selection

2. **CLI Menu System** (via `easy_run.bat`):
   - Interactive command-line menu
   - Step-by-step configuration prompts
   - Simplified operation for terminal users

#### Crawlers
3. **SERP API Crawler** (`serp_api_crawler.py`):
   - Uses serpapi.com service for reliable Google search results
   - Handles API key management and rate limiting
   - Supports multi-region searches (US, TW, HK)
   - Command-line interface with argparse

4. **Scrapingdog Crawler** (`scrapingdog_crawler.py`):
   - Alternative crawler using Scrapingdog API service
   - Handles pagination to retrieve up to 100 results
   - Optimizes API usage by stopping when target domain is found

5. **Apify Crawler** (`apify_crawler.py`):
   - Alternative crawler using Apify's Google Search Scraper actor
   - Requires APIFY_API_TOKEN environment variable

#### Utilities
6. **Configuration** (`config.py`):
   - Central configuration for regions, API keys, delays, and output settings
   - Region definitions with language and domain mappings
   - Default values for all crawlers

7. **Keyword Management** (`keywords_manager.py`):
   - Handles reading and processing keyword CSV files
   - Expected format: CSV with 'keyword' and 'domain' columns
   - Supports UTF-8 encoding

8. **Rank Analysis** (`rank_analyzer.py`):
   - Analyzes and reports ranking results
   - Processes CSV files from results folder
   - Generates summary statistics

### Data Flow

#### GUI Flow
1. User configures settings in GUI (API method, regions, domain, etc.)
2. Settings auto-saved to `gui_settings.json`
3. User clicks "Start Search"
4. GUI runs selected crawler in background thread
5. Real-time progress displayed in log window
6. Results saved to `results/` folder with timestamp
7. Completion message shows result file path

#### CLI Flow
1. User selects options from interactive menu
2. Keywords loaded from CSV file (default: `keywords.csv`)
3. Crawler searches each keyword in specified regions
4. Progress displayed in terminal
5. Results saved to `results/` folder with timestamp
6. Analysis tools can process result files for reporting

#### Direct Script Flow
1. Script called with command-line arguments
2. Keywords loaded from specified CSV file
3. Crawler executes searches
4. Results written to CSV in `results/` folder

## Key Configuration

### API Keys
- SERP API: Set in `config.py` as `SERPAPI_KEY` or pass via command line
- Scrapingdog API: Set in `config.py` as `SCRAPINGDOG_API_KEY`
- Apify: Set as environment variable `APIFY_API_TOKEN`

### Region Configuration
```python
ALL_REGIONS = {
    'US': {'lang': 'en', 'country': 'us', 'domain': 'google.com'},
    'TW': {'lang': 'zh-TW', 'country': 'tw', 'domain': 'google.com.tw'},
    'HK': {'lang': 'zh-TW', 'country': 'hk', 'domain': 'google.com.hk'}
}
```

### Command Line Options

#### serp_api_crawler.py
```bash
python serp_api_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY
```
- `--regions`: Regions to search (US, TW, HK)
- `--domain`: Target domain to track
- `--keywords_file`: Path to keywords CSV file
- `--api_key`: SERP API key

#### scrapingdog_crawler.py
```bash
python scrapingdog_crawler.py --regions US TW --domain example.com --keywords_file keywords.csv --api_key YOUR_KEY
```
- Similar options to SERP API crawler
- `--delay`: Delay between requests (default: 5 seconds)

#### apify_crawler.py
```bash
python apify_crawler.py
```
- Requires APIFY_API_TOKEN environment variable
- Configuration in config.py

## Output Format
Results are saved as CSV files in the `results/` folder with columns:
- `keyword`: Search keyword
- `region`: Search region (US, TW, or HK)
- `rank`: Position in search results (1-100, -1 if not found, -2 if error)
- `url`: Found URL
- `title`: Page title
- `snippet`: Search result snippet

## Files Generated
- **Results**: `results/serp_results_YYYYMMDD_HHMMSS.csv`
- **GUI Settings**: `gui_settings.json` (auto-saved GUI configuration)
- **Keywords**: `keywords.csv` (input file with keyword/domain pairs)

## Development Notes

### Adding New Regions
Add to `config.py` in `ALL_REGIONS` dictionary:
```python
'XX': {'lang': 'xx', 'country': 'xx', 'domain': 'google.xx'}
```

### Modifying GUI
- Main GUI code: `gui_app.py`
- Uses tkinter with ttk styling
- Threading for non-blocking operations
- Settings persisted to JSON

### Testing New Features
1. Add tests to `tests/` folder
2. Run `run_test.bat` to execute all tests
3. Test individual crawlers with their respective test files