from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request, url_for, redirect

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.boyfriends


# HTML 화면 보여주기
@app.get('/')
def home():
    return render_template('favorite.html')


@app.get('/add')
def add():
    return render_template('add.html')


@app.get('/chats')
def chat():
    return render_template('chatting.html')


@app.post('/findchat')
def findchat():
    form = request.form
    val = form['_val']
    name = form['name']
    boyfriend = list(db.chats.find({
        'name': name,
        'question': val
    }, {'_id': False}))
    if not boyfriend:
        return jsonify({
            'result': 'failed'
        })
    return jsonify({
        'result': 'success',
        'chat': boyfriend
    })

@app.post('/addchat')
def addchat():
    form = request.form
    question = form['question']
    answer = form['answer']
    name = form['name']
    db.chats.insert_one({
        'name': name,
        'question': question,
        'answer': answer
    })
    return jsonify({'msg': '저장성공!'})

# 여기서부터 파이몽고 활용
# 새로운 남자친구 추가
@app.post('/adding')
def adding():
    form = request.form
    name = form['name']
    personality = form['personality']
    age = form['age']
    hobby = form['hobby']
    blood_type = form['bloodType']

    boyfriend = db.boyfriends.find_one({'name': name})
    if boyfriend:
        return jsonify({'result':'failed', 'msg': '다른 남자친구 이름으로 써주세요!'})
    else:
        db.boyfriends.insert_one({
            'name': name,
            'personality': personality,
            'age': age,
            'hobby': hobby,
            'blood_type': blood_type,
            'like': 0
        })

    return jsonify({'result': 'success', 'msg': '추가가 완료됐습니다!'})


@app.get('/api/list')
def show_boyfriends():
    boyfriends_list = list(db.boyfriends.find({}, {'_id': False}).sort('like', -1))
    return jsonify({
        'result': 'success', 'msg': 'hello',
        'boyfriends_list': boyfriends_list
    })

@app.post('/api/like')
def like_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name = request.form['name'] #클라이언트가 보내줬다고 가정(index.html에서 data에 name을 넘겨준다.)

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    star = db.mystar.find_one({'name': name}) #find_one으로 하면 list로 감쌀 필요가 없다.

    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = star['like'] + 1

    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.mystar.update_one({'name': name}, {'$inc': {'like': 1}}) #이렇게 해주는게 더 안전하게 올려줄 수 있다.

    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': name + '좋아요!'})


@app.post('/api/delete')
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name = request.form['name']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.boyfriends.delete_one({'name': name})
    db.chats.delete_many({'name': name})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': '삭제가 완료됐습니다.'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)