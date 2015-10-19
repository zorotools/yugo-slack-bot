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


if __name__ == "__main__":
    app.run(host='0.0.0.0')
