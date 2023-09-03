import time
import traceback

import tweepy

from .applicationlogs import ApplicationLogs
from .calculatingdiff import CalculatingDifference
from .configreader import Configreader


class FollowbackTwitter:
    def __init__(self, mode: str = "prod"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.twitterauth = self.config.get_snsauth("twitter")
        self.calcuratediff = CalculatingDifference(mode)

    """ Parent account follower acquisition """

    def get_parent_follwers(self, api: object, screen_name: str):
        try:
            followers_ids = tweepy.Cursor(
                api.get_follower_ids, user_id=screen_name, cursor=-1
            ).items()
            result = [fw for fw in followers_ids]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get parent followers exception!!")

    """ Obtained back account followers """

    def get_my_follws(self, api: object, screen_name: str):
        try:
            follow_ids = tweepy.Cursor(api.get_follower_ids, id=screen_name).items()
            result = [fw for fw in follow_ids]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get my follows exception!!")

    """ Follow-up Execution """

    def follow_twitter(self, myname: str, api: object, user_ids: list):
        try:
            user_info = api.get_user(screen_name=myname)
            friend = int(user_info.friends_count)
            # Maximum number of followers
            i = 0
            if friend < 5000:
                for user in user_ids:
                    try:
                        msg = api.create_friendship(user_id=user)
                        self.applog.output_log("INFO", "{0}をフォローしました。".format(msg.name))
                        i += 1
                        time.sleep(10)
                    except tweepy.error.TweepError:
                        self.applog.output_log(self.loglevel, traceback.format_exc())
                        time.sleep(10)
                        continue
            return i
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get follow twitter exception!!")

    """ Oversight Functions """

    def main(self, myname: str, parentname: str):
        try:
            # setting twitter information
            auth = tweepy.OAuthHandler(
                self.twitterauth["consumer_key"],
                self.twitterauth["consumer_secret"],
            )
            auth.set_access_token(
                self.twitterauth["token"], self.twitterauth["token_secret"]
            )
            twitter = tweepy.API(auth, wait_on_rate_limit=True)
            parent_screen_name = parentname
            my_screen_name = myname
            # Extract and follow differences from parent account
            parent_follwers = self.get_parent_follwers(twitter, parent_screen_name)
            my_follws = self.get_my_follws(twitter, my_screen_name)
            followtargets = self.calcuratediff.get_diffids(parent_follwers, my_follws)
            if len(followtargets) == 0:
                self.applog.output_log("INFO", "フォロー対象は0件です。")
                return False
            result_num = self.follow_twitter(my_screen_name, twitter, followtargets)
            if result_num > 0:
                self.applog.output_log("INFO", "フォロー対象は{0}件です。".format(result_num))
                return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get follow twitter exception!!")
