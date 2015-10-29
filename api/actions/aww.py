from slack_api_action import Action
import requests
import random
import json

class Aww(Action):

    def __init__(self, message):
        super(Aww, self).__init__(message)
        self.helpDict = {
            'yugo aww': 'Display a random image from the "aww" subreddit'
        }

    def render(self):
        r = requests.get('http://www.reddit.com/r/aww.json')
        data = json.loads(r.text)
        urls = []
        for i in data['data']['children']:
            urls.append(i['data']['url'])
        return random.choice(urls)
