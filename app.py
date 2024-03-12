import os
import pymongo

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
        if 'userid' in session:
            return render_template("loginpage.html", userid=session.get('userid'), login=False)
        else:
            return render_template("loginpage.html", login=False)


@app.route("/login", methods=["GET"])
def login():
    _id_ = request.args.get("id")
    _pw_ = request.args.get("pw")
    _mem_ = request.args.get("mem")

    if _mem_ == 'on':
        session['userid'] = _id_
    else:
        session.pop('userid')

    _cursor_ = _DB_.find_one({"user_id": _id_, "user_pw": _pw_})

    if _cursor_:
        session['username'] = _cursor_.get("user_name")
        return redirect(url_for("loginpage"))
    else:
        return redirect(url_for("loginpage"))


@app.route("/logout")
def logout():
    session.pop('username')
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
        _DB_.insert_one({"user_id": _id_, "user_pw": _pw_, "user_name": _name_, "user_team": "1팀"})
        session['username'] = _name_
        return redirect(url_for("loginpage"))
    
    
# main 상단

@app.route("/insert")
def insert():
    jungler = {
        'id_num':2, 'user_id':"test", 'user_pw':"test", 'user_name':"안태리", 'user_team':"1팀", 'user_place':"407 강의실"
    }
    _DB_.insert_one(jungler)
    return jsonify({'result':"success"})

@app.route("/main")
def main():
    # myInfo = _DB_.find({"id_num":int(id_num)}, {'_id':0})
    junglers = list(_DB_.find({}, {'_id':0}))
    return render_template('main.html', junglers=junglers)

@app.route("/update/team", methods=["POST"])
def updateTeam():
    id_num = request.form["id_num"]
    user_team = request.form["user_team"]
    _DB_.update_one({"id_num":int(id_num)}, {"$set":{"user_team":user_team}})
    return jsonify({"result":"success"})

@app.route("/update/place", methods=["POST"])
def updatePlace():
    id_num = request.form["id_num"]
    user_place = request.form["user_place"]
    _DB_.update_one({"id_num":int(id_num)}, {"$set":{"user_place":user_place}})
    return jsonify({"result":"success"})
    
# toDo 조회 검색어

@app.route("/search/name/<name>", methods=["GET"])
def searchByName(name):
    result = list(_DB_.find({"user_name": name}, {'_id':0}))
    return jsonify({'result':'success', 'junglers': result})

@app.route("/search/team/<team>", methods=["GET"])
def searchByTeam(team):
    result = list(_DB_.find({"user_team": team}, {'_id':0}))
    return jsonify({'result':'success', 'junglers': result})

@app.route("/search/place/<place>", methods=["GET"])
def searchByPlace(place):
    result = list(_DB_.find({"user_place": place}, {'_id':0}))
    return jsonify({'result':'success', 'junglers': result})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)