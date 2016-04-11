from slack_api_action import Action
import json
import  requests
import random

class Groupon(Action):

    def __init__(self, message):
        super(Groupon, self).__init__(message)
        self.message = message
        self.categories = ["food", "automotive", "beauty", "fitness", "shopping"]
        self.base_url = "https://partner-api.groupon.com/deals.json?tsToken=US_AFF_0_201236_212556_0&"

    def render(self):
        custom_url = self.map_url()
        r = requests.get(self.base_url + custom_url)
        data = json.loads(r.text)
        result_list = []
        for deal in data["deals"]:
            deal_url = deal["dealUrl"]
            result = ""
            deal_data = deal["options"][0]
            result += "*" +  deal_data["title"] + "*"+ "\n"
            result += "Buy this deal at " + deal_url + "\n"
            result_list.append(result)
        random_results =  random.sample(result_list, 5)
        random_string = ""
        for result in random_results:
            random_string += result + "\n"

        return random_string


    def map_category(self):
        if not self.command:
            return ""
        else:
            category = self.command

        mapper = { "food": "food-and-drink",
                    "automative": "automative",
                    "beauty": "beauty-and-spas",
                    "men": "men",
                    "women": "women",
                    "fitness": "health-and-fitness"
                }
        if category in mapper:
            return mapper[category]
        return ""


    def map_location(self):
        command_info = self.message.split(" ")
        if len(command_info) > 3:
            location = command_info[2:]
            return "-".join(location)
        elif len(command_info) == 3:
            return command_info[2]
        return ""


    def map_url(self):
        custom_url = "&".join("offset=0&limit=50")
        category = self.map_category()
        location = self.map_location()
        if category:
            category_filter = "filters=category:{}".format(category)
            custom_url = "&".join((custom_url, category_filter))
        if location:
            category_location = "division_id={}".format(location)
            custom_url = "&".join((custom_url, category_location))
        return custom_url
