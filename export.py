import csv, os, pkg_resources
from   libraries.config   import _config
from   libraries.database import _tiny_db
pkg_resources.require("TinyDB==4.4.0")

config   = _config()


def _main():
    print('')
    done = False
    i    = 0

    while not done:
        i  += 1
        url = config.get_key('general', f'tweet{i}')
        if url is not None and url.lower()[:4] == 'http':
            tweets = get_saved_tweets(url)
            print(f'Exporting {len(tweets)} tweets for {url}\n')
            save_all(url, tweets)
        else:
            done = True
    print('Work complete!')


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
    csv_path    = os.path.join(this_file, 'export', f'{tweet_id}.csv')
    tdb_path    = os.path.join(this_file, 'db',     f'{tweet_id}.json')

    save_all_to_csv(csv_path, tweets)


def save_all_to_csv(path:str, tweets:list):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if len(tweets) > 0:
        with open(path, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_ALL)
            w.writerow(['datetime', 'short_name', 'full_name', 'reply_to', 'text', 'url'])
            for i in tweets:
                w.writerow([i['datetime'], i['short_name'], i['full_name'], i['reply_to'], i['text'], i['url']])


_main()