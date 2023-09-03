# import datetime
# import itertools
# import re
import time
import traceback

import feedparser
from libs.applicationlogs import ApplicationLogs
from libs.configreader import Configreader
from requests_oauthlib import OAuth1Session


class GetTrendWords:
    def __init__(self, mode: str = "prod"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)

    # """ Get Twitter Trends """

    # def get_trends_twitter(self, twitter: object = None, location: dict = None):
    #     try:
    #         trends_url = "https://api.twitter.com/1.1/trends/place.json"
    #         results = []
    #         keys = ["category", "name", "title", "volume", "link", "published"]
    #         req = twitter.get(trends_url, params=location)
    #         for trend in req.json()[0]["trends"]:
    #             category = "Twitter Trend"
    #             name = "Trend Words"
    #             title = re.sub("#", "", trend["name"])
    #             qurl = trend["url"]
    #             if trend["tweet_volume"] is not None:
    #                 volume = trend["tweet_volume"]
    #             else:
    #                 volume = 0
    #             gettime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             values = [category, name, title, volume, qurl, gettime]
    #             o = dict(zip(keys, values))
    #             results.append(o)
    #         if results:
    #             result = sorted(results, key=lambda x: int(x["volume"]), reverse=True)
    #             return result
    #         if req.status_code != 200:
    #             loglevel = "ERROR"
    #             errorinfo = req.status_code + " " + req.headers + " " + req.text
    #             self.applog.output_log(loglevel, errorinfo)
    #     except Exception:
    #         self.applog.output_log(self.loglevel, traceback.format_exc())
    #         raise Exception("twittertrends exception!!")

    """ Get Google Trends """

    def get_trends_gtrend(self, url: str = None) -> list:
        try:
            results = []
            keys = ["category", "name", "title", "volume", "link", "published"]
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if entry is not None:
                    if entry.keys() >= {
                        "title",
                        "ht_approx_traffic",
                        "published_parsed",
                    }:
                        values = [
                            "Google Trend",
                            "Trend Words",
                            entry.title,
                            entry.ht_approx_traffic.replace("+", "").replace(",", ""),
                            entry.ht_news_item_url,
                            time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed),
                        ]
                        o = dict(zip(keys, values))
                        results.append(o)
            if results:
                results = sorted(results, key=lambda x: int(x["volume"]), reverse=True)
            return results
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("Googletrends exception!!")

    def main(self, authinfo: dict = None):
        try:
            starttime = time.perf_counter()
            # GoogleTrend
            jp_trendsurl = (
                "https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=JP"
            )
            us_trendsurl = (
                "https://trends.google.co.jp/trends/trendingsearches/daily/rss?geo=US"
            )
            jpngtrends = self.get_trends_gtrend(jp_trendsurl)
            engtrends = self.get_trends_gtrend(us_trendsurl)

            # TwitterTrend
            if authinfo is not None:
                twitterauth = authinfo
                twitteroauth = OAuth1Session(
                    twitterauth["consumer_key"],
                    twitterauth["consumer_secret"],
                    twitterauth["token"],
                    twitterauth["token_secret"],
                )
            # # Ref Yahoo! WOEIDs
            # # https://gist.github.com/salvadorgascon/fd9526674e02511261512eabdc01c4eb?fbclid=IwAR2Ch05UrXIRBFvdDWLFHw_ag1gKtk0b5meBTuXAZfY4bB6IFAwrDGgIlQQ
            # location = [{"id": 23424856}, {"id": 23424977}]  # JPN  # USA
            # twittertrends = [
            #     self.get_trends_twitter(twitteroauth, loc) for loc in location
            # ]
            # twittertrend = list(itertools.chain.from_iterable(twittertrends))
            # result = jpngtrends + engtrends + twittertrend

            result = jpngtrends + engtrends

            endtime = time.perf_counter()
            processtime = endtime - starttime
            self.applog.output_log("INFO", f"処理時間:{processtime}秒")
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get trendwords exception!!")

    if __name__ == "__main__":
        main()
