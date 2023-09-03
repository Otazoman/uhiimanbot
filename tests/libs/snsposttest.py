import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.configreader import Configreader
from libs.snspost import SnsPost


class TestSnsPosting(TestCase):
    mode = "test"
    arthiclepost = SnsPost(mode)
    responsecode = 401

    """ テスト投稿 """

    def test_post_text_microblog(self):
        teststr = """
        #うひーメモTEST
        https://google.co.jp

        #TwitterTEST
        #TwitterTEST2
        #TwitterTEST3
        https://bookmark.hatenaapis.com/rest/1/my/bookmark?url=https://google.co.jp&comment=[TwitterTEST][TwitterTEST2][TwitterTEST3]%23%E3%81%86%E3%81%B2%E3%83%BC%E3%83%A1%E3%83%A2TEST&private=1
        """
        print("\nPost test mode-->>")
        targetfile = Configreader(self.mode).get_filepath("intervalpost")
        # ファイルを綺麗にする
        with open(targetfile, "r+") as f:
            f.truncate(0)
        postword = "#うひーメモTEST"
        url = "https://google.co.jp"
        tags = ["TwitterTEST", "TwitterTEST2", "TwitterTEST3"]
        self.arthiclepost.post_text_microblog(postword, url, tags)
        with open(targetfile, "r") as f:
            result = f.read()
        self.assertEqual(result.strip(), teststr.replace(" ", "").strip())
        # ファイルを綺麗にする
        with open(targetfile, "r+") as f:
            f.truncate(0)

    """ Twitter単独投稿 """

    def test_post_twitter(self):
        print("Post twitter-->>")
        postword = "twitterうひーメモTEST"
        url = "https://google.co.jp"
        tags = ["TwitterTEST", "TwitterTEST2", "TwitterTEST3"]
        print("\n-->> Twitter")
        # 認証エラー
        print("-->> NonAuth")
        result = self.arthiclepost.post_hateb(postword, url, tags)
        self.assertEqual(result.status_code, self.responsecode)

        # 通常投稿
        print("-->> Auth not image")
        result = SnsPost("prod").post_twitter(postword, url, tags)

        # 画像付き投稿
        image_filepath = (
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/image3.png"
        )
        tags = ["WordCloud"]
        print("-->> Auth attatch image")
        result = SnsPost("prod").post_twitter(postword, url, tags, image_filepath)

    """ Hatena単独投稿 """

    def test_post_hateb(self):
        print("\n-->> Post hatena")
        postword = "#はてブうひーメモTEST"
        url = "https://google.co.jp"
        tags = ["hatenaTEST", "hatenaTEST2", "hatenaTEST3"]
        print("-->> Hatena")
        # 認証エラー
        print("-->> NonAuth")
        result = self.arthiclepost.post_hateb(postword, url, tags)
        self.assertEqual(result.status_code, self.responsecode)
        # 通常投稿
        print("-->> Auth")
        result = SnsPost("prod").post_hateb(postword, url, tags)

    """ Hatena重複チェック """

    def test_dupulicate_check_hateb(self):
        target_url = "https://google.co.jp"
        target_users = ["ISB", "norikoni831"]
        assumption_results = [True, False]
        print("\n-->> Normalcheck")
        for target_user, assumption_result in zip(target_users, assumption_results):
            result = self.arthiclepost.duplicate_check_hateb(target_url, target_user)
            self.assertEqual(result, assumption_result)
        # 例外
        print("-->> Exception")
        target_url = {"AAA": "BBB"}
        target_user = {"AAA": "BBB"}
        with self.assertRaises(Exception, msg="hatena check exception!!"):
            self.arthiclepost.duplicate_check_hateb(target_url, target_user)

    """ flickr画像投稿 """

    def test_post_flickr(self):
        print("\n-->> Post flickr")
        image_filepaths = [
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/image1.png"
        ]
        print("-->> flickr")
        # 認証エラー
        print("-->> NonAuth")
        with self.assertRaises(Exception, msg="Flickr post exception!!s"):
            self.arthiclepost.post_flickr(image_filepaths)
        # 通常投稿
        print("-->> Auth")
        result = SnsPost("prod").post_flickr(image_filepaths)
        checkword = "https://farm"
        self.assertTrue(all(checkword in url for url in result))

    """ テスト投稿 """

    def test_post_text_blogger(self):
        targetfile = Configreader(self.mode).get_filepath("summarypost")
        print("\nPost Blogger-->>")
        title = "Bloggerテスト"
        contents = "<h1>TEST</h1><br/><p>テストです</p>"
        count = 2
        print("\n-->> Blogger")
        # ファイルを綺麗にする
        with open(targetfile, "r+") as f:
            f.truncate(0)
        self.arthiclepost.post_text_blogger(count, title, contents)
        with open(targetfile, "r") as f:
            result = f.read()
        self.assertRegex(result, contents)
        # ファイルを綺麗にする
        with open(targetfile, "r+") as f:
            f.truncate(0)

    """ Blogger単独投稿 """

    def test_post_blogger(self):
        print("\nPost Blogger-->>")
        title = "Bloggerテスト"
        contents = "<h1>TEST</h1><br/><p>テストです</p>"
        count = 2
        print("\n-->> Blogger")
        print("-->> NoAuth")
        # 認証エラー
        with self.assertRaises(Exception, msg="blogger post exception!!"):
            self.arthiclepost.post_blogger(count, title, contents)
        # 通常投稿
        print("-->> Auth not images")
        SnsPost("prod").post_blogger(count, title, contents)
        # 画像付投稿
        print("-->> Auth add images")
        image_filepaths = [
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/image1.png",
            "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/image2.png",
        ]
        SnsPost("prod").post_blogger(count, title, contents, image_filepaths)
