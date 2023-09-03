import datetime
import os
import time
import traceback

from jinja2 import Environment, FileSystemLoader
from libs.applicationlogs import ApplicationLogs
from libs.calculatingdiff import CalculatingDifference
from libs.configreader import Configreader
from libs.datacrud import Datacrud
from libs.sendmessage import SendMessage
from libs.snspost import SnsPost
from libs.textprocessing import TextProcessing
from tqdm import tqdm

from .gettrendwords import GetTrendWords


class ArticlePosting:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.calculate = CalculatingDifference(mode)
        self.datacrud = Datacrud(mode, destinationtype)
        self.snspost = SnsPost(mode)
        self.sendmessage = SendMessage(mode)
        self.textprocessing = TextProcessing(mode)
        self.hatenauser = self.config.get_snsauth("hatena")["user_name"]
        self.contents_template = self.config.get_filepath("bloggertemplate")
        self.trendwords_template = self.config.get_filepath("trendwordtemplate")
        self.wordcloud_path = self.config.get_filepath("wordcloudpath")
        self.trendwords = GetTrendWords(mode)
        self.twitterauth = self.config.get_snsauth("twitter")
        self.mail_template = self.config.get_filepath("mailtemplate")
        self.destinationtype = destinationtype
        self.jpn_stopwords = self.textprocessing.get_japanese_stopwords()
        self.en_stopwords = self.textprocessing.get_english_stopwords()

    """ Submit articles with time differences """

    def interval_post(self, contents: list = None, wait_time: int = None) -> bool:
        try:
            # Retrieve articles for posting from list
            record_count = len(contents)
            for content in tqdm(contents):
                if content.keys() >= {"_id", "title", "link", "category"}:
                    tags = []
                    # Extract target articles
                    keyid = content["_id"]
                    posttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    postword = "#うひーメモ" + "\r\n" + posttime + "\r\n" + content["title"]
                    url = content["link"]
                    tags.append(content["category"])
                    if "addlabel" in content and content["addlabel"] is not None:
                        tags.extend(content["addlabel"])
                    # Check dupulicate hatena
                    dup_check_result = self.snspost.duplicate_check_hateb(
                        url, self.hatenauser
                    )
                    update_condition = {"_id": keyid}
                    if dup_check_result:
                        duplicatereplace = {"$set": {"dupucheck": "DUPULECATE"}}
                        self.datacrud.update_data(update_condition, duplicatereplace)
                    else:
                        if self.mode == "test" or self.destinationtype == "text":
                            self.snspost.post_text_microblog(postword, url, tags)
                        else:
                            # Post Hatena and Slack
                            self.snspost.post_hateb(postword, url, tags)
                            tagstr = " ".join(["#" + t for t in tags])
                            slack_content = f"{postword}\n{url}\n{tagstr}"
                            self.sendmessage.send_message_slack(slack_content)
                        # Rewrite status
                        statusreplace = {"$set": {"poststatus": "POSTED"}}
                        self.datacrud.update_data(update_condition, statusreplace)
                        if wait_time is not None:
                            time.sleep(wait_time)
                        else:
                            time.sleep(
                                self.calculate.get_intervaltime(reccount=record_count)
                            )
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("interval post exception!!")

    """ Merge and submit multiple articles """

    def summary_post(
        self, contents: list, template_filepath: str, title_prefix: str
    ) -> bool:
        try:
            record_count = len(contents)
            if record_count == 0:
                return
            directory, filename = os.path.split(template_filepath)
            env = Environment(loader=FileSystemLoader(directory))
            temp_html = env.get_template(filename)
            prechr = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
            post_blogger_body = temp_html.render({"items": contents})
            title = f"{title_prefix}{prechr}分まとめ({record_count}件)"

            if self.mode == "test" or self.destinationtype == "text":
                self.snspost.post_text_blogger(record_count, title, post_blogger_body)
            else:
                self.snspost.post_blogger(record_count, title, post_blogger_body)
            # status update
            for content in contents:
                if content.keys() >= {"_id", "title", "link", "category"}:
                    keyid = content["_id"]
                    update_condition = {"_id": keyid}
                    statusreplace = {"$set": {"poststatus": "bloggerdone"}}
                    self.datacrud.update_data(update_condition, statusreplace)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("summary post exception!!")

    """ Check for trending words in submitted articles """

    def checkwords_in_submitted(self, trendwords: list) -> bool:
        try:
            target_contents_condition = {
                "$and": [{"labelstat": "added"}, {"poststatus": "bloggerdone"}]
            }
            target_contents = self.datacrud.read_data(target_contents_condition)
            check_trendwords = [trendword["title"] for trendword in trendwords]
            for target_content in tqdm(target_contents):
                if target_content.keys() >= {
                    "_id",
                    "title",
                    "description",
                    "link",
                    "category",
                }:
                    content = target_content["description"]
                    trend_check = self.textprocessing.check_word_include(
                        check_trendwords, content, self.jpn_stopwords
                    )
                    if trend_check:
                        update_condition = {"_id": target_content["_id"]}
                        trendword_update_value = {
                            "$set": {
                                "trendwordstatus": "subject",
                                "hitwords": trend_check,
                            }
                        }
                        self.datacrud.update_data(
                            update_condition, trendword_update_value
                        )
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("checkwords in submitted exception!!")

    """ Trending Article Generation and send message """

    def trending_article_sending(
        self, trendword_contents: list, template_filepath: str
    ) -> bool:
        try:
            trendword_condition = {
                "$and": [{"trendwordstatus": "subject"}, {"poststatus": "bloggerdone"}]
            }
            target_contents = self.datacrud.read_data(trendword_condition)
            posttime = datetime.datetime.now().strftime("%Y-%m-%d %H:00")
            subject = f"トレンドワードヒット記事{posttime}分"
            directory, filename = os.path.split(template_filepath)
            env = Environment(loader=FileSystemLoader(directory))
            temp_mail = env.get_template(filename)
            template_data = {
                "trends": trendword_contents,
                "items": target_contents,
            }
            mail_body = temp_mail.render(**template_data)
            targetaddress = "ujimasa@hotmail.com"
            # sending mail
            if self.mode == "prod":
                self.sendmessage.send_mail_smtp(targetaddress, subject, mail_body)
            else:
                self.sendmessage.test_result_write(targetaddress, subject, mail_body)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("checkwords in submitted exception!!")

    """ Create WordCloud and update status after submission """

    def create_post_wordcloud(self) -> bool:
        try:
            wordcloud_condition = {"poststatus": "bloggerdone"}
            wordcloud_contents = self.datacrud.read_data(wordcloud_condition)
            record_count = sum(1 for _ in wordcloud_contents)
            wordcloud_sources = []
            for wordcloud_content in tqdm(wordcloud_contents):
                if wordcloud_content.keys() >= {
                    "_id",
                    "title",
                    "description",
                    "link",
                    "category",
                }:
                    wordcloud_sources.append(wordcloud_content["description"])
                    wordcloud_update_condition = {"_id": wordcloud_content["_id"]}
                    wordcloud_update_value = {"$set": {"wordcloud": "completed"}}
                    self.datacrud.update_data(
                        wordcloud_update_condition, wordcloud_update_value
                    )
            self.textprocessing.generate_wordcloud(
                wordcloud_sources,
                self.wordcloud_path,
                self.jpn_stopwords,
                self.en_stopwords,
            )
            wordcloudfiles = [
                self.wordcloud_path + "jp_wordcloud.png",
                self.wordcloud_path + "en_wordcloud.png",
            ]
            postdate = datetime.datetime.now().strftime("%Y-%m-%d")
            title = f"WordCloud{postdate}分"
            post_blogger_body = f"{postdate}分記事のワードクラウド"
            tag = ["WordCloud"]
            url = ""
            if self.mode == "test" or self.destinationtype == "text":
                self.snspost.post_text_blogger(record_count, title, post_blogger_body)
                self.snspost.post_text_microblog(title, url, tag)
            else:
                self.snspost.post_blogger(
                    record_count, title, post_blogger_body, wordcloudfiles
                )
                for wordcloudfile in wordcloudfiles:
                    self.snspost.post_twitter(title, url, tag, wordcloudfile)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("create post wordcloud exception!!")

    """ Post articles to twitter and hatena and blogger """

    def main(self, wc_post_time: int = 23):
        try:
            starttime = time.perf_counter()

            trendword_title = "トレンドワード"
            contents_title = "RSSフィード"
            articles = self.datacrud.read_data({})
            count_record_contents = len(articles)
            if count_record_contents > 0:
                # Get trendwords contents
                trendwords_contents = self.trendwords.main()
                self.summary_post(
                    trendwords_contents, self.trendwords_template, trendword_title
                )
                # hatena and twitter contents
                hatena_slack_condition = {
                    "$and": [
                        {"labelstat": "added"},
                        {"poststatus": {"$ne": "bloggerdone"}},
                    ]
                }
                interval_contents = self.datacrud.read_data(hatena_slack_condition)
                self.interval_post(interval_contents)
                # blogger contents
                blogger_condition = {
                    "$and": [
                        {"labelstat": "added"},
                        {"dupkey": {"$ne": "DUPULECATE"}},
                        {"poststatus": "POSTED"},
                    ]
                }
                # blogger post
                blogger_contents = self.datacrud.read_data(blogger_condition)
                self.summary_post(
                    blogger_contents, self.contents_template, contents_title
                )
                # Trend Word Email Sending
                self.checkwords_in_submitted(trendwords_contents)
                self.trending_article_sending(trendwords_contents, self.mail_template)
                operate_count = sum(1 for _ in trendwords_contents) + sum(
                    1 for _ in interval_contents
                )
                # If it's 23:00, create WordCloud
                now = datetime.datetime.now()
                if now.hour == wc_post_time:
                    self.create_post_wordcloud()

                endtime = time.perf_counter()
                processtime = endtime - starttime
                self.applog.output_log(
                    "INFO", f"処理時間:{processtime}秒  処理件数:{operate_count}件"
                )
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("ArticlePosting exception!!")
