from flask import Flask, render_template, jsonify, request, session, url_for, redirect
app = Flask(__name__)
app.secret_key = "#rkawkclqdmsaktdlTDj"

ID = "admin"
PW = "admin!"
users = ['user1', 'user2', 'user3']

@app.route('/')
def loginpage():
    if 'userID' in session:
        return render_template("index.html", username=session.get('userID'), login=True)
    else:
        return render_template("loginpage.html", login=False)


@app.route("/login", methods=["get"])
def login():
    global ID, PW
    _id_ = request.args.get("id")
    _pw_ = request.args.get("pw")

    if ID == _id_ and PW == _pw_:
        session['userID'] = _id_
        return redirect(url_for("loginpage"))
    else:
        return redirect(url_for("loginpage"))

@app.route("/logout")
def logout():
    session.pop('userID')
    return redirect(url_for("loginpage"))

@app.route("/checkid", methods=["get"])
def checkid():
    id_confirm = request.form['id']

    if id_confirm in users:
        return jsonify({'status': 'error', 'message': '이미 사용 중인 아이디 입니다.'})
    else:
        return jsonify({'status': 'success', 'message': '사용 가능한 아이디 입니다.'})


@app.route("/signup", methods = ["post"])
def signup():
    _id_ = request.form['id']
    _pw_ = request.form['pw']
    _name_ = request.form['name']

    if _id_ in users:
        return jsonify({'status': 'error', 'message': '이미 사용 중인 아이디 입니다.'})
    else:
        users.append(_id_)
        session['userID'] = _id_
        return redirect(url_for("loginpage"))


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)