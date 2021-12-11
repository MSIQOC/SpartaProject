import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://sports.news.naver.com/kbaseball/record/index.nhn?category=kbo',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

tr_tags = soup.select('#regularTeamRecordList_table > tr') #tr들을 불러오고

for tr_tag in tr_tags:
    try:
        rank_tag = tr_tag.select_one('th > strong')
        name_tag = tr_tag.select_one('td.tm > div > span')
        point_tag = tr_tag.select_one('td:nth-child(7) > strong')
        print(rank_tag.text, name_tag.text, point_tag.text)
    except:
        pass
