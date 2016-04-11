var Slack = require('slack-client');
var querystring = require('querystring');
var http = require('http');
var config = require('./config.json');

var slackToken = config.yugoSlackToken;
var autoReconnect = true;
var autoMark = true;

var slack = new Slack(slackToken, autoReconnect, autoMark);

slack.on('open', function () {
    console.log("Connected to " + slack.team.name + " as " + slack.self.name);
});

slack.on('message', function (message) {
    if (!message.text) {
        return;
    }
    var words = message.text.split(" ");
    var start = words.shift().toLowerCase();
    var devCommands = config.yugoDevCommands;
    var commands = [
        "<@u0ckd3ksl>",
        "<@u0ckd3ksl>:",
        "<@u0ckd3ksl>,",
        "yugo",
        "yugo:",
        "yugo,"
    ];
    if (devCommands.indexOf(start) != -1) {
        http.get("http://localhost:8000/?message=" + encodeURIComponent(words.join(" ")), function (response) {
            response.setEncoding('utf8');
            response.on("data", function(chunk) {
              channel = slack.getChannelGroupOrDMByID(message.channel);
              channel.send(chunk);
            });
        }).on('error', function (e) {
            console.log("API Error: " + e.message);
        });
    }
});

slack.on('error', function (err) {
    console.error("Slack Error: " + err.msg);
});

slack.login();
