import base64
import re
import sys
from random import seed, choice, randint, shuffle

import rethinkdb as r
from flask import Flask, render_template, request
from oath import accept_totp

try:
    import secrets
except:
    pass

DB = ("localhost" if __name__ == "__main__" else "db", 28015)
KEY = list(set(randint(0, 255) for _ in range(randint(50, 70))))
shuffle(KEY)

app = Flask(__name__)


@app.route("/")
def index():
    init()
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    init()
    global DB
    if request.method == 'POST':
        c = r.connect(*DB)
        login = request.form['login']
        token = request.form['token']
        try:
            user = r.db('totp').table('users').filter({'login': login}).run(c).next()
        except:
            return render_template('index.html', msg="User not found", type="danger")
        if check(token, user['key']):
            if user['login'] == "admin":
                try:
                    flag = secrets.flag
                except:
                    flag = "404 Flag Not Found"
                return render_template('index.html', msg="Hello, admin! Your flag is: {}".format(flag), type="success")
            else:
                return render_template('index.html', msg="Hello, {}!".format(user['login']), type="success", show_source=True)
        else:
            return render_template('index.html', msg="Invalid code!", type="danger")
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    init()
    if request.method == 'POST':
        login = request.form['login']
        if not re.match("^[a-zA-Z0-9]{3,20}$", login):
            return render_template('index.html', msg="Login should match ^[a-zA-Z0-9]{3,20}$", type="danger", register=True)
        result, key = insert_user(login)
        if result:
            return render_template('index.html',
                                   msg="Register success, please import key into your Google Authenticator", key=key, type="success")
        else:
            return render_template('index.html', msg="User already exists", type="danger", register=True)
    else:
        return render_template('index.html', register=True)


def insert_user(login):
    global DB
    key = gen_key(login)
    c = r.connect(*DB)
    result = r.db('totp') \
        .table('users') \
        .filter({'login': login}) \
        .is_empty() \
        .do(lambda empty: r.branch(empty,
                                   r.db('totp').table('users').insert({
                                       'login': login,
                                       'key': key}),
                                   False)) \
        .run(c)
    return bool(result), key


def gen_key(login):
    global KEY
    seed(int.from_bytes(login.encode(), 'little'))
    return base64.b32encode(bytearray([choice(KEY) for _ in range(20)])).decode()


def check(token, key):
    return accept_totp(base64.b32decode(key).hex(), token)[0]

def init():
    global DB, KEY
    c = r.connect(*DB)
    try:
        r.db_create("totp").run(c)
        print('DB created')
    except:
        pass
    for t in ("users", "keys"):
        try:
            r.db("totp").table_create(t).run(c)
            print('Table {} created'.format(t))
        except:
            pass
    result = r.db('totp') \
        .table('keys') \
        .is_empty() \
        .do(lambda empty: r.branch(empty,
                                   r.db('totp').table('keys').insert({
                                       'key': KEY
                                   }),
                                   r.db('totp').table('keys').limit(1)
                                   )) \
        .run(c)
    try:
        KEY = result[0]['key']
        print('Key is {}'.format(KEY))
    except:
        pass
    insert_user("admin")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
