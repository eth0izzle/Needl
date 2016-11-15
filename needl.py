import os, sys, time, argparse, logging
import daemon, daemon.pidfile
import needl, needl.tasks as scheduler


def main():
    parser = argparse.ArgumentParser(description=needl.__description__)
    parser.add_argument('--datadir', default=os.getcwd() + '/data', help='Data directory')
    parser.add_argument('-d', '--daemon', action='store_true', help='Run as a deamon')
    parser.add_argument('-v', '--verbose', action='store_true', help='Increase logging')
    parser.add_argument('--logfile', type=argparse.FileType('a'), default=sys.stdout, help='Log to this file. Default is stdout.')
    parser.add_argument('--pidfile', default='/tmp/needl.pid', help='Save process PID to this file. Default is /tmp/needl.pid. Only valid when running as a daemon.')
    args = parser.parse_args()

    if args.daemon and args.logfile is sys.stdout:
        args.logfile = open('/tmp/needl.log', 'a')

    needl.init(args)
    daemonize(args.logfile, args.pidfile) if args.daemon else start()


def daemonize(logfile, pidfile):
    needl.log.info('Daemonizing and logging to %s', logfile)

    with daemon.DaemonContext(working_directory=os.getcwd(),
                              stderr=logfile,
                              umask=0o002,
                              pidfile=daemon.pidfile.PIDLockFile(pidfile)) as dc:

        start()


def start():
    needl.log.info('Starting %s v%s', needl.__project__, needl.__version__)

    scheduler.register_tasks()

    while True:
        try:
            scheduler.start()
            time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            needl.log.debug('Received terminate signal..')
            stop()


def stop():
    needl.log.warn('Shutting down')

    scheduler.stop()

    if needl.args.logfile is not sys.stdout:
        needl.log.debug('Closing logfile %s', needl.args.logfile.name)
        needl.args.logfile.close()

    logging.shutdown()
    sys.exit()


if __name__ == "__main__":
    main()