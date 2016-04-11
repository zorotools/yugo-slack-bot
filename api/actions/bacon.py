from slack_api_action import Action
import requests

class Bacon(Action):

    def __init__(self, message):
        super(Bacon, self).__init__(message)
        self.helpDict = {
            'yugo bacon': 'Display a five-paragraph all bacon ipsum paragraph',
            'yugo bacon <all|some>': 'Display a single paragraph all or some bacon ipsum paragraph',
            'yugo bacon <all|some> <num>': 'Display number of aragraphs of all or some bacon ipsum paragraph',
        }

    def render(self):
        if len(self.params) <= 0:
            paras = "1"
        else:
            paras = self.params.pop(0)
        if self.command == 'all':
            r = requests.get('https://baconipsum.com/api/?format=text&type=all-meat&paras=' + paras)
            returnString = r.text
        elif self.command == 'some':
            r = requests.get('https://baconipsum.com/api/?format=text&type=meat-and-filler&paras=' + paras)
            returnString = r.text
        else:
            r = requests.get('https://baconipsum.com/api/?format=text&type=all-meat&paras=5')
            returnString = r.text
        return returnString
