""" SNS 認証設定用データ """
sns_testtitles = ["\nblogger", "twitter", "flickr", "bluesky", "other"]
sns_names = ["blogger", "twitter", "flickr", "bluesky", "hatena"]
sns_auth_datas = [
    {
        "client_id": "dummy.com",
        "client_secret": "blogger_clientsecret",
        "scope": "https://www.googleapis.com/auth/blogger",
        "redirect_uri": "urn:aaaaa",
        "post_blog_id": "xxxxxx",
        "credentials": "/home/matarain/pythonapp/uhiimanbot/tests/"
        "testmaterials/config/credentials.dat",
    },
    {
        "parent_screen_name": "parent",
        "my_screen_name": "child",
        "consumer_key": "twitter1234567",
        "consumer_secret": "token123",
        "token": "token234",
        "token_secret": "secret998",
    },
    {"secret": "a123", "api_key": "apikeys"},
    {"user_name": "abc.bsky.social", "app_password": "aaaa-bb"},
    {
        "user_name": "hatebuser",
        "consumer_key": "hateb",
        "consumer_secret": "hatenasecret",
        "token": "token889",
        "token_secret": "secret884",
    },
]


""" Database 設定用データ """

database_testtitles = ["\ntext", "mongo", "sql", "exception"]
databasenames = ["text", "mongo", "database", 123]
databases = [
    {
        "filepath": "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
        "data/output.db",
        "filetype": "text",
    },
    {
        "host": "localhost",
        "username": "testtohonokai",
        "password": "password",
        "authSource": "test_cr_tohonokai",
        "authMechanism": "SCRAM-SHA-1",
        "dbname": "test_cr_tohonokai",
        "collection": "rss_article",
    },
    {
        "host": "localhost",
        "username": "username",
        "password": "password",
        "dbname": "databasename",
        "tablename": "tablename",
    },
]

""" file settings testdata """

file_testtitles = ["\nlog", "csv"]
pathstrings = ["applog", "csvfile"]
filepaths = [
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/logs/app.log",
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/config/rssfeed.csv",
]

""" rss feed data testdata """

feeds = [
    [
        "＠IT Smart & Socialフォーラム 最新記事一覧",
        "https://rss.itmedia.co.jp/rss/2.0/ait_smart.xml",
        "IT",
    ],
    ["気になる、記になる…", "https://taisy0.com/feed", "IT"],
    ["PCパーツまとめ", "http://blog.livedoor.jp/bluejay01-review/index.rdf", "IT"],
    [
        "＠IT Database Expertフォーラム 最新記事一覧",
        "https://rss.itmedia.co.jp/rss/2.0/ait_db.xml",
        "IT",
    ],
]

""" Message settings testdata """

message_testtitles = ["\nsmtp", "sendgrid", "slack"]
messagetypes = ["smtp", "sendgrid", "slack"]
messages = [
    {
        "server": "mail.google.com",
        "port": 465,
        "user": "sample",
        "password": "password",
        "from": "aaa@gmail.com",
    },
    {"apikey": "SG.api_key", "from": "aaa@aaa.com"},
    {"token": "xoxb-token", "channel": "Cannel"},
]
