from flask import Flask, render_template, requests
import requests
from pymongo import MongoClient
from bson import ObjecId # 몽고디비id객체를 문자열로 변환, 스트링값을 id 객체로 변환해주는 기능

app = Flask(__name__)

'''
예시
@app.route('/ex')
def index():
    title = "Welcome to My Website"
    user = {'username': 'Guest', 'is_authenticated': False}
    items = ['item1', 'item2', 'item3']
    today_date = '2024-03-11'
    return render_template('index.html', title=title, user=user, items=items, today_date=today_date)
'''

# toDo 로그인 기능


# toDo 메인화면 기능




if __name__ == '__main__':
    app.run(debug=True)