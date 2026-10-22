import os
import needl, needl.schedule as schedule, needl.utils as utils
import requests

# Alexa was retired in 2022 and its S3 bucket no longer serves the list.
# The NetAPI Top 1M is a free daily list in the same rank,domain format.
TOP1M_URL = 'https://netapi.com/netapi_top1mln.csv'
CSV_NAME = 'top-1m.csv'


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
    browser.get(site)
    utils.process_click_depth(browser, needl.settings['alexa']['click_depth'])


def update():
    needl.log.info('Downloading top one million list (%s)', TOP1M_URL)
    file = requests.get(TOP1M_URL, timeout=300)
    file.raise_for_status()

    # drop the header line, so every line is rank,domain as before
    lines = file.text.splitlines()[1:]
    with open(os.path.join(needl.args.datadir, CSV_NAME), 'w') as f:
        f.write('\n'.join(lines) + '\n')
