from flask import Flask
from flask import request
import importlib
import random
from actions.basics import Lunch
from actions.aww import Aww
from actions.basics import Happyhour
from actions.cat import Cat
from actions.help import Help

app = Flask(__name__)

commands = {
    'lunch': Lunch,
    'aww': Aww,
    'happyhour': Happyhour,
    'cat': Cat,
    'help': Help
}

@app.route("/")
def get():
    message = request.args.get('message')
    command = message.split(' ').pop(0)
    if command in commands:
        cls = commands[command]
        inst = cls(message)
        return inst.render()
    else:
        return unknown()

def unknown():
    options = ['You\'re not making any sense...',
               'Did you want something from me?',
               'Could you repeat that, I couldn\'t quite hear you.',
               'WHAT?',
               'You talkin\' to me?',
               'Whoa, slow down. What are we talking about now?',
               'I don\'t think I like your tone']
    return random.choice(options);

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
