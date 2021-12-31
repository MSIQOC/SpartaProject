from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request, url_for, redirect

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.boyfriends


# HTML 화면 보여주기
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('favorite.html')


@app.route('/add', methods=['GET','POST'])
def add():
    return render_template('add.html')


# 여기서부터 파이몽고 활용
# 새로운 남자친구 추가
@app.route('/adding', methods=['POST'])
def adding():
    form = request.form
    name = form['name']
    personality = form['personality']
    age = form['age']
    hobby = form['hobby']
    blood_type = form['bloodType']

    db.boyfriends.insert_one({
        'name': name,
        'personality': personality,
        'age': age,
        'hobby': hobby,
        'blood_type': blood_type,
        'like': 0
    })

    return jsonify({'result': 'success', 'msg': '추가가 완료됐습니다!'})


@app.route('/api/list', methods=['GET'])
def show_boyfriends():
    boyfriends_list = list(db.boyfriends.find({}, {'_id': False}).sort('like', -1))
    return jsonify({
        'result': 'success', 'msg': 'hello',
        'boyfriends_list': boyfriends_list
    })


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)