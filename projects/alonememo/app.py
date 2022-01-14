from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('mongodb://test:test@localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.sparta  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.post('/memo')
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    form = request.form
    url = form['url']  #클라이언트에 url, comment라고 써놨기 때문에 이렇게 해준다.
    comment = form['comment']
    print(url, comment)


    # 2. meta tag를 스크래핑하기
    resp = requests.get(url) #이렇게 url을 가져오는 것이다.
    soup = BeautifulSoup(resp.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']
    print(url, comment, image, title, desc)

    # 3. mongoDB에 데이터 넣기
    db.memos.insert_one({
        'url': url,
        'comment': comment,
        'image': image,
        'title': title,
        'desc': desc
    })

    return jsonify({'result': 'success', 'msg': '저장됐습니다!'})


@app.get('/memo')
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기(Read)
    memos = list(db.memos.find({}, {'_id': False}))
    # 2. articles라는 키 값으로 articles 정보 보내주기
    print(memos)
    return jsonify({  #json으로 정보들 넘겨주기
        'result': 'success',
        'memos': memos
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)