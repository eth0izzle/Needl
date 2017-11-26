import needl, needl.schedule as schedule, needl.utils as utils

GOOGLE = needl.settings['google']['base_url']


def register():
    # todo: ugly as hell
    se = needl.settings['google']['search_interval']
    args = map(int, se.split('..'))
    schedule.every(*args).minutes.do(search)


def search():
    search_phrase = utils.get_keywords(3)
    needl.log.info('Searching Google for: %s', search_phrase)

    browser = utils.get_browser()
    browser.get(GOOGLE)
    search_form = browser.find_element_by_id('tsf')
    browser.find_elements_by_css_selector('input[name=q]')[0].send_keys(search_phrase)
    search_form.submit()

    results_count = browser.find_element_by_id('resultStats').text.rstrip()
    needl.log.debug('%s for %s', results_count, search_phrase)

    if needl.settings['google']['click_through']:
        links = [link for link in browser.find_elements_by_css_selector('h3.r > a') if utils.url_is_absolute(link.get_attribute('href'))]

        if len(links) > 0:
            link = needl.rand.choice(links).get_attribute('href')
            needl.log.info('Visiting %s', link)
            browser.get(link)

            click_depth = needl.settings['google']['click_depth']
            if click_depth > 0:
                utils.process_click_depth(browser, click_depth)

    browser.quit()