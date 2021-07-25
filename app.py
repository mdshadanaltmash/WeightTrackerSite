from flask import Flask,render_template,redirect,session,url_for,flash
from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,FloatField
from pymongo import MongoClient
from datetime import datetime

app=Flask(__name__)
app.config['SECRET_KEY']='mysecretkey'


def saveDetails(name,weight):
    client = MongoClient("mongodb+srv://sadaalt:sadaalt@cluster0.8s1ok.gcp.mongodb.net/Persons?retryWrites=true&w=majority")
    db = client.Persons

    #Store the details
    db.Weight.insert_one({
        'Name':name,
        'Weight':weight,
        'Date':datetime.now()
        })
    client.close()
    
class DetailsForm(FlaskForm):
    name=StringField("What is your Name: ")
    weight=FloatField("What is your Current weight: ")
    submit=SubmitField('Save')

@app.route('/',methods=['GET','POST'])
def index():
    form=DetailsForm()
    if form.validate_on_submit():
        name=form.name.data
        weight=form.weight.data
        saveDetails(name,weight)  #saving details on database
        print(name)
        #flash(f"Hi {name}! Your Data has been saved")
        return redirect('saved')
    return render_template('index.html',form=form)

@app.route('/saved')
def saved():
    return render_template('saved.html')
if __name__=='__main__':
    app.run(debug=True)