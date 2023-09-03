output_interval_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
    "data/interval_postcontent.txt"
)
output_summary_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
    "data/brogger_content.html"
)
output_trendword_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
    "data/trendword_content.html"
)
rss_template = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/templates/"
    "blogger_content.tpl"
)
trendwords_template = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/"
    "templates/blogger_trend.tpl"
)

template_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/templates/mail.tpl"
)

output_mail_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/data/mail.txt"
)

wordcloud_filepath = (
    "/home/matarain/pythonapp/uhiimanbot/tests/" "testmaterials/images/jp_wordcloud.png"
)

"""
投稿前の記事
"""
org_articles = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "11110000",
        "addlabel": ["pixel", "シリーズ", "ディスプレイ"],
        "summary": "pixel,シリーズ,ディスプレイ",
        "labelstat": "added",
        "poststatus": "DELETED",
        "dupkey": "None",
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
        "dupkey": "None",
    },
]

"""
投稿済記事
"""
before_check_contents = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
]

"""
Blogger投稿済記事
"""
before_blogger_contents = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
        "poststatus": "bloggerdone",
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
]


"""
トレンドワードチェック用
"""
checkwords_expected_result = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
        "poststatus": "bloggerdone",
        "trendwordstatus": "subject",
        "hitwords": ["Google"],
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
]

"""
トレンドワード付与済
"""
after_posted_contents = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
        "poststatus": "bloggerdone",
        "trendwordstatus": "subject",
        "hitwords": ["Google"],
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
]

"""
トレンドワード
"""
trendwords_data = [
    {
        "category": "Google Trend",
        "name": "Trend Words",
        "title": "Google",
        "volume": "200000",
        "link": "https://news.yahoo.co.jp/org_articles/2d35d6a68ff33e13273313a7401b038fe54d9097",
        "published": "2023-07-21 02:00:00",
    },
    {
        "category": "Google Trend",
        "name": "Trend Words",
        "title": "なでしこジャパン",
        "volume": "100000",
        "link": "https://www3.nhk.or.jp/news/html/20230722/k10014138561000.html",
        "published": "2023-07-22 09:00:00",
    },
    {
        "category": "Google Trend",
        "name": "Trend Words",
        "title": "台風情報",
        "volume": "50000",
        "link": "https://weathernews.jp/s/topics/202307/220075/",
        "published": "2023-07-20 12:00:00",
    },
]

"""
はてぶ投稿用テストデータ
"""
hatena_posted_content = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "11110000",
        "addlabel": ["pixel", "シリーズ", "ディスプレイ"],
        "summary": "pixel,シリーズ,ディスプレイ",
        "labelstat": "added",
    },
]


"""
WordCloud複数件用結果確認データ
"""
wordcloud_expected_result = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
        "poststatus": "bloggerdone",
        "trendwordstatus": "subject",
        "hitwords": ["Google"],
        "wordcloud": "completed",
    },
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢iOS 17｣や｢macOS Sonoma｣では｢Safari｣や｢メール｣のURLからトラッキングパラメータを自動的に削除可能に",
        "description": "MacRumorsによると  iOS   iPadOS   macOS Sonoma の Safari では Webサイト間のトラッキングを防ぐためにプライベートブラウジングモード中にURLからトラッキングパラメ   ",
        "link": "https://taisy0.com/2023/06/18/173129.html",
        "orgpublished": "Sun, 18 Jun 2023 01:38:21 +0000",
        "published": "2023-06-18 01:38:21",
        "updated": "2023-06-18 01:38:21",
        "_id": "20230618172417-92",
        "addlabel": ["iosipadosmacossonoma", "macos", "macrumors"],
        "summary": "iosipadosmacossonoma,macos,macrumors",
        "labelstat": "added",
        "poststatus": "POSTED",
    },
]

"""
WordCloud作成対象外のデータ
"""
nomatch_expected_result = [
    {
        "name": "気になる、記になる…",
        "category": "IT",
        "title": "｢Pixel 8｣と｢Pixel 8 Pro｣のディスプレイの仕様の詳細が明らかに",
        "description": "Googleは今秋に次期フラッグシップスマホ Pixel  シリーズを投入する予定ですが 本日 Android Authorityがその Pixel  シリーズのディスプレイの仕様に関する詳細を報じています 今回の   ",
        "link": "https://taisy0.com/2023/06/18/173142.html",
        "orgpublished": "Sun, 18 Jun 2023 02:17:48 +0000",
        "published": "2023-06-18 02:17:48",
        "updated": "2023-06-18 02:17:48",
        "_id": "20230618172417-1",
        "addlabel": ["pixel", "android", "authority"],
        "summary": "pixel,android,authority",
        "labelstat": "added",
    },
]
