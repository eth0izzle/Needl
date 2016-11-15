import socket
import schedule
import needl, needl.utils as utils
from . import catch_exceptions


def register():
    schedule.every(needl.settings['dns']['lookup_interval']).minutes.do(lookup)


@catch_exceptions
def lookup():
    site = utils.get_line(needl.args.datadir + '/top-1m.csv').split(',')[1]

    try:
        host = socket.gethostbyname(site)
        needl.log.info('%s resolved to %s', site, host)
    except socket.gaierror:
        needl.log.warning('Failed to resolve %s', site)