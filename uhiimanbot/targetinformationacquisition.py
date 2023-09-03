import datetime
import html
import itertools
import random
import time
import traceback
import urllib
from concurrent.futures import ThreadPoolExecutor

import feedparser
from libs.applicationlogs import ApplicationLogs
from libs.configreader import Configreader
from libs.datacrud import Datacrud
from libs.textprocessing import TextProcessing
from tqdm import tqdm


class TargetInformationAcquisition:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.textprocessing = TextProcessing(mode)
        self.datacrud = Datacrud(mode, destinationtype)
        self.destinationtype = destinationtype

    """ rssfeed getting operating process """

    def get_rssfeed(self, feedinfo: dict = None, timedifference: int = 1):
        try:
            keys = [
                "name",
                "category",
                "title",
                "description",
                "link",
                "orgdescription",
                "orgpublished",
                "published",
                "updated",
            ]
            try:
                feed = feedparser.parse(
                    feedinfo["feedurl"],
                    response_headers={"content-type": "text/xml; charset=utf-8"},
                )
            except urllib.error.URLError:
                feed = ""
                self.applog.output_log(
                    "WARNING", "エラーURL:{0}".format(feedinfo["feedurl"])
                )
            if feed:
                result = []
                for entry in tqdm(feed.entries):
                    name = feedinfo["name"]
                    category = feedinfo["category"]
                    if entry.keys() >= {
                        "title",
                        "links",
                        "published",
                        "published_parsed",
                    }:
                        title = html.escape(entry.title)
                        link = entry.links[0]
                        description = ""
                        org_description = ""
                        if "summary" in entry:
                            description = self.textprocessing.clean_text(entry.summary)
                            org_description = entry.summary
                        # Time Zone Control
                        published = datetime.datetime.now()
                        updated = published
                        if len(entry.published) != 0 and "+" in entry.published:
                            tzdecision = entry.published.split("+")[1]
                            plushour = datetime.timedelta(hours=int(tzdecision[1]))
                            tz = datetime.timezone(plushour)
                            nowtime = datetime.datetime.now(tz)
                            orgpublished = entry.published
                            published = (
                                datetime.datetime(
                                    *entry.published_parsed[:6], tzinfo=tz
                                )
                                + plushour
                            )
                            updated = (
                                datetime.datetime(*entry.published_parsed[:6])
                                + plushour
                            )
                            # Obtain only data for which the difference between
                            # the current time and the posting time is the
                            # specified time
                            if abs(nowtime - published) < datetime.timedelta(
                                hours=timedifference
                            ):
                                value = [
                                    name,
                                    category,
                                    title,
                                    description,
                                    link["href"],
                                    org_description,
                                    orgpublished,
                                    published.strftime("%Y-%m-%d %H:%M:%S"),
                                    updated.strftime("%Y-%m-%d %H:%M:%S"),
                                ]
                                result.append(dict(zip(keys, value)))
                return result
            else:
                self.applog.output_log(
                    "WARNING", "エントリー取得不可URL:{0}".format(feedinfo["feedurl"])
                )
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get rssfeed exception!!")

    """ Rssfeed getting multi thread """

    def get_rssfeeds(self, workcount: int = 20, settingtime: int = 1):
        starttime = time.perf_counter()
        try:
            feedlists = self.config.get_rss_feed()
            keys = ["name", "feedurl", "category"]
            feeddicts = [dict(zip(keys, item)) for item in feedlists]
            size = len(feedlists)
            self.applog.output_log("INFO", "RSSフィード数:{0}件".format(size))
            settingtimes = []

            for s in range(size):
                settingtimes.append(settingtime)

            with ThreadPoolExecutor(max_workers=workcount) as executor:
                r = list(executor.map(self.get_rssfeed, feeddicts, settingtimes))
            result = [e for e in r if e]

            endtime = time.perf_counter()
            processtime = endtime - starttime
            self.applog.output_log("INFO", "処理時間:{0}秒".format(processtime))
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get rssfeeds exception!!")

    """ Output rss feed data """

    def store_postsdata(self, datas: list = None):
        result = True
        try:
            if len(datas) != 0:
                for data in datas:
                    if isinstance(data, dict):
                        if self.destinationtype != "mongo":
                            current_time = datetime.datetime.now()
                            random_number = random.randint(1, 100)
                            key_id = (
                                f"{current_time.strftime('%Y%m%d%H%M%S')}-"
                                f"{random_number}"
                            )
                            data["_id"] = key_id
                        self.datacrud.create_data(data)
                    else:
                        self.store_postsdata(data)
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("Store data exception!!")

    def main(self, intervaltime: int = 1):
        try:
            rssdatas = list(
                itertools.chain.from_iterable(
                    self.get_rssfeeds(settingtime=intervaltime)
                )
            )
            result = self.store_postsdata(rssdatas)
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("TargetInformationAcquisition exception!!")
