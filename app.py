import os
import pymongo
import hashlib

from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(verbose=True)

# DB 설정
_PATH_ = os.getenv('MONGO_DB_PATH')
_DB_ = pymongo.MongoClient(_PATH_).week00_junglerDongsun.junglers
_DB_CATEGORY = pymongo.MongoClient(_PATH_).week00_junglerDongsun.category

# Flask 키 설정
_KEY_ = os.getenv('KEY')
app = Flask(__name__)
app.secret_key = _KEY_


# 로그인 동작부.

@app.route("/login", methods=["POST"])
def login():
    _id_ = request.form["id"]
    _pw_ = request.form["pw"]

    if "mem" in request.form:
        session['memorize'] = _id_
    elif 'memorize' in session:
        session.pop('memorize')

    # 비밀번호 해시
    _HASH_ = hashlib.sha256()
    _HASH_.update(str(_pw_).encode('utf-8'))
    _PASS_ = _HASH_.hexdigest()

    _cursor_ = _DB_.find_one({"user_id": _id_, "user_pw": _PASS_})

    if _cursor_:
        session['userID'] = _id_
        return redirect(url_for("loginpage"))
    else:
        session['notAllowed'] = 'true'
        return redirect(url_for("loginpage"))


@app.route("/logout")
def logout():
    session.pop('userID')
    return redirect(url_for("loginpage"))


@app.route("/checkid", methods=["POST"])
def checkid():
    id_confirm = request.form['id']

    _cursor_ = _DB_.find_one({"user_id": id_confirm})

    if _cursor_:
        return jsonify({'result': 'stop'})
    else:
        return jsonify({'result': 'good'})


@app.route("/signup", methods=["POST"])
def signup():
    _id_ = request.form['id']
    _pw_ = request.form['pw']
    _name_ = request.form['name']
    _photo_ = request.files['photo']

    _cursor_ = _DB_.find_one({"user_id": _id_})

    if _cursor_:
        return jsonify({'message': '이미 사용 중인 아이디 입니다.'})
    else:
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
        filename = f'file-{mytime}'

        # 확장자 나누기
        extension = _photo_.filename.split('.')[-1]
        # static 폴더에 저장
        save_to = f'static/{filename}.{extension}'
        _photo_.save(save_to)

        # 비밀번호 해시
        _HASH_ = hashlib.sha256()
        _HASH_.update(str(_pw_).encode('utf-8'))
        _PASS_ = _HASH_.hexdigest()

        _DB_.insert_one({"user_id": _id_, "user_pw": _PASS_, "user_name": _name_, "user_team": "1팀",
                         "user_place": "비공개", "user_photo": f'{filename}.{extension}', "$currentDate":
                             {"update_time": True}})

        return redirect(url_for("loginpage"))


@app.route('/')
def loginpage():
    if 'userID' in session:
        return redirect(url_for("main"))
    else:
        if 'notAllowed' in session:
            _Error000_ = session.pop('notAllowed')
        else:
            _Error000_ = 'false'

        if 'memorize' in session:
            return render_template("loginpage.html", userID=session.get('memorize'), login_failure=_Error000_)
        else:
            return render_template("loginpage.html", login_failure=_Error000_)

# main 상단


# @app.route("/insert")
# def insert():
#     for i in range(1, 13):
#         tem = {
#             'team': str(i)+"팀",
#             'index': int(i)
#         }
#         _DB_CATEGORY.insert_one(tem)
#     cnt = 1
#     place = {"기숙사", "식당", "L401호", "L403호", "L405호", "L407호", "휴게실", "체력단련실", "교외", "비공개"}
#     for i in place:
#         tem = {
#             'place': str(i),
#             'index': cnt
#         }
#         _DB_CATEGORY.insert_one(tem)
#         cnt += 1
#     return jsonify({'result': "success"})


@app.route("/main")
def main():
    if 'userID' in session:
        user_id = session.get('userID')
        myinfo = _DB_.find_one({"user_id": user_id}, {'_id': 0, 'pw': 0})
        category = list(_DB_CATEGORY.find({}, {'_id': 0}).sort({'index': 1}))

        return render_template('main.html', myInfo=myinfo, category=category)
    else:
        return redirect(url_for('loginpage'))


@app.route("/update/team", methods=["POST"])
def update_team():
    user_id = request.form["user_id"]
    user_team = request.form["user_team"]
    _DB_.update_one({"user_id": user_id}, {"$set": {"user_team": user_team}, "$currentDate": {"update_time": True}})
    return jsonify({"result": "success"})


@app.route("/update/place", methods=["POST"])
def update_place():
    user_id = request.form["user_id"]
    user_place = request.form["user_place"]
    _DB_.update_one({"user_id": user_id}, {"$set": {"user_place": user_place}, "$currentDate": {"update_time": True}})
    return jsonify({"result": "success"})


# 조회 검색어

@app.route("/search/list/all", methods=["GET"])
def listing():
    junglers = list(_DB_.find({}, {'_id': 0, 'user_pw': 0}))

    return jsonify({'result': 'success', 'junglers': junglers})


@app.route("/search/name/<name>", methods=["GET"])
def search_by_name(name):
    result = list(_DB_.find({"user_name": {'$regex': name}}, {'_id': 0, 'user_pw': 0}))

    return jsonify({'result': 'success', 'junglers': result})


@app.route("/search/team/<team>", methods=["GET"])
def search_by_team(team):
    result = list(_DB_.find({"user_team": {'$regex': team}}, {'_id': 0, 'user_pw': 0}))

    return jsonify({'result': 'success', 'junglers': result})


@app.route("/search/place/<place>", methods=["GET"])
def search_by_place(place):
    result = list(_DB_.find({"user_place": {'$regex': place}}, {'_id': 0, 'user_pw': 0}))

    return jsonify({'result': 'success', 'junglers': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
