import datetime
import json
import os
import crawler as c
import schedule as s
import time
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')
ENABLE_REDIS = os.getenv('ENABLE_REDIS')

if __name__ == '__main__':
    try:
        open("articles/articles.json")
        print("靠北麥塊爬蟲系統 | File attempted successfully")
    except FileNotFoundError:
        print("靠北麥塊爬蟲系統 | Generating File")

    print("靠北麥塊爬蟲系統 | 正在初始化")
    c.crawler()

    # Get article from crawler in every 00:00
    s.every().day.at("00:00").do(c.crawler)

    while True:
        print(f"靠北麥塊爬蟲系統運作正常 | 現在時間為 {datetime.datetime.now()}")

        f = open("hc.log", "a")
        f.write(f"{datetime.datetime.now()} | I am still alive\n")
        f.close()

        s.run_pending()
        time.sleep(3600)
