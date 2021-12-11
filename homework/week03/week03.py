import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

tr_tags = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for tr_tag in tr_tags:
    try:
        rank_tag = tr_tag.select_one('.list > td.number')
        title_tag = tr_tag.select_one('td.info > a.title.ellipsis')
        singer_tag = tr_tag.select_one('td.info > a.artist.ellipsis')
        rank_tag = str(rank_tag)
        rank_tag = rank_tag[19:22].strip()
        print(rank_tag, title_tag.text.strip(), singer_tag.text.strip())
        doc = {
            'rank': rank_tag,
            'title': title_tag.text.strip(),
            'singer': singer_tag.text.strip()
        }
        db.genie.insert_one(doc)
    except:
        pass
