from flask import Flask, render_template, jsonify, request
import requests
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = Flask(__name__)

# .env 파일로부터 환경 변수 로드
load_dotenv()

client = MongoClient(os.environ.get("MONGO_DB_PATH"))
db = client.week00_junglerDongsun.junglers # cluster0 > week00_junglerDongsun > junglers 컬렉션(유저)



@app.route("/insert")
def insert():
    jungler = {
        'id_num':2, 'user_id':"test", 'user_pw':"test", 'user_name':"안태리", 'user_team':"1팀", 'user_place':"407 강의실"
    }
    db.insert_one(jungler)
    return jsonify({'result':"success"})

@app.route("/main")
def main():
    # myInfo = db.find({"id_num":int(id_num)}, {'_id':0})
    junglers = list(db.find({}, {'_id':0}))
    return render_template('main.html', junglers=junglers)

@app.route("/update/team", methods=["POST"])
def updateTeam():
    id_num = request.form["id_num"]
    user_team = request.form["user_team"]
    db.update_one({"id_num":int(id_num)}, {"$set":{"user_team":user_team}})
    return jsonify({"result":"success"})

@app.route("/update/place", methods=["POST"])
def updatePlace():
    id_num = request.form["id_num"]
    user_place = request.form["user_place"]
    db.update_one({"id_num":int(id_num)}, {"$set":{"user_place":user_place}})
    return jsonify({"result":"success"})

# toDo 로그인 기능


# toDo 메인화면 기능




if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=False)
