import os
import sys

import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

from redis.commands.json.path import Path

import main
import connection as c

url_patten = "https://cbmc.club/posts/"


def crawler():
    if main.ENABLE_REDIS:
        client = c.redis_init()

        if client is not None:
            print("靠北麥塊爬蟲系統 | 已經連接 REDIS")
        else:
            print("靠北麥塊爬蟲系統 | REDIS 出現故障")

    # Get article count
    dir_path = "articles"
    init_count = 1
    exception_post, articles = [], {}

    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            init_count += 1

    count = init_count

    exception_post = fetch_all_empty(count)

    while True:
        if count not in exception_post:
            # 進度條
            print("\r", end="")
            print("靠北麥塊爬蟲系統 | 下載量: {} 篇文章 | ".format(count), "▓" * (count // 10), end="")
            sys.stdout.flush()

            page = fetch_page(count)
            if page == 0:
                break
            articles[count] = page

            if main.ENABLE_REDIS and client is not None:
                client.hset(count, "content", page.get("content"))
                client.hset(count, "img", page.get("img"))
        count += 1

    print("\n靠北麥塊爬蟲系統 | All article fetched successfully")

    file_name = "articles.json"
    with open(dir_path + "/" + file_name, 'w') as json_file:
        json.dump(articles, json_file)

    if main.ENABLE_REDIS and client is not None:
        print("靠北麥塊爬蟲系統 | 已將所有文章儲存到 articles.json 及 REDIS")
    else:
        print("靠北麥塊爬蟲系統 | 已將所有文章儲存到 articles.json")


def fetch_page(post_number: int):
    url = url_patten + str(post_number)
    web_page = requests.get(url).text

    soup = BeautifulSoup(web_page, 'html.parser')
    tag_content_search = soup.find("meta", property="og:description")

    formatted_content = str(tag_content_search).replace('<meta content="靠北麥塊 » cbmc.club › 檢視文章 • ', '').replace(
        '" property="og:description"/>', '')

    if stop_code(formatted_content):
        return 0

    try:
        img = str(soup.find_all("img", class_="image_max_width")[1]).split(" ")[2].replace('src="', '').replace('"/>','')
    except IndexError:
        img = "None"

    return {"content": formatted_content, "img": img}


def stop_code(content: str):
    if "無此文章" in content:
        return True
    else:
        return False


def fetch_all_empty(count: int):
    init, continuous_null, exception_posts = count, 0, []
    while True:

        print("\r", end="")
        print("靠北麥塊爬蟲系統 | 正在讀取文章數目: {} 索引 | ".format(init), "▓" * (init // 10), end="")
        sys.stdout.flush()

        if fetch_page(init) == 0:
            exception_posts.append(init)
            continuous_null += 1
        else:
            continuous_null = 0

        if continuous_null == 25:
            break

        init += 1

    exception_posts.append(datetime.now().strftime("%d/%m/%Y"))
    with open("exception_post.json", 'w') as json_file:
        json.dump(exception_posts, json_file)
    print("\n靠北麥塊爬蟲系統 | Exception List Updated.")
    return exception_posts
