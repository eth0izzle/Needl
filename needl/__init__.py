import sys, random, logging, yaml

__project__ = 'needl'
__description__ = 'Take back your privacy. Lose yourself in the haystack.'
__version__ = '0.1'

log = logging.getLogger(__name__)
args = None
settings = None
rand = random.SystemRandom()

if sys.version_info < (3, 0):
    sys.exit('Error: Python 3.0+ is required.') # peasants


def init(_args):
    global settings, args
    args = _args

    with open(args.config) as f:
        settings = yaml.load(f)

    logging.basicConfig(stream=args.logfile,
                        level=logging.DEBUG if args.verbose else logging.INFO,
                        format='(%(levelname)s) [%(module)s->%(funcName)s]: %(message)s')
