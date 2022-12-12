import send
import requests
import boto3
from flask import Flask,jsonify,request,render_template


app = Flask(__name__)

client = boto3.client(
        "sns",
        aws_access_key_id="xxxxxxx",
        aws_secret_access_key= "xxxxxxxxxxxxxxx",
        region_name="us-east-1")

topic_arn=""

app = Flask(__name__)
      
#Get email from user input in form
@app.route('/', methods = ['POST' , 'GET' ])
def home(): 
    if request.method == 'POST':
        email = request.form['email']
        city = request.form['city']
        send.sns(email)
        weather, temp = send.getWeather_info(city)
        send.sendEmail()
    return render_template("index.html")


if __name__ == '__main__':
        app.run(host="0.0.0.0", port=8080)