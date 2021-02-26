import time, os
from   libraries.selenium import _selenium, _webelem
from   libraries.data     import _locators
from   libraries.config   import _config
from   libraries.database import _tiny_db
from   selenium.webdriver.remote.webelement import WebElement


b        = _selenium()
locators = _locators()
config   = _config()


def _main():
    print('')
    done = False
    i    = 0

    while not done:
        i  += 1
        url = config.get_key('general', f'tweet{i}')
        if url is not None and url.lower()[:4] == 'http':
            old_tweets = get_saved_tweets(url)
            print(f'Scraping {url}\nPreviously saved: {len(old_tweets)}')
            print('Searching ... ')

            new_tweets = scrape_tweets(url, old_tweets)
            print('Done!')
            print(f'Found {len(new_tweets)} new tweet(s).\n')

            save_all(url, new_tweets)
        else:
            done = True
    print('Work complete!')


def scrape_tweets(url:str, saved_tweets:list):
    tweets = []
    try:
        b.create_firefox(url, headless=True)
        while not b.is_alive(): time.sleep(1)
        b.delete_class(locators.annoying_overlay)

        fails = 0
        while fails < 20 and b.is_alive():
            e:WebElement = None
            count_before = len(tweets)
            
            more_buttons = b.find_elements_by_xpath(locators.show_replies)
            more_buttons.append(b.find_elements_by_xpath(locators.show_more_replies))
            for i in more_buttons:
                _webelem(i).click()
            
            for e in b.find_elements_by_xpath(locators.tweet):
                add_tweet(saved_tweets, tweets, url, e)
            
            if len(tweets) == count_before:
                fails += 1

            b.scroll_with_keypress(locators.first_tweet)
            time.sleep(1)

    except Exception as ex:
        print(ex)

    finally:
        b.quit()
        return tweets
        

def add_tweet(saved_tweets:list, tweets:list, url:str, element:WebElement):
    e = _webelem(element)
    d = dict()

    if e.get_text() != '':
        d['conversation'] = url
        d['short_name']   = find_sub_element(e, locators.short_name, 'text')
        d['full_name']    = find_sub_element(e, locators.full_name,  'text')
        d['text']         = e.get_text()
        d['reply_to']     = find_sub_element(e, locators.reply_to,   'text')
        d['url']          = find_sub_element(e, locators.reply_url,  'href')
        d['datetime']     = find_sub_element(e, locators.datetime,   'datetime')

        if d['text'] != '' and d['url'] != '' and is_new(saved_tweets+tweets, d['url']):
            tweets.append(d)


def find_sub_element(e:_webelem, locator, what:str):
    try:
        ee = e.find_element_by_xpath(locator)
        if what.lower() == 'text':
            return ee.get_text()
        else:
            return ee.get_attribute(what)
    except Exception as ex:
        if not 'NoneType' in str(ex):
            print(f'Error looking for {locator} : {ex}')
        return ''


def is_new(tweets, url) -> bool:
    for i in tweets:
        if i['url'] == url:
            return False
    return True


def get_saved_tweets(url):
    index       = url.rstrip()[:-1].rfind('/') + 1
    tweet_id    = url[index:]
    this_file   = os.path.dirname(os.path.abspath(__file__))
    tdb_path    = os.path.join(this_file, 'db', f'{tweet_id}.json')

    db = _tiny_db(tdb_path)
    return db.all()


def save_all(url:str, tweets:list):
    index       = url.rstrip()[:-1].rfind('/') + 1
    tweet_id    = url[index:]
    this_file   = os.path.dirname(os.path.abspath(__file__))
    tdb_path    = os.path.join(this_file, 'db',     f'{tweet_id}.json')

    save_all_to_db(tdb_path, tweets)


def save_all_to_db(name:str, tweets:list):
    db = _tiny_db(name)

    if len(tweets) > 0:
        db.insert_multiple(tweets)


def save_text(file, text):
    try:
        with open(file, 'w') as f:
            f.write(text)
    except:
        pass


_main()