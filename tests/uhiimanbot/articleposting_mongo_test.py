import datetime
import os
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

import articlepost_test_data
from libs.datacrud import Datacrud
from uhiimanbot.articleposting import ArticlePosting


class TestArticlePostingMongo(TestCase):
    def setUp(self):
        self.mode = "test"
        self.destinationtype = "mongo"
        self.articleposting = ArticlePosting(self.mode, self.destinationtype)
        self.datacrud = Datacrud(self.mode, self.destinationtype)

    def setUpDBandClearlog(self, contents):
        deletecondition = {}
        self.datacrud.delete_data(deletecondition)
        self.datacrud.create_data(contents)
        with open(articlepost_test_data.output_interval_filepath, mode="r+") as f:
            f.truncate(0)
        with open(articlepost_test_data.output_summary_filepath, mode="r+") as f:
            f.truncate(0)
        with open(articlepost_test_data.output_mail_filepath, mode="r+") as f:
            f.truncate(0)
        if os.path.exists(articlepost_test_data.wordcloud_filepath):
            os.remove(articlepost_test_data.wordcloud_filepath)

    """ タイミングを計っての投稿(はてな) """

    def test_interval_post(self):
        wait = 2
        matches_word = "うひーメモ"
        # 正常ケース(時間を設定するケース)
        print("\n-->> RegularCase set wait time")
        self.setUpDBandClearlog(articlepost_test_data.org_articles)
        # ステータス書込み確認
        self.articleposting.interval_post(
            articlepost_test_data.hatena_posted_content, wait
        )
        result = self.datacrud.read_data({})
        poststat = result[0]["poststatus"]
        self.assertEqual(poststat, "POSTED")
        # 投稿確認
        with open(articlepost_test_data.output_interval_filepath, mode="r") as f:
            output = f.read()
            self.assertRegex(output, matches_word)
        # 正常ケース(ランダム)
        print("-->> RegularCase random time")
        self.setUpDBandClearlog(articlepost_test_data.org_articles)
        self.articleposting.interval_post(contents=articlepost_test_data.org_articles)
        # ステータス書込み確認
        result = self.datacrud.read_data({})
        poststat = result[0]["poststatus"]
        self.assertEqual(poststat, "POSTED")
        # 投稿確認
        with open(articlepost_test_data.output_interval_filepath, mode="r") as f:
            output = f.read()
            self.assertRegex(output, matches_word)
        # 例外ケース
        print("-->> exception")
        with self.assertRaises(Exception, msg="interval post exception!!"):
            test = 1
            self.articleposting.interval_post(test)

    """ 複数件の記事を統合しての投稿(blogger) """

    def test_contents_summary_post(self):
        title = "RSSフィード"
        # 正常ケース(RSSフィード)
        print("\n-->> RegularCase(RSS)")
        self.setUpDBandClearlog(articlepost_test_data.org_articles)
        self.articleposting.summary_post(
            articlepost_test_data.org_articles,
            articlepost_test_data.rss_template,
            title,
        )
        # ステータス書込み確認
        result = self.datacrud.read_data({})
        poststat = result[1]["poststatus"]
        self.assertEqual(poststat, "bloggerdone")
        with open(articlepost_test_data.output_summary_filepath, mode="r+") as f:
            result = f.read()
            self.assertRegex(result, title)
            f.truncate(0)
        # 0件の場合
        contents = []
        print("-->> RegularCase(zero)")
        self.articleposting.summary_post(
            contents,
            articlepost_test_data.rss_template,
            title,
        )
        # 例外ケース
        print("-->> exception")
        with self.assertRaises(Exception, msg="contents summary post exception!!"):
            test = 1
            self.articleposting.contents_summary_post(test)

    def test_trendwords_summary_post(self):
        # 正常ケース(トレンドワード)
        title = "トレンドワード"
        print("\n-->> RegularCase(trendword)")
        self.articleposting.summary_post(
            articlepost_test_data.trendwords_data,
            articlepost_test_data.trendwords_template,
            title,
        )
        with open(articlepost_test_data.output_trendword_filepath, mode="r+") as f:
            result = f.read()
            self.assertRegex(result, title)
            f.truncate(0)
        # 0件の場合
        zero_content = []
        print("-->> RegularCase(zero)")
        self.articleposting.summary_post(
            zero_content, articlepost_test_data.trendwords_template, title
        )
        with open(articlepost_test_data.output_trendword_filepath, mode="r") as f:
            result = f.readlines()
        self.assertEqual(len(result), 0)
        # 例外ケース
        print("-->> exception")
        with self.assertRaises(Exception, msg="contents summary post exception!!"):
            test = 1
            self.articleposting.summary_post(test)

    """ トレンドワードに類似しているかの確認 """

    def test_checkwords_in_submitted(self):
        print("\n-->> RegularCase")
        self.setUpDBandClearlog(articlepost_test_data.before_blogger_contents)
        self.articleposting.checkwords_in_submitted(
            articlepost_test_data.trendwords_data
        )
        result = self.datacrud.read_data({})
        self.assertEqual(result, articlepost_test_data.checkwords_expected_result)
        print("-->> exception")
        with self.assertRaises(Exception, msg="checkwords in submitted exception!!"):
            test = 1
            self.articleposting.checkwords_in_submitted(test)

    """ トレンドワードが含まれる記事の一覧を抽出 """

    def test_trending_article_sending(self):
        print("\n-->> RegularCase")
        self.setUpDBandClearlog(articlepost_test_data.after_posted_contents)
        self.articleposting.trending_article_sending(
            articlepost_test_data.trendwords_data,
            articlepost_test_data.template_filepath,
        )
        mailaddress = "ujimasa@hotmail.com"
        subject = "トレンドワードヒット記事"
        trendword = "なでしこジャパン"
        content = "気になる、記になる"
        with open(articlepost_test_data.output_mail_filepath, mode="r+") as f:
            result = f.read()
            self.assertRegex(result, mailaddress)
            self.assertRegex(result, subject)
            self.assertRegex(result, trendword)
            self.assertRegex(result, content)
            f.truncate(0)
        print("-->> exception")
        with self.assertRaises(Exception, msg="checkwords in submitted exception!!"):
            test = 1
            self.articleposting.trending_article_sending(test)

    """ WordCloud作成のテスト """

    def test_create_post_wordcloud(self):
        # 条件合致して作成するケース
        print("\n-->> RegularCase")
        self.setUpDBandClearlog(articlepost_test_data.after_posted_contents)
        self.articleposting.create_post_wordcloud()
        result = self.datacrud.read_data({})
        self.assertEqual(result, articlepost_test_data.wordcloud_expected_result)
        self.assertTrue(
            os.path.exists(articlepost_test_data.wordcloud_filepath),
            f"File '{articlepost_test_data.wordcloud_filepath}' does not exist.",
        )
        # 条件合致せずに作成されないケース
        print("-->> NotMatch Case")
        self.setUpDBandClearlog(articlepost_test_data.nomatch_expected_result)
        self.articleposting.create_post_wordcloud()
        result = self.datacrud.read_data({})
        self.assertEqual(result, articlepost_test_data.nomatch_expected_result)
        self.assertFalse(
            os.path.exists(articlepost_test_data.wordcloud_filepath),
            f"File '{articlepost_test_data.wordcloud_filepath}' does not exist.",
        )
        # 例外
        print("-->> Exception")
        with self.assertRaises(Exception, msg="create post wordcloud exception!!"):
            test = 1
            self.articleposting.create_post_wordcloud(test)

    """ メイン関数のテスト """

    def test_main(self):
        # 正常ケース ワードクラウド動かない
        print("\n-->> RegularCase not hour 23")
        self.setUpDBandClearlog(articlepost_test_data.org_articles)
        result = self.articleposting.main()
        self.assertTrue(result)
        checkval = "bloggerdone"
        result = self.datacrud.read_data({})
        self.assertEqual(result[0]["poststatus"], checkval)
        # 正常ケース ワードクラウド動く
        print("-->> RegularCase wordcloud")
        now = datetime.datetime.now()
        cwtime = now.hour
        self.setUpDBandClearlog(articlepost_test_data.org_articles)
        result = self.articleposting.main(cwtime)
        self.assertTrue(result)
        checkval = "completed"
        result = self.datacrud.read_data({})
        self.assertEqual(result[0]["wordcloud"], checkval)
        self.assertTrue(
            os.path.exists(articlepost_test_data.wordcloud_filepath),
            f"File '{articlepost_test_data.wordcloud_filepath}' does not exist.",
        )
        # 不正な認証情報
        print("-->> Exception")
        with self.assertRaises(Exception, msg="ArticlePosting exception!!"):
            test = "aaa"
            test2 = "bbb"
            self.articleposting.main(test, test2)
