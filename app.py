from flask import Flask, request, render_template, redirect, url_for
import pymysql as pms
import pickle
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

def db_connection():
    return pms.connect(host="localhost", 
                   port = 3306, 
                   user="root", 
                   password="mysql",
                   db = "model")

model = pickle.load(open('model.pkl','rb'))
print(model)
@app.route("/", methods=['GET'])
def main():
    return render_template("Login.html")

@app.route("/login", methods=['Post']) #Add Get if doesn't work
def log():
    username = request.form.get('exp')
    password = request.form.get('test')
    with db_connection() as conn:
        conn = db_connection()
        cur = conn.cursor()
        output = cur.execute("select * from Details WHERE Username = %s", (username,))
        result = cur.fetchone()
        print(result, check_password_hash(result[0], password))
        if result and check_password_hash(result[1], password):
                return redirect(url_for('predict'))
        else:
            data = "Invalid Username or Password!"
            return render_template("Login.html", msg=data)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('new_exp')
        password = request.form.get('new_test')
        hashed_password = generate_password_hash(password)
        
        with db_connection() as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO Details (Username, Password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return redirect(url_for('main'))
    
    return render_template("Signup.html")

@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        pred =  [str(i) for i in (request.form.values())]
        D = {'mega': 0, 'micro': 1,'nano': 2, 'macro': 3}
        pred[3] = D[pred[3]]
        pred = [float(i) for i in pred]
        print(pred, model)
        out = round(model.predict([pred])[0],2)
        return render_template("Success.html", data=out)
    return render_template("Prediction.html")

if __name__ == '__main__':
    app.run(host='localhost', port = 5000)