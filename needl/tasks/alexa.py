import needl, needl.schedule as schedule, needl.utils as utils
from needl.adapters.fingerprint import FingerprintAdapter
import requests
import zipfile
from io import BytesIO
import urllib.parse as url

AWS_ROOT = 'https://s3.amazonaws.com'
CSV_NAME = 'top-1m.csv'
TOP1M = '/alexa-static/' + CSV_NAME + '.zip'
AWS_THUMBPRINT = '46516b8e1492af030d2c747a5a3137b57423a843'


def register():
    schedule.every(needl.settings['alexa']['update_interval']).days.do(update)

    vi = needl.settings['alexa']['visit_interval']
    args = map(int, vi.split('..'))
    schedule.every(*args).minutes.do(visit)


def get_random_site():
    return 'http://' + utils.get_line(needl.args.datadir + '/' + CSV_NAME).split(',')[1]


def visit():
    site = get_random_site()

    needl.log.info('Visiting %s', site)
    browser = utils.get_browser()
    page = browser.get(site)

    utils.process_click_depth(browser, page, needl.settings['alexa']['click_depth'])

def update():
    needl.log.info('Downloading Alexa top one million list (%s)', TOP1M)
    r = requests.session()
    r.mount(AWS_ROOT, FingerprintAdapter(AWS_THUMBPRINT))
    file = r.get(url.urljoin(AWS_ROOT, TOP1M))

    with zipfile.ZipFile(BytesIO(file.content)) as zip:
        zip.extractall(needl.args.datadir)
