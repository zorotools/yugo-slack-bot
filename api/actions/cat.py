from slack_api_action import Action
import xmltodict
import requests

class Cat(Action):

    def __init__(self, message):
        super(Cat, self).__init__(message)
        self.helpDict = {
            'yugo cat': 'Display a random cat image',
            'yugo cat categories': 'Display a list of available cat image categories',
            'yugo cat {category}': 'Display a random cat image from within a given category'
        }

    def render(self):
        if self.command == 'me':
            category = self.params.pop(0)
            r = requests.get('http://thecatapi.com/api/images/get?format=xml&category=' + category)
            xml = xmltodict.parse(r.text)
            if xml['response']['data']['images']:
                return xml['response']['data']['images']['image']['url']
            else:
                return 'That\'s not a valid cat category!'
        elif self.command == 'categories':
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
