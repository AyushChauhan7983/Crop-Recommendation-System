from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pickle

from sqlalchemy.orm import Mapped, mapped_column

# importing model
model = pickle.load(open('rf.pkl','rb'))

# creating flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://ayush:ayush7983@localhost/crop_recommendation"
db=SQLAlchemy(app)

class Predictions(db.Model):
    sno: Mapped[int] = mapped_column(primary_key=True)
    nitrogen: Mapped[int] = mapped_column(unique=False, nullable=False)
    phosphorous: Mapped[int] = mapped_column(unique=False, nullable=False)
    potassium: Mapped[int] = mapped_column(unique=False, nullable=False)
    temperature: Mapped[int] = mapped_column(unique=False, nullable=False)
    humidity: Mapped[int] = mapped_column(unique=False, nullable=False)
    pH: Mapped[int] = mapped_column(unique=False, nullable=False)
    rainfall: Mapped[int] = mapped_column(unique=False, nullable=False)
    crop: Mapped[str] = mapped_column(unique=False, nullable=False)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/harvest')
def harvest():
    return render_template("harvest.html")

@app.route('/form')
def form():
    return render_template("form.html")

@app.route("/history")
def show_all():
    return render_template("history.html",crops=Predictions.query.all())

@app.route("/predict",methods=['POST'])
def predict():
    N = request.form['Nitrogen']
    P = request.form['Phosphorus']
    K = request.form['Potassium']
    temp = request.form['Temperature']
    humidity = request.form['Humidity']
    ph = request.form['Ph']
    rainfall = request.form['Rainfall']

    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    prediction = model.predict(single_pred)

    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}

    if prediction[0] in crop_dict:
        crop = crop_dict[prediction[0]]
        result = "{} is the best crop to be cultivated right there".format(crop)
    else:
        result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

    entry = Predictions(nitrogen=N,phosphorous=P,potassium=K,temperature=temp,humidity=humidity,pH=ph,rainfall=rainfall,crop=crop)
    db.session.add(entry)
    db.session.commit()
    return render_template('form.html',result=result)

# python main
if __name__ == "__main__":
    app.run(debug=True)