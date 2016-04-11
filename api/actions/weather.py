from slack_api_action import Action
import requests
import urllib
import json
import config


class Weather(Action):
    def __init__(self, message):
        super(Weather, self).__init__(message)
        self.helpDict = {
            'yugo weather {location}': 'Display the current weather contions for the given location (defaults to Chicago)',
            'yugo weather forecast {location}': 'Display the 5 day forecast for the given location (defaults to Chicago)'
        }
        commands = ['current', 'forecast']
        if not self.command or self.command not in commands:
            if self.command:
                self.params.append(self.command)
            self.command = 'current'
        if not self.params:
            self.params.append('Chicago')
        self.location = ' '.join(self.params)
        if ',' not in self.location:
            self.location += ',us'
        
    def makeApiCall(self, url, params):
        if 'units' not in params:
            params['units'] = 'Imperial'
        response = requests.get(url + '?' + urllib.urlencode(params))
        return response.json()
        
    def current(self):
        response = self.makeApiCall('http://api.openweathermap.org/data/2.5/weather', {'q': self.location, 'appid': config.weather_api_key})
        returnString = "Current weather for " + response['name'] + ": \n"
        degree_sign= u'\N{DEGREE SIGN}'
        weatherData = {
            'Conditions': str(response['weather'][0]['description']),
            'Temerature': str(response['main']['temp']) + degree_sign + " F",
            'Wind Speed': str(response['wind']['speed']) + " mph",
        }
        for key, value in weatherData.iteritems():
            returnString += "*" + key + ":* " + value + "\n"
        return returnString
        
        
    def forecast(self):
        pass
        
    def render(self):
        commands = {
            'current': self.current,
            'forecast': self.forecast
        }
        return commands[self.command]()
        