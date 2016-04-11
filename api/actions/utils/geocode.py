import requests
import json
import urllib
import config


class Geocode(object):
    def __init__(self, location):
        self.location = location
        self.url = 'https://maps.googleapis.com/maps/api/geocode/json'
        
    def set_location(self, location):
        self.location = location
        
    def get_geocode(self):
        params = {
            'address': self.location,
            'key': config.google_geocode_api_key
        }
        response = requests.get(self.url + '?' + urllib.urlencode(params))
        data = response.json()
        return {
            'name': data['results'][0]['formatted_address'],
            'latitude': data['results'][0]['geometry']['location']['lat'],
            'longitude': data['results'][0]['geometry']['location']['lng']
        }
        