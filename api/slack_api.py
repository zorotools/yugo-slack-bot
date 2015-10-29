from flask import Flask
from flask import request
import importlib
import random

app = Flask(__name__)

commands = {
    'lunch': 'actions.basics.Lunch',
    'aww': 'actions.aww.Aww',
    'happyhour': 'actions.basics.Happyhour',
    'cat': 'actions.cat.Cat',
    'help': 'actions.help.Help'
}

@app.route("/")
def get():
    message = request.args.get('message')
    command = message.split(' ').pop(0)
    if command in commands:
        mod = importlib.import_module(commands[command].rsplit('.', 1)[0])
        print mod
        cls = getattr(mod, commands[command].rsplit('.', 1)[1])
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
