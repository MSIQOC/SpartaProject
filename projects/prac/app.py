from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def get_index():  # put application's code here
    return render_template('index.html', welcome_message='반갑습니다')
# 프론트쪽에서 {{ welcome_message }}라고 쓰고 서버쪽에서 welcome_message='반갑습니다'라고 쓰면 변수를 넘겨주는거가 된다.


@app.get('/test') #/test인데 get으로 받고싶은 경우에는 app.get으로 쓴다.
def get_test():
    args = request.args
    title = args['title']
    print(title)
    print(args) #args는 url에 /test?title=happy&day=friday&hello=hi 이런식 받는 것이다. 주소창에 직접 쓰는 행위는 get 행위와 같다.
    return jsonify({
        'result': 'success'
    })


@app.post('/test')
def post_test(): #post랑 get은 행위는 같다. 하지만 post는 request나 ajax로 해야한다.
    form = request.form
    title = form['title'] #get을 쓰는 것과 []를 쓰는 것과 같지만 []를 쓰면 에러 발견이 쉽다.
    print(title)
    print(form)
    return jsonify({
        'result': 'success'
    })


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000) #app.run 안에 이렇게 써주면 계속 리프레쉬 안해줘도 된다.
