import needl, needl.utils as utils
from . import catch_exceptions
import schedule
import random

GOOGLE = 'https://www.google.co.uk'


def register():
    schedule.every(needl.settings['google']['search_interval']).minutes.do(search, needl.settings['google']['click_through'])


@catch_exceptions
def search(click_through=True):
    search_phrase = utils.get_keywords(3)
    needl.log.info('Searching Google for: %s', search_phrase)

    browser = utils.get_browser()
    page = browser.get(GOOGLE)
    search_form = page.soup.select('form[name=f]')[0]
    search_form.select('input[name=q]')[0]['value'] = search_phrase
    search_form.select('input[name=tnI]')[0]['name'] = '' # hack so mechanicalsoup doesn't include I'm Feeling Lucky

    search_results = browser.submit(search_form, page.url)
    results_count = search_results.soup.find('div', id='resultStats').text.rstrip()
    needl.log.info('%s for %s', results_count, search_phrase)

    links = [link for link in search_results.soup.select('h3 > a') if link.get('href').startswith('/url')]

    if click_through and len(links) > 0:
        link = random.choice(links).get('href')

        if not utils.url_is_absolute(link):
            link = GOOGLE + link

        needl.log.info('Visiting %s', link)
        browser.get(link)