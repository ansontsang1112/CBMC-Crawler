import datetime
import json
import os
import crawler as c
import schedule
import time

if __name__ == '__main__':
    try:
        open("articles/articles.json")
        print("File attempted successfully")
    except FileNotFoundError:
        print("Generating File")

    # Get article from crawler in every 00:00
    schedule.every().day.at("00:00").do(c.crawler)

    while True:
        print(f"靠北麥塊爬蟲系統運作正常 | 現在時間為 {datetime.datetime.now()}")
        schedule.run_pending()
        time.sleep(3600)
