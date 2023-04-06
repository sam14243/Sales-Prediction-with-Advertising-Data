from flask import Flask, request, \
        render_template
app = Flask(__name__)
import pymysql as pms
conn = pms.connect(host="localhost", 
                   port = 3306, 
                   user="root", 
                   password="mysql",
                   db = "model")
import pickle
model = pickle.load(open('model.pkl','rb'))

@app.route("/")
def main():
    return render_template("Login.html")

@app.route("/login", methods=['Get','Post'])
def log():
    features = [str(i) for i in (request.form.values())]
    #pred = model.predict([features])
    #pred = round(pred[0],2)
    #print(features)
    cur = conn.cursor()
    output = cur.execute("select * from Details WHERE Username = %s AND Password = %s", (features[0], features[1]))
    check = cur.fetchone()
    #print(check)
    if (check):
        
        return render_template("Prediction.html")
    else:
        data = "Invalid Username or Password!"
        return render_template("Login.html", msg=data)
    
@app.route("/predict", methods=['Get','Post'])
def pred():
    pred =  [str(i) for i in (request.form.values())]
    D = {'mega': '0', 'micro': '1','nano': '2', 'macro': '3'}
    pred[3] = D[pred[3]]
    pred = [float(i) for i in pred]
    out = round(model.predict([pred])[0],2)
    return render_template("success.html", data=out)
    #return 1

if __name__ == '__main__':
    app.run(host='localhost', port = 5000)