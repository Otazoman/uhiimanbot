import base64
import datetime
import json
import os
import re
import traceback
import urllib
import xml.etree.ElementTree as ET

import flickrapi
import httplib2
import requests
from atproto import Client, models
from googleapiclient.discovery import build
from oauth2client import file, tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage as OAuth2Storage
from requests_oauthlib import OAuth1, OAuth1Session

from .applicationlogs import ApplicationLogs
from .configreader import Configreader
from .datacrud import Datacrud


class SnsPost:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.datacrud = Datacrud(mode, destinationtype)
        self.twitterauth = self.config.get_snsauth("twitter")
        self.blueskyauth = self.config.get_snsauth("bluesky")
        self.hatenaauth = self.config.get_snsauth("hatena")
        self.flickrauth = self.config.get_snsauth("flickr")
        self.bloggerauth = self.config.get_snsauth("blogger")

    """ Posted localtest twitter and hatena """

    def post_text_microblog(
        self, postword: str = None, url: str = None, tags: list = None
    ):
        try:
            filepath = self.config.get_filepath("intervalpost")
            # twitter
            tagstr = ""
            for t in tags:
                if len(postword + tagstr) < 140:
                    tagstr = tagstr + "\n#" + t
            content = postword + "\r\n" + url + "\r\n" + tagstr
            # Hatena
            posturl = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"
            tagstr = ""
            for t in tags:
                tagstr = tagstr + "[" + urllib.parse.quote_plus(t) + "]"
            bookmark_api_url = (
                posturl
                + "?url="
                + url
                + "&comment="
                + tagstr
                + urllib.parse.quote(postword)
                + "&private=1"
            )
            with open(filepath, mode="a") as f:
                f.write(content)
                f.write("\n")
                f.write(bookmark_api_url)
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("localtest post exception!!")

    """ Posted Twitter """

    def post_twitter(
        self,
        postword: str = None,
        url: str = None,
        tags: list = None,
        imagepath: str = None,
    ):
        try:
            # Setting api information (twitter API v2)
            twitter = OAuth1Session(
                self.twitterauth["consumer_key"],
                self.twitterauth["consumer_secret"],
                self.twitterauth["token"],
                self.twitterauth["token_secret"],
            )
            # post apis
            comment_post_url = "https://api.twitter.com/2/tweets"
            image_post_url = "https://upload.twitter.com/1.1/media/upload.json"
            # Building post content
            if imagepath:
                with open(imagepath, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode("utf-8")
                media_data = {"media_data": image_data}
                upload_response = twitter.post(image_post_url, data=media_data)
                media_id = upload_response.json()["media_id_string"]
                tweet_params = {
                    "text": postword + "\r\n" + f"#{tags[0]}",
                    "media": {"media_ids": [media_id]},
                }
                req = twitter.post(comment_post_url, json=tweet_params)
            else:
                tagstr = ""
                for t in tags:
                    if len(postword + tagstr) < 140:
                        tagstr = tagstr + "\n#" + t
                content = postword + "\r\n" + url + "\r\n" + tagstr
                tweet = {"text": content}
                req = twitter.post(comment_post_url, json=tweet)
            if req.status_code != 201:
                loglevel = "ERROR"
                errorinfo = (
                    str(req.status_code)
                    + " "
                    + json.dumps(dict(req.headers))
                    + " "
                    + req.text
                )
                self.applog.output_log(loglevel, errorinfo)
            return req
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("twitter post exception!!")
        finally:
            twitter.close()

    """ Posted Bluesky """

    def post_bluesky(
        self,
        postword: str = None,
        url: str = None,
        tags: list = None,
        content: object = None,
        imagepath: str = None,
    ):
        try:
            # post apis
            bluesky = Client()
            bluesky.login(
                self.blueskyauth["user_name"], self.blueskyauth["app_password"]
            )

            # Building post content
            if imagepath:
                
                with open(imagepath, "rb") as image_file:
                    image_data = image_file.read()
                media_data = image_data
                text = (postword + "\r\n" + f"#{tags[0]}",)

                req = bluesky.send_image(text=text, image=media_data, image_alt=tags[0])
                print(req)

            else:
                title = content["title"]
                description = content["description"]
                tagstr = "\n".join(["#" + t for t in tags])
                content = postword + "\r\n" + tagstr
                embed_external = models.AppBskyEmbedExternal.Main(
                    external=models.AppBskyEmbedExternal.External(
                        title=title, description=description, uri=url
                    )
                )
                req = bluesky.send_post(content, embed=embed_external)
                print(req)

        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("bluesky post exception!!")

    """ Posted HatenaBookmark """

    def post_hateb(self, postword: str = None, url: str = None, tags: list = None):
        try:
            # setting api information
            posturl = "https://bookmark.hatenaapis.com/rest/1/my/bookmark"
            hatena = OAuth1(
                self.hatenaauth["consumer_key"],
                self.hatenaauth["consumer_secret"],
                self.hatenaauth["token"],
                self.hatenaauth["token_secret"],
            )
            # Building post content
            tagstr = ""
            for t in tags:
                tagstr = tagstr + "[" + urllib.parse.quote_plus(t) + "]"
            # Call hatena api
            bookmark_api_url = (
                posturl
                + "?url="
                + url
                + "&comment="
                + tagstr
                + urllib.parse.quote(postword)
                + "&private=1"
            )
            req = requests.post(bookmark_api_url, auth=hatena)
            if req.status_code != 200:
                loglevel = "ERROR"
                errorinfo = (
                    str(req.status_code)
                    + " "
                    + json.dumps(dict(req.headers))
                    + " "
                    + req.text
                )
                self.applog.output_log(loglevel, errorinfo)
            return req
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("hatena post exception!!")
        finally:
            req.close()

    """ Dupulicate hatenabookmark post """

    def duplicate_check_hateb(
        self, check_target_url: str, check_target_user: str
    ) -> bool:
        try:
            checker_url = "http://b.hatena.ne.jp/entry/json/?url="
            target_url = urllib.parse.quote(check_target_url)
            res = requests.get(checker_url + target_url)

            if res.status_code != 200:
                res_msg = (
                    f"statuscode:{res.status_code},"
                    f"header:{res.headers},"
                    f"response:{res.text}"
                )
                self.applog.output_log("ERROR", res_msg)
                return False

            if res.text == "null":
                return False

            res_bookmarks = json.loads(res.text)
            bookmarkbody = res_bookmarks["bookmarks"]

            for bookmark in bookmarkbody:
                author_user = bookmark["user"]
                if check_target_user in author_user:
                    return True
            return False
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("hatena check exception!!")

    """ Upload flickr """

    def post_flickr(self, filepaths: list) -> list:
        try:
            apikey = self.flickrauth["api_key"]
            secret = self.flickrauth["secret"]
            flickr = flickrapi.FlickrAPI(apikey, secret)
            urls = []
            if len(filepaths) == 0:
                return urls
            for file_path in filepaths:
                filename = os.path.basename(file_path)
                with open(file_path, "rb") as uploadfile:
                    res = flickr.upload(
                        filename=filename, fileobj=uploadfile, is_public=1
                    )
                photo_id = res.findtext(".//photoid")
                if photo_id is not None:
                    photo_info = flickr.photos.getInfo(photo_id=photo_id)
                    farm_id = photo_info.find(".//photo").get("farm")
                    server_id = photo_info.find(".//photo").get("server")
                    original_secret = photo_info.find(".//photo").get("originalsecret")
                    photo_url = (
                        f"https://farm{farm_id}.staticflickr.com/"
                        f"{server_id}/{photo_id}_{original_secret}.png"
                    )
                    urls.append(photo_url)
                else:
                    self.applog.output_log("ERROR", ET.fromstring(res))
            return urls
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("Flickr post exception!!")

    """ Posted localtest blogger """

    def post_text_blogger(
        self, count: int = None, title: str = None, contents: str = None
    ):
        try:
            filepath = self.config.get_filepath("summarypost")
            if re.search(r"トレンドワード", title):
                filepath = self.config.get_filepath("trendwordpost")
            blogid = self.bloggerauth["post_blog_id"]
            # Building title
            posttime = "投稿時間:" + str(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            posttitle = posttime + " " + title
            # write file
            with open(filepath, mode="a") as f:
                f.write(f"blogid:{blogid}\n")
                f.write(posttitle)
                f.write("\n")
                f.write(contents)
                f.write("\n")
            return count
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("localtest brogger post exception!!")

    """ Posted Blogger """

    def post_blogger(
        self,
        count: int = None,
        title: str = None,
        contents: str = None,
        image_paths: list = None,
    ):
        try:
            # setting api information
            flow = OAuth2WebServerFlow(
                self.bloggerauth["client_id"],
                self.bloggerauth["client_secret"],
                self.bloggerauth["scope"],
                self.bloggerauth["redirect_uri"],
            )
            blogid = self.bloggerauth["post_blog_id"]
            credentialfile = OAuth2Storage(self.bloggerauth["credentials"])
            credentials = credentialfile.get()
            if credentials is None or credentials.invalid:
                credentials = tools.run_flow(flow, credentialfile)
            # Building title
            posttime = "投稿時間:" + str(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            posttitle = posttime + " " + title
            postdate = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            # Call blogger api
            http = credentials.authorize(http=httplib2.Http())
            service = build("blogger", "v3", http=http)
            posts = service.posts()
            # No image attached
            body = {
                "kind": "blogger#post",
                "id": blogid,
                "title": posttitle,
                "content": contents,
            }
            # Image Attachment
            if image_paths:
                # upload imagefile use flickr
                image_urls = self.post_flickr(image_paths)
                media_items = ""
                for image_url in image_urls:
                    media_items += f"<p><img src='{image_url}' /></p><br/>"
                body = {
                    "kind": "blogger#post",
                    "title": f"{postdate}分WordCloud",
                    "content": "本日分のWordCloud画像<br/>" + media_items,
                }
            # posting
            insert = posts.insert(blogId=blogid, body=body)
            posts_doc = insert.execute()

            if bool(posts_doc["status"] == "LIVE") is False:
                loglevel = "ERROR"
                errorinfo = (
                    posts_doc["status"]
                    + " "
                    + posts_doc.headers
                    + "\n"
                    + posttitle
                    + "\n"
                    + contents
                    + "\n"
                )
                self.applog.output_log(loglevel, errorinfo)
            result = count
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("blogger post exception!!")
