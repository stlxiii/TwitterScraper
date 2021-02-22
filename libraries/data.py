class _locators(object):
    def __init__(self) -> None:
        
        self.show_replies     = '//*[.="Show replies"]'
        self.show_more_replies= '//*[.="Show more replies"]'
        self.annoying_overlay = 'css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0'
        self.tweet            = '//div[@class="css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0"]'
        self.reply_to         = './../..//*[@class="css-901oao r-9ilb82 r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-qvutc0"]'
        self.full_name        = './../../..//*[@class="css-901oao css-bfa6kz r-1fmj7o5 r-1qd0xha r-a023e6 r-b88u0q r-ad9z0x r-bcqeeo r-3s2u2q r-qvutc0"]'
        self.short_name       = './../../..//div[@class="css-1dbjc4n r-18u37iz r-1wbh5a2 r-1f6r7vd"]'
        self.reply_url        = './../../..//a[contains(@href, "/status/")]'
        self.datetime         = './../../..//time'

        self.first_tweet      = '(//article)[1]'
        self.last_tweet       = '(//article)[last()]'

