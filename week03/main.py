import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sparta

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200716',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

tr_tags = soup.select('#old_content > table > tbody > tr')

# for tr_tag in tr_tags:
#     rank_tag = tr_tag.select_one('td.ac > img')
#     if rank_tag is not None:
#         rank = rank_tag['alt']  #어트리뷰트는 다 딕셔너리로
#     else:
#         rank = None
#     title_tag = tr_tag.select_one('td.title > div > a')
#     if title_tag is not None:
#         title = title_tag.text
#     else:
#         title = None
#     print(rank, title)

for tr_tag in tr_tags:
    try:
        rank_tag = tr_tag.select_one('td.ac > img')  #td.ac가 많기 때문에 제일 처음걸 선택
        rank = int(rank_tag['alt'])
        title_tag = tr_tag.select_one('td.title > div > a')
        print(title_tag)
        title = title_tag.text
        point_tag = tr_tag.select_one('td.point')
        point = point_tag.text
        doc = {   #이렇게 만들어주는게 더 편하다.
            'title': title,
            'rank': rank,
            'point': point
        }
        db.movies.insert_one(doc)
    except:
        pass
