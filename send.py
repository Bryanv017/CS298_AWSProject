import app
import boto3
import requests

client = boto3.client(
        "sns",
        aws_access_key_id="xxxxxxxxxxx",
        aws_secret_access_key="xxxxxxxxxxxxxx",
        region_name="us-east-1")

response = client.create_topic(Name="weather_info")
topic_arn = response["TopicArn"]

API_key = 'xxxxxxxx'

#creates weather topic and adds email to it
def sns(email):
        response = client.create_topic(Name="weather_info")
        topic_arn = response["TopicArn"]
        subscribed = False
        subscriptions = client.list_subscriptions_by_topic(TopicArn=topic_arn).get('Subscriptions')
        for subscription in subscriptions:
                if ((email == subscription.get('Endpoint')) and (subscription.get('SubscriptionArn') != 'PendingConfirmation')):
                        subscribed = True
        if not subscribed:
                response = client.subscribe(TopicArn=topic_arn, Protocol="Email", Endpoint= email)
                subscription_arn = response["SubscriptionArn"]

def getWeather_info(input):
        global city,weather,temp
        city = input
        url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}&units=imperial'.format(city,API_key)
        res = requests.get(url)
        data = res.json()
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        print("City Name:", city)
        print('Weather Description:', weather)
        print('Temperature: {0} F'.format(temp))
        return weather,temp


def sendEmail():
    client.publish(TopicArn = topic_arn,
                Message = '''City Name: {0}\nWeather Description:{1}\nTemperature: {2} F'''
                       .format(city,weather,temp),
                Subject = "Weather Information")




