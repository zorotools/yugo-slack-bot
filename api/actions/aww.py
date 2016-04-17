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
        r = requests.get('http://www.reddit.com/r/aww.json', headers = {'User-agent': 'Slack Yugo bot 1.01'})
        awwUrl = "http://imgur.com/x6TwpSQ"
        data = json.loads(r.text)
        if data['data']['children']:
            awwUrl = random.choice(data['data']['children'])['data']['url']
        return awwUrl
