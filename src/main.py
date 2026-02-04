#!/usr/bin/env python3
"""
TIKTOK AUTOMATION MAIN
Version: 5.3.0
"""

import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apify_fetcher import fetch_all_data
from daily_processor import process_data, load_yesterday_cache, save_today_cache, calculate_metrics
from discord_notify import send_discord_notification
import pandas as pd


def main():
    print("=" * 50)
    print("TikTok Daily Processor v5.3.0")
    print("=" * 50)
    
    # Directories
    output_dir = os.environ.get('OUTPUT_DIR', 'output')
    cache_dir = os.environ.get('CACHE_DIR', 'data')
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(cache_dir, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Cache directory: {cache_dir}")
    
    # Step 1: Fetch data from Apify
    print("\n[Step 1] Fetching data from Apify...")
    us_data, uk_data, us_music, uk_music = fetch_all_data()
    
    if not us_data and not uk_data:
        print("ERROR: No data fetched from Apify!")
        sys.exit(1)
    
    print(f"  US videos: {len(us_data) if us_data else 0}")
    print(f"  UK videos: {len(uk_data) if uk_data else 0}")
    print(f"  US music: {len(us_music) if us_music else 0}")
    print(f"  UK music: {len(uk_music) if uk_music else 0}")
    
    # Step 2: Load yesterday's cache
    print("\n[Step 2] Loading yesterday's cache...")
    yesterday_us, yesterday_uk = load_yesterday_cache(cache_dir)
    
    if yesterday_us and yesterday_uk:
        print(f"  Cache found! US: {len(yesterday_us)}, UK: {len(yesterday_uk)} records")
    else:
        print("  No cache found - all statuses will be NEW")
    
    # Step 3: Process data
    print("\n[Step 3] Processing data...")
    stats = process_data(
        us_data, uk_data, 
        us_music, uk_music,
        yesterday_us, yesterday_uk,
        output_dir, cache_dir
    )
    
    # Step 4: Save today's cache for tomorrow
    print("\n[Step 4] Saving cache for tomorrow...")
    # Need to recreate processed DataFrames for caching
    us_df = pd.DataFrame(us_data) if us_data else pd.DataFrame()
    uk_df = pd.DataFrame(uk_data) if uk_data else pd.DataFrame()
    
    if len(us_df) > 0:
        us_df = us_df.drop_duplicates(subset=['webVideoUrl'], keep='first')
        us_df = calculate_metrics(us_df)
    
    if len(uk_df) > 0:
        uk_df = uk_df.drop_duplicates(subset=['webVideoUrl'], keep='first')
        uk_df = calculate_metrics(uk_df)
    
    save_today_cache(us_df, uk_df, cache_dir)
    
    # Step 5: Send Discord notification
    print("\n[Step 5] Sending Discord notification...")
    send_discord_notification(stats)
    
    # Done
    print("\n" + "=" * 50)
    print("Processing complete!")
    print("=" * 50)
    
    # Print summary
    print(f"\nSummary:")
    print(f"  Your Posts: {stats.get('your_posts', 0)}")
    print(f"  Competitor Posts: {stats.get('competitor', 0)}")
    print(f"  🔥 URGENT: {stats.get('urgent', 0)}")
    print(f"  ⚡ HIGH: {stats.get('high', 0)}")
    print(f"  🟡 WATCH: {stats.get('watch', 0)}")
    print(f"  🚀 SPIKING: {stats.get('spiking', 0)}")


if __name__ == '__main__':
    main()
