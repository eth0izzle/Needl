import random
import needl, needl.utils as utils
from . import catch_exceptions
from needl.adapters.fingerprint import FingerprintAdapter
import schedule
import requests
import zipfile
from io import BytesIO
import urllib.parse as url

AWS_ROOT = 'https://s3.amazonaws.com'
CSV_NAME = 'top-1m.csv'
TOP1M = '/alexa-static/' + CSV_NAME + '.zip'
AWS_THUMBPRINT = '46516b8e1492af030d2c747a5a3137b57423a843'

sites = None


def register():
    global sites
    sites = needl.args.datadir + '/' + CSV_NAME
    schedule.every(needl.settings['alexa']['update_interval']).days.do(update)
    schedule.every(needl.settings['alexa']['visit_interval']).minutes.do(visit, needl.settings['alexa']['click_through'])


def get_random_site():
    return 'http://' + utils.get_line(sites).split(',')[1]


@catch_exceptions
def visit(click_through=True):
    site = get_random_site()
    needl.log.info('Visiting %s', site)

    browser = utils.get_browser()
    page = browser.get(site)
    links = [link for link in page.soup.findAll('a') if utils.url_is_absolute(link.get('href'))]

    if click_through and len(links) > 0:
        link = random.choice(links).get('href')
        needl.log.info('Visiting %s', link)
        browser.get(link)


@catch_exceptions
def update():
    needl.log.info('Downloading Alexa top one million list (%s)', TOP1M)
    r = requests.session()
    r.mount(AWS_ROOT, FingerprintAdapter(AWS_THUMBPRINT))
    file = r.get(url.urljoin(AWS_ROOT, TOP1M))

    with zipfile.ZipFile(BytesIO(file.content)) as zip:
        zip.extractall(sites)