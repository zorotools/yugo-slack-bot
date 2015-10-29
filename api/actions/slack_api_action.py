class Action(object):

    def __init__(self, message):
        self.params = message.split(' ')[1:]
        if self.params:
            self.command = self.params.pop(0)
        else:
            self.command = False
        self.helpDict = {}

    def renderHelp(self):
        helpString = ''
        count = 0
        for key in self.helpDict:
            if count > 0:
                helpString += "\n\n"
            helpString += "*Usesage:* `" + key + "`\n"
            helpString += "*Description:* " + self.helpDict[key]
            count += 1
        return helpString
