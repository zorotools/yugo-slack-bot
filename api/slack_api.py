from flask import Flask
from flask import request
import requests
import random
import json

app = Flask(__name__)


@app.route("/")
def get():
    message = request.args.get('message')
    if message == 'lunch':
        return lunch()
    elif message == 'aww':
        return aww()
    elif message == 'happyhour':
        return happyhour()
    elif message.startswith('cat'):
        return cat(message)
    else:
        return unknown()


@app.route("/lunch")
def lunch():
    options = ['Leghorn', 'Rezas', 'Brunch', 'Cocoro', 'Slurping Turtle', 'India House', 'Portillos', "Al's Beef",
               'Taco Joint'
               'Wildfire', 'McDonalds', 'Fado', 'Kerrymans']
    return random.choice(options)


@app.route("/happyhour")
def happyhour():
    options = ['Municipal', 'Pepper Cannister', "O'Leary's Pub", 'Stout Barrel House & Gallery', 'Fado', 'Kerrymans']
    return random.choice(options)


@app.route("/aww")
def aww():
    r = requests.get('http://www.reddit.com/r/aww.json')
    data = json.loads(r.text)
    urls = []
    for i in data['data']['children']:
        urls.append(i['data']['url'])
    return random.choice(urls)

@app.route("/unknown")
def unknown():
    options = ['You\'re not making any sense...',
               'Did you want something from me?',
               'Could you repeat that, I couldn\'t quite hear you.',
               'WHAT?',
               'You talkin\' to me?',
               'Whoa, slow down. What are we talking about now?',
               'I don\'t think I like your tone',
               'Step One: you cut a hole in the box']
    return random.choice(options);

@app.route("/cat")
def cat(message):
    import xmltodict
    if message.startswith('cat me '):
        category = message.split(' ')[2]
        r = requests.get('http://thecatapi.com/api/images/get?format=xml&category=' + category)
        xml = xmltodict.parse(r.text)
        print 'printing works'
        if xml['response']['data']['images']:
            return xml['response']['data']['images']['image']['url']
        else:
            return 'That\'s not a valid cat category!'
    elif message.startswith('cat categories'):
        r = requests.get('http://thecatapi.com/api/categories/list')
        xml = xmltodict.parse(r.text)
        returnString = ""
        for category in xml['response']['data']['categories']['category']:
            returnString = returnString + category['name'] + "\n"
        return returnString
    else:
        r = requests.get('http://thecatapi.com/api/images/get?format=xml')
        xml = xmltodict.parse(r.text)
        return xml['response']['data']['images']['image']['url']

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
