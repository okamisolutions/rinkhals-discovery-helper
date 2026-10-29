. /useremain/rinkhals/.current/tools.sh

APP_ROOT=$(dirname $(realpath $0))
APP_LOG=$RINKHALS_LOGS/app-discovery-helper.log

status() {
    PIDS=$(get_by_name join-multicast.py)

    if [ "$PIDS" == "" ]; then
        report_status $APP_STATUS_STOPPED
    else
        report_status $APP_STATUS_STARTED "$PIDS" $APP_LOG
    fi
}
start() {
    stop
    log "Starting discovery helper"

    # Run from the app folder: busybox ps cuts long command lines, so get_by_name would not find the full path
    cd $APP_ROOT
    mkdir -p $RINKHALS_LOGS

    # Detach from the caller: the on-screen menu reads its output through a pipe and waits for it to close,
    # and a shell started from a terminal sends SIGHUP to its jobs when the session ends
    nohup python join-multicast.py </dev/null >> $APP_LOG 2>&1 &
}
stop() {
    kill_by_name join-multicast.py
}

case "$1" in
    status)
        status
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
        echo "Usage: $0 {status|start|stop}" >&2
        exit 1
        ;;
esac
