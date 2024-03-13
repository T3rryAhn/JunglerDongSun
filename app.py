import os
import pymongo

from flask import Flask, render_template, jsonify, request, session, url_for, redirect
from dotenv import load_dotenv


load_dotenv(verbose=True)
_PATH_ = os.getenv('MONGO_DB_PATH')
_KEY_ = os.getenv('KEY')
_DB_ = pymongo.MongoClient(_PATH_).week00_junglerDongsun.junglers
_DB_CATEGORY = pymongo.MongoClient(_PATH_).week00_junglerDongsun.category

app = Flask(__name__)
app.secret_key = _KEY_


# 로그인 동작부
@app.route('/')
def loginpage():
    if 'userInfo' in session:
        return redirect(url_for(main))
    else:
        if '_memorize_' in session:
            return render_template("loginpage.html", userID=session.get('_memorize_'), login=False)
        else:
            return render_template("loginpage.html", login=False)


@app.route("/login", methods=["POST"])
def login():
    _id_ = request.form["id"]
    _pw_ = request.form["pw"]

    if "mem" in request.form:
        session['_memorize_'] = _id_
    elif '_memorize_' in session:
        session.pop('_memorize_')

    _cursor_ = _DB_.find_one({"user_id": _id_, "user_pw": _pw_})

    if _cursor_:
        session['userInfo'] = []

        session['userInfo'].append(_cursor_["user_id"])
        session['userInfo'].append(_cursor_["user_name"])
        session['userInfo'].append(_cursor_["user_team"])
        session['userInfo'].append(_cursor_["user_place"])

        return redirect(url_for("loginpage"))
    else:
        return redirect(url_for("loginpage"))


@app.route("/logout")
def logout():
    session.pop('userInfo')
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

    _cursor_ = _DB_.find_one({"user_id": _id_})

    if _cursor_:
        return jsonify({'message': '이미 사용 중인 아이디 입니다.'})
    else:
        _DB_.insert_one({"user_id": _id_, "user_pw": _pw_, "user_name": _name_, "user_team": "1팀", "user_place": "비공개"})
        session['username'] = _name_
        return redirect(url_for("loginpage"))


# main 상단

@app.route("/insert")
def insert():
    for i in range(1, 13):
        tem = {
            'team':str(i)+"팀",
            'index':int(i)
        }
        _DB_CATEGORY.insert_one(tem)
    cnt = 1
    place = {"기숙사", "식당", "L401", "L403", "L405", "L407", "휴게실", "체력단련실", "교외", "비공개"}
    for i in place:
        tem = {
            'place':str(i),
            'index':cnt
        }
        _DB_CATEGORY.insert_one(tem)
        cnt+=1
    return jsonify({'result':"success"})

@app.route("/main")
def main():
    user_id = session.get('userID')
    myInfo = _DB_.find_one({"user_id":user_id}, {'_id':0, 'pw':0})
    category = list(_DB_CATEGORY.find({}, {'_id':0}).sort({'index': 1}))
    return render_template('main.html', myInfo = myInfo, category = category, login=True)

@app.route("/update/team", methods=["POST"])
def updateTeam():
    user_id = request.form["user_id"]
    user_team = request.form["user_team"]
    _DB_.update_one({"user_id":user_id}, {"$set":{"user_team":user_team}})
    return jsonify({"result":"success"})

@app.route("/update/place", methods=["POST"])
def updatePlace():
    user_id = request.form["user_id"]
    user_place = request.form["user_place"]
    _DB_.update_one({"user_id":user_id}, {"$set":{"user_place":user_place}})
    return jsonify({"result":"success"})


# 조회 검색어

@app.route("/search/list/all", methods=["GET"])
def listing():
    junglers = list(_DB_.find({}, {'_id':0}))
    return jsonify({'result':'success', 'junglers': junglers})

@app.route("/search/name/<name>", methods=["GET"])
def searchByName(name):
    result = list(_DB_.find({"user_name": { '$regex': name }}, {'_id': 0}))
    return jsonify({'result': 'success', 'junglers': result})


@app.route("/search/team/<team>", methods=["GET"])
def searchByTeam(team):
    result = list(_DB_.find({"user_team": {'$regex': team}}, {'_id': 0}))
    return jsonify({'result': 'success', 'junglers': result})


@app.route("/search/place/<place>", methods=["GET"])
def searchByPlace(place):
    result = list(_DB_.find({"user_place": {'$regex': place}}, {'_id': 0}))
    return jsonify({'result': 'success', 'junglers': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
