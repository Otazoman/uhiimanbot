import pathlib
import sys

import tweepy

sys.path.append("..")
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.configreader import Configreader
from libs.followbacktwitter import FollowbackTwitter


class TestFollowbackTwitter(TestCase):
    conf = Configreader("prod")
    twitterauth = conf.get_snsauth("twitter")
    auth = tweepy.OAuthHandler(
        twitterauth["consumer_key"],
        twitterauth["consumer_secret"],
    )
    auth.set_access_token(twitterauth["token"], twitterauth["token_secret"])
    twitter = tweepy.API(auth, wait_on_rate_limit=True)
    parent_screen_name = twitterauth["parent_screen_name"]
    my_screen_name = twitterauth["my_screen_name"]
    mode = "test"
    followbacktwitter = FollowbackTwitter(mode)

    """ 親アカウントのフォロワー取得 """

    def test_get_parent_follwers(self):
        result = self.followbacktwitter.get_parent_follwers(
            self.twitter, self.parent_screen_name
        )
        self.assertIsInstance(result, list)

    """ 子アカウントのフォロー取得 """

    def test_get_my_follws(self):
        result = self.followbacktwitter.get_parent_follwers(
            self.twitter, self.my_screen_name
        )
        self.assertIsInstance(result, list)

    """ フォロー """

    def test_follow_twitter_test(self):
        ids = [123, 234, 567]
        with self.assertRaises(Exception, msg="get follow twitter exception!!"):
            self.self.followbacktwitter.follow_twitter(
                self.my_screen_name, self.twitter, ids
            )

    """ 全体のテスト """

    def test_main(self):
        mode = "prod"
        followbacktwitter = FollowbackTwitter(mode)
        result = followbacktwitter.main(self.my_screen_name, self.parent_screen_name)
        self.assertEqual(False, result)
