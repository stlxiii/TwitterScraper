import time, csv, os
from libraries.selenium import _selenium, _webelem
from libraries.data     import _locators
from libraries.config   import _config
from libraries.database import _tiny_db
from selenium.webdriver.remote.webelement import WebElement


b        = _selenium()
locators = _locators()
config   = _config()


def _main():
    done = False
    i    = 0

    while not done:
        i  += 1
        url = config.get_key('general', f'tweet{i}')
        if url is not None and url.lower()[:4] == 'http':
            print(f'Scraping {url}\n')
            save_all(url, scrape_tweets(url))
        else:
            done = True
    print('Work complete!')


def scrape_tweets(url):
    tweets = []
    try:
        b.create_firefox(url, headless=True)
        while not b.is_alive(): time.sleep(1)
        b.delete_class(locators.annoying_overlay)

        fails = 0
        while fails < 25 and b.is_alive():
            e:WebElement = None
            count_before = len(tweets)
            
            more_buttons = b.find_elements_by_xpath(locators.show_replies)
            more_buttons.append(b.find_elements_by_xpath(locators.show_more_replies))
            for i in more_buttons:
                _webelem(i).click()
            
            for e in b.find_elements_by_xpath(locators.tweet):
                add_tweet(tweets, url, e)
            
            if len(tweets) == count_before:
                fails += 1

            b.scroll_with_keypress(locators.first_tweet)
            time.sleep(1)

            if fails == 10 or fails == 15 or fails == 20:
                b.driver.refresh()
                time.sleep(10)

    except Exception as ex:
        print(ex)

    finally:
        b.quit()
        return tweets
        

def add_tweet(tweets:list, url:str, element:WebElement):
    try:
        e = _webelem(element)
        d = dict()

        if e.get_text() != '':
            d['conversation'] = url
            d['n_found']      = int(len(tweets)) + 1
            d['short_name']   = find_sub_element(e, locators.short_name, 'text')
            d['full_name']    = find_sub_element(e, locators.full_name,  'text')
            d['text']         = e.get_text()
            d['hash']         = hash(e.get_text())
            d['reply_to']     = find_sub_element(e, locators.reply_to,   'text')
            d['url']          = find_sub_element(e, locators.reply_url,  'href')
            d['datetime']     = find_sub_element(e, locators.datetime,   'datetime')

            if is_new(tweets, d['hash']) and d['text'] != '' and d['url'] != '':
                tweets.append(d)
                print(d)
                print('\n')

    finally:
        pass


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


def save_all(url:str, tweets:list):
    index       = url.rstrip()[:-1].rfind('/') + 1
    tweet_id    = url[index:]
    this_file   = os.path.dirname(os.path.abspath(__file__))
    csv_path    = os.path.join(this_file, 'export', f'{tweet_id}.csv')
    tdb_path    = os.path.join(this_file, 'db',     f'{tweet_id}.json')

    save_all_to_db(tdb_path, tweets)
    save_all_to_csv(csv_path, tweets)


def save_all_to_csv(path:str, tweets:list):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if len(tweets) > 0:
        with open(path, 'w', encoding='utf-8') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow(['datetime', 'short_name', 'full_name', 'reply_to', 'text', 'url'])
            for i in tweets:
                w.writerow([i['datetime'], i['short_name'], i['full_name'], i['reply_to'], i['text'], i['url']])


def save_all_to_db(name:str, tweets:list):
    db = _tiny_db(name, clear=True)

    if len(tweets) > 0:
        db.insert_multiple(tweets)


def save_text(file, text):
    try:
        with open(file, 'w') as f:
            f.write(text)
    except:
        pass


def is_new(tweets, hash) -> bool:
    for i in tweets:
        if i['hash'] == hash:
            return False
    return True

_main()