from slack_api_action import Action
from utils.geocode import Geocode
import requests
import urllib
import json
import datetime
import calendar
import config


class Weather(Action):
    def __init__(self, message):
        super(Weather, self).__init__(message)
        self.helpDict = {
            'yugo weather {location}': 'Display the current weather contions for the given location (defaults to Chicago)',
            'yugo weather forecast {location}': 'Display the 7 day forecast for the given location (defaults to Chicago)'
        }
        self.degree_sign= u'\N{DEGREE SIGN}'
        commands = ['current', 'forecast']
        if not self.command or self.command not in commands:
            if self.command:
                self.params.append(self.command)
            self.command = 'current'
        if not self.params:
            self.params.append('Chicago')
        location = ' '.join(self.params)
        geocode = Geocode(location)
        self.location = geocode.get_geocode()
        
    def current(self):
        result = requests.get('https://api.forecast.io/forecast/' + config.forecast_io_api_key + '/' + str(self.location['latitude']) + ',' + str(self.location['longitude']))
        data = result.json()
        return_string = "Current weather for " + self.location['name'] + ": \n"
        weather_data = {
            'Conditions': str(data['currently']['summary']),
            'Temerature': str(data['currently']['temperature']) + self.degree_sign + " F",
            'Wind Speed': str(data['currently']['windSpeed']) + " mph",
        }
        for key, value in weather_data.iteritems():
            return_string += "*" + key + ":* " + value + "\n"
        return return_string
        
    def forecast(self):
        days = ['Today', 'Tomorrow']
        for offset in range(2, 8):
            date = datetime.date.today() + datetime.timedelta(days=offset)
            weekday = date.weekday()
            days.append(calendar.day_name[weekday])
        result = requests.get('https://api.forecast.io/forecast/' + config.forecast_io_api_key + '/' + str(self.location['latitude']) + ',' + str(self.location['longitude']))
        data = result.json()
        return_string = "7 day forecast for " + self.location['name'] + ": \n"
        return_string += data['daily']['summary'] + "\n\n"
        for day in data['daily']['data']:
            return_string += "*" + days.pop(0) + "*\n"
            return_string += day['summary'] + "\n"
            return_string += "High Temperature: " + str(day['temperatureMax']) + self.degree_sign + " F\n"
            if day.get('precipProbability'):
                return_string += "Chance of " + day['precipType'] + ": " + str(day['precipProbability'] * 100) + "%\n"
            return_string += "\n"
        return return_string
        
    def render(self):
        commands = {
            'current': self.current,
            'forecast': self.forecast
        }
        return commands[self.command]()
        