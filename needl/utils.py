import os, re, time
import urllib.parse as url
from selenium import webdriver
import needl


def generate_wordlist(wordfile=None, min_length=5, max_length=20):
    words = []
    regexp = re.compile("^%s{%i,%i}$" % ('.', min_length, max_length))
    wordfile = os.path.expanduser(wordfile)

    with open(wordfile) as wordlist:
        for line in wordlist:
            thisword = line.strip()

            if regexp.match(thisword) is not None:
                words.append(thisword)

    return words


def get_word(words):
    return needl.rand.choice(needl.rand.choice(words))


def get_keywords(num=3, separator=' '):
    data = os.getcwd() + '/data/'
    words = [generate_wordlist(data + '/adjectives.txt'),
             generate_wordlist(data + '/nouns.txt'),
             generate_wordlist(data + '/verbs.txt')]

    return ' '.join([get_word(words) for _ in range(num)])


def get_line(file):
    with open(file) as f:
        line = next(f)

        for num, aline in enumerate(f):
            if needl.rand.randrange(num + 2): continue
            line = aline

        return line.rstrip()


def url_is_absolute(link):
    return bool(url.urlparse(link).netloc)


def get_browser():
    chromedriver = os.path.join(needl.args.datadir, 'chromedriver')
    if not os.path.exists(chromedriver):
        raise FileNotFoundError("Could not find chromedriver executable at %s. Download it for your platform at https://chromedriver.storage.googleapis.com/index.html?path=2.33/", chromedriver)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1024x3000')
    chrome_options.add_argument("user-agent=" + get_line(os.path.join(needl.args.datadir, 'user-agents.txt')))

    return webdriver.Chrome(executable_path=chromedriver, chrome_options=chrome_options)


def process_click_depth(browser, click_depth=None):
    if click_depth:
        i = click_depth if is_int(click_depth) else needl.rand.randrange(int(click_depth.split('..')[0]), int(click_depth.split('..')[1]) + 1)
        needl.log.debug('Clicking through %s %i times', browser.current_url, i)

        for _ in range(i):
            links = browser.find_elements_by_xpath("//a[@href]")

            if len(links) > 0:
                link = needl.rand.choice(links).get_attribute('href')

                if not url_is_absolute(link):
                    link = url.urljoin(browser.current_url, link)

                try:
                    needl.log.info('Visiting %s', link)
                    browser.get(link)

                    if (_ + 1) < i:
                        sleep_time = needl.settings['sleep_between_requests']

                        if sleep_time:
                            sleep_time = sleep_time if is_int(sleep_time) else needl.rand.uniform(int(sleep_time.split('..')[0]), int(sleep_time.split('..')[1]))
                            needl.log.debug('Sleeping for %fms before next request', sleep_time)
                            time.sleep(sleep_time / 1000.0)

                except Exception as e:
                    needl.log.debug('Failed to visit %s: %s', link, e)
            else:
                needl.log.debug('Site %s has no links to follow, skipping', browser.current_url)
                break


def is_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False