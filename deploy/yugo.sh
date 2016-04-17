#!/bin/bash
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source setenv

NAME=yugo
PM2=/usr/local/lib/node_modules/pm2/bin/pm2

export PATH=/usr/bin:$PATH
export YUGO_LOGS="$YUGO_HOME/logs"
export DEPLOY_HOME="$YUGO_HOME/deploy"
export PM2_HOME="$YUGO_LOGS/pm2"
export GUNICORN="$YUGO_HOME/api/bin/gunicorn"

cd $YUGO_HOME/api
source bin/activate

start() {
    echo "Starting $NAME"
    $PM2 start $YUGO_HOME/client/index.js --name "$NAME"
    echo $GUNICORN --bind="127.0.0.1:8000" --access-logfile="$YUGO_LOGS/access.log" --pid="$YUGO_LOGS/pid" --daemon wsgi:app
    $GUNICORN --bind="127.0.0.1:8000" --access-logfile="$YUGO_LOGS/access.log" --pid="$YUGO_LOGS/pid" --daemon wsgi:app
}

stop() {
    echo "Stopping $NAME"
    $PM2 delete all
    $PM2 kill
    kill -9 `cat $YUGO_LOGS/pid`
}

restart() {
    echo "Restarting $NAME"
    stop
    start
}

reload() {
    echo "Reloading $NAME"
    $PM2 reload all
    kill -HUP `cat $YUGO_LOGS/pid`
}

status() {
    echo "Status for $NAME:"
    $PM2 list
    ps -ef | grep `cat $YUGO_LOGS/pid` | grep -v grep
}

deploy() {
    echo "Deploying $NAME"
    pip install -r requirements.txt
    reload
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        status
        ;;
    restart)
        restart
        ;;
    reload)
        reload
        ;;
    deploy)
        deploy
        ;;
    *)
        echo "Usage: {start|stop|status|restart|reload|deploy}"
        exit 1
        ;;
esac
exit 
