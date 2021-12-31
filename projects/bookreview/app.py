from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.sparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.post('/review')
def write_review():
    # 1. 클라이언트가 준 title, author, review 가져오기.
    form = request.form  # form으로 받아온다.
    title = form['title']
    author = form['author']
    bookReview = form['bookReview']
    # 2. DB에 정보 삽입하기
    db.reviews.insert_one({
        'title': title,
        'author': author,
        'bookReview': bookReview
    })
    # 3. 성공 여부 & 성공 메시지 반환하기
    print(title, author, bookReview)
    return jsonify({'result': 'success', 'msg': '저장에 성공했습니다!'})


@app.get('/review')
def read_reviews():
    reviews = list(db.reviews.find({}, {'_id': False})) #list로 묶어서 메모리 위에 올려준다.
    return jsonify({
        'result': 'success',
        'reviews': reviews  #위에 reviews를 집어넣는 느낌으로
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
