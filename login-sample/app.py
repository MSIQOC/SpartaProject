import functools

from flask import Flask, redirect, url_for, g, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from pymongo import MongoClient

app = Flask(__name__)
app.config.update(
    SECRET_KEY='SPARTA_SECRET_KEY'
)

client = MongoClient('localhost', 27017)
db = client.dbsparta


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('/login')

        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    g.user = None

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = db.users.find_one({
                'user_id': user_id
            })
        except:
            pass


@app.route('/')
def get_index():
    return render_template('index.html')


@app.get('/login')
def get_login():
    return render_template('login.html')


@app.post('/login')
def post_login():
    user_id = request.form['user_id']
    password = request.form['password']

    error = None

    user = db.users.find_one({
        'user_id': user_id
    })

    if user is None:
        error = 'Incorrect user id.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        session.clear()
        session['user_id'] = user['user_id']
        return redirect('/')

    return redirect('/login')


@app.get('/signup')
def get_signup():
    return render_template('signup.html')


@app.post('/signup')
def post_signup():
    user_id = request.form['user_id']
    username = request.form['username']
    password = request.form['password']

    error = None

    if not user_id:
        error = 'User ID is required.'
    elif not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'
    elif db.users.find_one({'user_id': user_id}) is not None:
        error = 'User {} is already registered.'.format(username)

    if error is None:
        user = {
            'user_id': user_id,
            'password': generate_password_hash(password),
            'username': username
        }

        db.users.insert_one(user)

        return redirect('/login')

    return redirect('/signup')


@app.get('/logout')
def get_logout():
    session.clear()
    return redirect('/')

@app.get('/upload')
@login_required
def get_upload():
    username = g.user['username']
    return render_template('upload.html', username=username)

@app.post('/upload')
@login_required
def post_upload():
    files = request.files
    form = request.form

    print(files, form)
    return redirect('/')


if __name__ == '__main__':
    app.run()
