import socket
import needl, needl.schedule as schedule, needl.utils as utils


def register():
    # todo: ugly
    li = needl.settings['dns']['lookup_interval']
    args = map(int, li.split('..'))
    schedule.every(*args).minutes.do(lookup)


def lookup():
    site = utils.get_line(needl.args.datadir + '/top-1m.csv').split(',')[1]

    try:
        host = socket.gethostbyname(site)
        needl.log.info('%s resolved to %s', site, host)
    except socket.gaierror:
        needl.log.warning('Failed to resolve %s', site)
