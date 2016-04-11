from slack_api_action import Action
import importlib

class Help(Action):

    def __init__(self, message):
        super(Help, self).__init__(message)
        self.helpDict = {
            'yugo help': 'Display a list of all available commands',
            'yugo help {command}': 'Display the help text for a particular command'
        }

    def render(self):
        from slack_api import commands

        if self.command and self.command in commands:
            cls = commands[self.command]
            inst = cls('')
            return inst.renderHelp()
        else:
            returnString = ''
            for command in commands:
                returnString += command + "\n"
            return returnString
