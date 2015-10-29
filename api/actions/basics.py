from slack_api_action import Action
import random

class Lunch(Action):
    def __init__(self, message):
        super(Lunch, self).__init__(message)
        self.helpDict = {
            'yugo lunch': 'Display a random lunch location'
        }

    def render(self):
        options = ['Leghorn', 'Rezas', 'Brunch', 'Cocoro', 'Slurping Turtle', 'India House', 'Portillos', "Al's Beef",
                   'Taco Joint', 'Wildfire', 'McDonalds', 'Fado', 'Kerrymans']
        return random.choice(options)

class Happyhour(Action):
    def __init__(self, message):
        super(Happyhour, self).__init__(message)
        self.helpDict = {
            'yugo happyhour': 'Display a random happy hour location'
        }

    def render(self):
        options = ['Municipal', 'Pepper Cannister', "O'Leary's Pub", 'Stout Barrel House & Gallery', 'Fado', 'Kerrymans']
        return random.choice(options)
