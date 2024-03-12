import os
import pymongo
import dotenv

from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from dotenv import load_dotenv

load_dotenv(verbose=True)
_PATH_ = os.getenv('MONGO_DB_PATH')
_KEY_ = os.getenv('KEY')
_DB_ = pymongo.MongoClient(_PATH_).week00_junglerDongsun.junglers

app = Flask(__name__)
app.secret_key = _KEY_

@app.route('/')
def loginpage():
    if 'username' in session:
        return render_template("index.html", username=session.get('username'), login=True)
    else:
        return render_template("loginpage.html", login=False)


@app.route("/login", methods=["get"])
def login():
    _id_ = request.args.get("id")
    _pw_ = request.args.get("pw")

    _cursor_ = _DB_.find_one({"id": _id_, "pw": _pw_})

    if _cursor_:
        session['username'] = _cursor_.get("name")
        return redirect(url_for("loginpage"))
    else:
        return redirect(url_for("loginpage"))

@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for("loginpage"))

@app.route("/checkid", methods=["get"])
def checkid():
    id_confirm = request.form['id']

    _cursor_ = _DB_.find({"id": id_confirm})

    if _cursor_:
        return jsonify({'status': 'error', 'message': '이미 사용 중인 아이디 입니다.'})
    else:
        return jsonify({'status': 'success', 'message': '사용 가능한 아이디 입니다.'})


@app.route("/signup", methods=["post"])
def signup():
    _id_ = request.form['id']
    _pw_ = request.form['pw']
    _name_ = request.form['name']

    _cursor_ = _DB_.find({"id": _id_})

    if _cursor_:
        return jsonify({'status': 'error', 'message': '이미 사용 중인 아이디 입니다.'})
    else:
        _DB_.insert_one({"id": _id_, "pw": _pw_, "name": _name_, "team": "1팀"})
        session['username'] = _name_
        return redirect(url_for("loginpage"))


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)