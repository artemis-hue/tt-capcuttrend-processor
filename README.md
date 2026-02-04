# TikTok Trend System - GitHub Automation

**Version:** 5.3.0  
**Status:** Production Ready - All Bugs Fixed

## What This Does

Automated daily processing of TikTok trend data:
- Fetches data from Apify API (US + UK markets)
- Calculates momentum scores and 24h tracking
- Detects YOUR posts and competitor posts
- Generates BUILD files with tutorial triggers
- Sends Discord notifications

## Setup

### 1. Create Repository
Upload all files maintaining the folder structure.

### 2. Add GitHub Secrets
Go to: Settings → Secrets and variables → Actions → New repository secret

| Secret | Required | Description |
|--------|----------|-------------|
| `APIFY_TOKEN` | ✅ | Your Apify API token |
| `US_VIDEO_TASK_ID` | ✅ | US video scraper task ID |
| `UK_VIDEO_TASK_ID` | ✅ | UK video scraper task ID |
| `US_MUSIC_TASK_ID` | ❌ | US music task (optional) |
| `UK_MUSIC_TASK_ID` | ❌ | UK music task (optional) |
| `DISCORD_WEBHOOK` | ✅ | Discord webhook URL |

### 3. Run Workflow
- **Automatic:** Runs daily at 9am UTC
- **Manual:** Actions → Daily Processing → Run workflow

### 4. Download Output
- Go to Actions → Select run → Scroll to Artifacts
- Download `tiktok-output-X`

## Files Generated

- `BUILD_TODAY_TOP20_YYYY-MM-DD.xlsx` - Top 20 trends
- `BUILD_TODAY_TOP100_YYYY-MM-DD.xlsx` - Top 100 trends
- `TikTok_Trend_System_US_YYYY-MM-DD.xlsx` - Full US data
- `TikTok_Trend_System_UK_YYYY-MM-DD.xlsx` - Full UK data
- `SUMMARY_REPORT_YYYY-MM-DD.txt` - Text summary

## Version 5.3.0 Fixes

1. ✅ YOUR posts from ALL processed data (not just 72h fresh)
2. ✅ Competitor count from ALL processed data
3. ✅ Trigger counts (URGENT/HIGH/WATCH) from ALL data
4. ✅ MY_PERFORMANCE keeps duplicates for BOTH market posts
5. ✅ AUDIO sheets properly populated
6. ✅ START_HERE full summary with all stats
7. ✅ Tab order fixed (UK together, US together)
8. ✅ Cache persistence between runs (actions/cache)

## Expected Output

After 2+ runs:
- **Your Posts:** 20-40 (depending on posting activity)
- **Competitor Posts:** 20-30
- **URGENT/HIGH/WATCH:** Non-zero counts
- **SPIKING:** Should show if momentum increasing
- **Status diversity:** NEW, SPIKING, RISING, COOLING, DYING
