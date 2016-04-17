# yugo-slack-bot
A client for a generic Slack bot and an API it can talk to.

## Local setup

### Slack client
The slack client lives in the root `/client` directory. It is a NodeJS app that uses the [Slack Client](https://github.com/slackhq/node-slack-client) package to connect to Slack and listen for messages.

To set up this client to listen locally, you will need:

* NodeJS
    * OS X: `brew install node`
    * Ubuntu: `apt-get install nodejs nodejs-legacy`
* NPM
    * OS X: `brew install npm`
    * Ubuntu: `apt-get install npm`

Once these are installed, `cd` into the `/client` directory and do the following:

1. Run `npm install`
2. Run `cp config.json.default config.json` to create a working version of the config file
3. Edit `config.json`
    1. Add Yugo's Slack API key for `yugoSlackToken`
    2. Add a unique value to `yugoDevCommands`, optionally removing the existing value. This unique value will allow you to trigger your local instance of Yugo without others doing so.
    3. Set `yugoDevMode` to `true`. This will make your local instance of Yugo listen for the command you specified above, instead of the default commands.
4. You can now start the client with `node index.js`

The client functions by passively listening to any channels it has access to. It checks each incoming message to see if the message starts with one of its recognized commands, and if it does, it passes that message on to the API server. When the server responds, the client posts that response back to the slack channel from which the initial message originated.

### API Server
The API server lives in the root `/api` directory. It is a Python app that uses the Flask framework.

To set up this server locally, you will need:

* pip
    * OS X: `easy_install pip`
        * Alternatively you can install a different version of Python than the OS X default using `brew install python`, which will come with pip.
    * Ubuntu: `apt-get install python-pip`
* Virtualenv
    * OS X: `pip install virtualenv`
    * Ubuntu: `apt-get install virtualenv`

Once you have this installed, `cd ` into the `/api` directory and do the following:

1. Run `virtualenv .` to set up a virtual environment in the current directory
2. Run `source bin/activate` to activate your newly created virtual environment
3. Run `pip install -r requirements.txt` to install required packages
4. Run `cp config.py.default config.py` to create a working version of the config file
5. Edit `config.py`
    1. Add the API keys as appropriate
    2. Set `flask_debug` to `True` to have Flask run in debug mode, allowing more detailed error messages.
6. You can now start the server with `python slack_api.py`

The server functions as a standard API server. The current setup has it accepting only one parameter, `message`, which is the message text passed in from the Node client. It assumes the first word of this message to be the command, and dispatches the request accordingly.

## Developing for the API

To add a new command to the API server, you will need to do the following:

1. Create a new class that will manage the functionality of this command. You can do this by adding a new file in `/api/actions`, or by adding a new class to an existing file.
2. Your class must:
    * Inherit from the `Action` base class, found in `/api/actions/slack_api_action.py`
    * Accept two arguments in its constructor (`self` and `message`, though technically you can name them whatever you want)
    * Call its parent class's constructor from its own constructor, passing its own second argument (`message`) as an argument to the parent
    * Define, in its constructor, a dictionary named `self.helpDict` which will define the help text that is printed for your command when a user asks for it
    * Define a public method called `self.render`, the return value of which is what will eventually be posted to Slack.
3. Edit `/api/slack_api.py`
    1. Add an import line for your new class
    2. Add an entry in the `commands` dictionary, where the key is the unique command that will trigger your new action, and the value is your new class.

Beyond that, the rest is up to you. Current endpoints range in complexity from displaying a random entry from a static list of possibilities (`yugo lunch`) to searching a place name in Google's Geocoding API to retrieve latitude and longitude, then using that information to retrieve and display a 7 day weather forecast for that location (`yugo weather forecast`). If you can do it in Python, you can make Yugo do it for you.

## Developing for the client

So far we've had little need or desire to do additional development on the Node client side of things, so the playing field is wide open. There's no standardized way to add functionality like there is on the Python side, but if you do decide to start adding functionality to the Node client, please keep an eye towards architecture and maintainability.

Some ideas we've had that would make good Node projects include:
* Having Yugo interact with all conversations, not just those that begin with a recognized keyword. Maybe he should listen for any time someone uses the words "major", "private", "kernel" or the like, and respond with "*salute* Colonel Panic!"
* Set up a server aspect to listen on a given port. This endpoint could look for two parameters, `channel` and `message`, and post the given message to the given channel any time the endpoint is hit. This would allow us to automate some posts (like a Monday morning weekly weather forecast), using cron or something similar.

## Deploying Yugo

Running the client application in daemon mode requires pm2, process manager for Node.js
Run `npm install pm2 -g` to install pm2

The server app is daemonized with gunicorn, which should already exist in the virtualenv

Once pm2 is installed, `cd ` into the `/deploy` directory and do the following:
1. Run `cp setenv.default setenv` to create a working version of the setenv file
2. Edit `setenv` to set the proper `YUGO_HOME`
3. You can now start the client/server in daemon mode with `/bin/bash yugo.sh start`

Run `/bin/bash yugo.sh` to see all the available options
