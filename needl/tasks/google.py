import needl, needl.schedule as schedule, needl.utils as utils

GOOGLE = needl.settings['google']['GOOGLE']


def register():
    # todo: ugly as hell
    se = needl.settings['google']['search_interval']
    args = map(int, se.split('..'))
    schedule.every(*args).minutes.do(search)


def search():
    search_phrase = utils.get_keywords(3)
    needl.log.info('Searching Google for: %s', search_phrase)

    browser = utils.get_browser()
    page = browser.get(GOOGLE)
    search_form = page.soup.select('form[name=f]')[0]
    search_form.select('input[name=q]')[0]['value'] = search_phrase

    try:
        search_form.select('input[name=btnI]')[0]['name'] = '' # hack so mechanicalsoup doesn't request I'm Feeling Lucky results
    except IndexError:
        pass

    search_results = browser.submit(search_form, page.url)
    results_count = search_results.soup.find('div', id='resultStats').text.rstrip()
    needl.log.debug('%s for %s', results_count, search_phrase)

    if needl.settings['google']['click_through']:
        links = [link for link in search_results.soup.select('h3.r > a') if utils.url_is_absolute(link.get('href'))]

        if len(links) > 0:
            link = needl.rand.choice(links).get('href')
            needl.log.info('Visiting %s', link)
            page = browser.get(link)

            click_depth = needl.settings['google']['click_depth']
            if click_depth > 0:
                utils.process_click_depth(browser, page, click_depth)
