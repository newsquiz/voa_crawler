from selenium.webdriver import Chrome, ChromeOptions
import time
import os
import subprocess
from post_process import post_process
import youtube_dl
import json
import glob
import shutil


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def download(yt_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])


def main():
    data = 'data.json'
    try:
        os.remove(data)
    except:
        pass
    subprocess.call(['scrapy', 'runspider', 'scrapy/crawler/spiders/quotes_spider.py', '-o', data])
    post_process(data)
    with open(data, 'r') as fn:
        data = json.loads(fn.read())
    new_data = []
    for item in data:
        download(item['url'])
        new_item = {
            'content': item['content'],
            'title': item['title'],
            'thumbnail': item['thumbnail'],
            'audio': os.path.join('data', glob.glob('*.mp3')[0]),
            'type': 'audio'
        }
        shutil.move(glob.glob('*.mp3')[0], 'data')


if __name__ == '__main__':
    main()
