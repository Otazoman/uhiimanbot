import os
import pathlib
import sys

sys.path.append("..")

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + "/../..")
from unittest import TestCase

from libs.textprocessing import TextProcessing


class TestTextProcessing(TestCase):
    mode = "test"
    tp = TextProcessing(mode)

    """ ストップワード取得 """

    def test_get_stopwords(self):
        print("\nenglish stopwords-->>")
        result = self.tp.get_english_stopwords()
        self.assertIsInstance(result, list, "ourselves")
        print("japanese stopwords-->>")
        result = self.tp.get_japanese_stopwords()
        self.assertIsInstance(result, list, "わたし")

    """ テキスト正規化処理 """

    def test_clean_text(self):
        testdoc = """
        【こんにちわ、】（わたしは）［とても親しい友人が］@いません。
        https://google.co.jp　あいうえお 123456 \\!@#$%^&*+-+\"';:?<>という文字列です。cokiee
        """
        result = self.tp.clean_text(testdoc)
        text = "こんにちわわたしはとても親しい友人がいませんという文字列ですcokiee"
        self.assertEqual(result, text)

    """ 名詞リスト取得 """

    def test_get_noun_list(self):
        stopwords = self.tp.get_japanese_stopwords()
        testdoc = "こんにちわ、わたしはとても親しい友人がいませんという文字列です。広島県に住んでいます。"
        result = self.tp.get_nonus_list(testdoc, stopwords)
        texts = ["友人", "文字列", "広島県"]
        self.assertEqual(result, texts)

    """ 要約 """

    def test_get_summarize_text(self):
        print("japanese-->>")
        testdoc = """
        正規表現の起源は、言語学と、理論計算機科学の一分野であるオートマトン理論や形式言語理論にみることができる。
        20世紀の言語学では数理的に言語を扱う数理言語学が発展しその過程の一部として、また後者は計算のモデル化（オートマトン）や
        形式言語の分類方法などを扱う学術分野である。
        数学者のスティーヴン・クリーネは1950年代に正規集合と呼ばれる独自の数学的表記法を用い、これらの分野のモデルを記述した。
        Unix系のツールに広まったのは、ケン・トンプソンがテキストファイル中のパターンにマッチさせる手段として、この表記法を
        エディタQEDに導入したことなどに始まる。彼はこの機能をUNIXのエディタedにも追加し、後に一般的な検索ツールである
        grepの正規表現へと受け継がれていった。これ以降、トンプソンの正規表現の適用にならい、多くのUnix系のツールがこの方法を
        採用した（例えば expr, awk, Emacs, vi, lex, Perl など）。
        PerlとTclの正規表現はヘンリー・スペンサー(英)によって書かれたものから派生している
        （Perlは後にスペンサーの正規表現を拡張し、多くの機能を追加した）。
        フィリップ・ヘーゼルはPerlの正規表現とほぼ互換のものを実装する試みとしてPerl Compatible Regular Expressions (PCRE) を
        開発した。これはPHPやApacheなどといった新しいツールで使用されている。
        Rakuでは、正規表現の機能を改善してその適用範囲や能力を高め、Parsing Expression Grammarを定義できるようにする努力が
        なされた。この結果として、Raku文法の定義だけでなくプログラマのツールとしても使用できる、Perl 6 rulesと呼ばれる
        小言語が生み出された。
        （本来の）正規表現からの拡張は各種あり便利であるがその多くは、（本来の）正規言語から逸脱するものであり、
        キャプチャなどが代表例である。なお、正規言語から逸脱しないことによって理論的な扱いが可能になるという利点があるため、
        例えば「非包含オペレータ」の提案ではそういった観点からの理由も挙げられている。
        Rakuに限らずいくつかの実装では、（Perlではsubpatternと呼んでいる）部分パターンの定義とその再帰的な呼出しにより、
        例えばカッコの対応などといった（本来の）正規表現では不可能なパターンも表現できる。
        これは、対象部分にマッチした文字列が捕獲され、後から利用できるキャプチャとは異なり、パターンそのものの定義と利用である。
        PHP, Perl, Python（regexライブラリ）, Ruby などで利用できる。
        """
        result = self.tp.get_summarize_text(testdoc)
        texts = [
            "Unix系のツールに広まったのは、ケン・トンプソンがテキストファイル中のパターンにマッチさせる手段として、この表記法を エディタQEDに導入したことなどに始まる。",
            "PerlとTclの正規表現はヘンリー・スペンサー(英)によって書かれたものから派生している （Perlは後にスペンサーの正規表現を拡張し、多くの機能を追加した）。",
            "これは、対象部分にマッチした文字列が捕獲され、後から利用できるキャプチャとは異なり、パターンそのものの定義と利用である。",
        ]
        self.assertEqual(result, texts)
        print("english-->>")
        testdoc = """
        The United States of America (U.S.A. or USA), commonly known as the United States (U.S. or US) or America, 
        is a transcontinental country located primarily in North America. It consists of 50 states, a federal district, 
        five major unincorporated territories, nine minor outlying islands,[j] and 326 Indian reservations. It is either 
        the fourth- or third-largest country by land or total area, respectively.[d] The United States shares land borders 
        with Canada to its north and with Mexico to its south. It has maritime borders with the Bahamas, Cuba, Russia, and 
        other nations.[k] With a population of over 331 million,[e] it is the third most populous country in the world. 
        The national capital is Washington, D.C., and the most populous city and financial center is New York City.
        Paleo-aboriginals migrated from Siberia to the North American mainland at least 12,000 years ago, and advanced 
        cultures began to appear later on. These advanced cultures had almost completely declined by the time European 
        colonists arrived during the 16th century. The United States emerged from the Thirteen British Colonies established 
        along the East Coast when disputes with the British Crown over taxation and political representation led to the 
        American Revolution (1765–1784), which established the nation's independence. In the late 18th century, the U.S. 
        began expanding across North America, gradually obtaining new territories, sometimes through war, frequently 
        displacing Native Americans, and admitting new states. By 1848, the United States spanned the continent from 
        east to west. The controversy surrounding the practice of slavery culminated in the secession of the Confederate 
        States of America, which fought the remaining states of the Union during the American Civil War (1861–1865). With 
        the Union's victory and preservation, slavery was abolished by the Thirteenth Amendment.
        """
        result = self.tp.get_summarize_text(testdoc)
        texts = [
            "The United States of America (U.S.A. or USA), commonly known as the United States (U.S. or US) or America, is a transcontinental country located primarily in North America.",
            "[d] The United States shares land borders with Canada to its north and with Mexico to its south.",
            "By 1848, the United States spanned the continent from east to west.",
        ]
        self.assertEqual(result, texts)

    """ ラベル付 """

    def test_get_label_candidate(self):
        print("\njapanese-->>")
        lang = "jp"
        testdoc = """
        正規表現の起源は、言語学と、理論計算機科学の一分野であるオートマトン理論や形式言語理論にみることができる。
        20世紀の言語学では数理的に言語を扱う数理言語学が発展しその過程の一部として、また後者は計算のモデル化（オートマトン）や
        形式言語の分類方法などを扱う学術分野である。
        数学者のスティーヴン・クリーネは1950年代に正規集合と呼ばれる独自の数学的表記法を用い、これらの分野のモデルを記述した。
        Unix系のツールに広まったのは、ケン・トンプソンがテキストファイル中のパターンにマッチさせる手段として、この表記法を
        エディタQEDに導入したことなどに始まる。彼はこの機能をUNIXのエディタedにも追加し、後に一般的な検索ツールである
        grepの正規表現へと受け継がれていった。これ以降、トンプソンの正規表現の適用にならい、多くのUnix系のツールがこの方法を
        採用した（例えば expr, awk, Emacs, vi, lex, Perl など）。
        PerlとTclの正規表現はヘンリー・スペンサー(英)によって書かれたものから派生している
        （Perlは後にスペンサーの正規表現を拡張し、多くの機能を追加した）。
        """
        category = "サンプル"
        print("jpn exist text-->>")
        jsw = self.tp.get_japanese_stopwords()
        result = self.tp.get_label_candidate(testdoc, category, jsw)
        texts = ["正規表現", "exprawkemacsvilexperl", "grep"]
        self.assertEqual(result, texts)
        print("jpn non exist text-->>")
        testdoc = ""
        result = self.tp.get_label_candidate(testdoc, category)
        self.assertEqual(result, [category])

        print("english-->>")
        lang = "en"
        testdoc = """
        The United States of America (U.S.A. or USA), commonly known as the United States (U.S. or US) or America, 
        is a transcontinental country located primarily in North America. It consists of 50 states, a federal district, 
        five major unincorporated territories, nine minor outlying islands,[j] and 326 Indian reservations. It is either 
        the fourth- or third-largest country by land or total area, respectively.[d] The United States shares land borders 
        with Canada to its north and with Mexico to its south. It has maritime borders with the Bahamas, Cuba, Russia, and 
        other nations.[k] With a population of over 331 million,[e] it is the third most populous country in the world. 
        The national capital is Washington, D.C., and the most populous city and financial center is New York City.
        """
        category = "sample"
        print("en exist text-->>")
        result = self.tp.get_label_candidate(testdoc, category)
        texts = ["america", "bahamas", "canada"]
        self.assertEqual(result, texts)
        testdoc = ""
        print("en non exist text-->>")
        result = self.tp.get_label_candidate(testdoc, category)
        self.assertEqual(result, [category])

    """ 類似する単語が含まれるか確認 """

    def test_check_word_include(self):
        test_titles = [
            "\njpn exist text",
            "jpn non exist text",
            "en exist text",
            "en non exist text",
        ]
        search_terms = [
            "幸村",
            "伊藤忠雄",
            "Washington",
            "cat",
        ]
        target_texts = [
            "幸村は小学校に上がる前から祖父の開いている剣道場に通っている。幼馴染みの兼次と三成と清正も同門だ。",
            "抱きしめられている、その現状を孫一の脳味噌が理解するより慶次の方が早かった。",
            "Washington,[4] is a state in the Pacific Northwest region of the Washington United States. ",
            "Washington,[4] is a state in the Pacific Northwest region of the Western United States. ",
        ]
        expected_results = [["幸村"], [], ["washington"], []]
        jsw = self.tp.get_japanese_stopwords()
        for test_title, target_text, expected_result in zip(
            test_titles, target_texts, expected_results
        ):
            print(test_title + "-->>")
            results = self.tp.check_word_include(search_terms, target_text, jsw)
            self.assertEqual(results, expected_result)

    """ ワードクラウド """

    def test_generate_wordcloud(self):
        outputpath = "/home/matarain/pythonapp/uhiimanbot/tests/testmaterials/images/"
        print("\nMultilanguage-->>")
        target_texts = [
            "幸村は小学校に上がる前から祖父の開いている剣道場に通っている。幼馴染みの兼次と三成と清正も同門だ。",
            "抱きしめられている、その現状を孫一の脳味噌が理解するより慶次の方が早かった。",
            "Washington,[4] is a state in the Pacific Northwest region of the Washington United States. ",
            "Washington,[4] is a state in the Pacific Northwest region of the Western United States. ",
        ]
        jsw = self.tp.get_japanese_stopwords()
        esw = self.tp.get_english_stopwords()
        # 両方が含まれている場合
        files = ["jp_wordcloud.png", "en_wordcloud.png"]
        self.tp.generate_wordcloud(target_texts, outputpath, jsw, esw)
        for file in files:
            expected_filepath = outputpath + file
            self.assertTrue(
                os.path.exists(expected_filepath),
                f"File '{expected_filepath}' does not exist.",
            )
            os.remove(expected_filepath)
        # 日本語のみ
        print("japanese omly-->>")
        target_texts = [
            "幸村は小学校に上がる前から祖父の開いている剣道場に通っている。幼馴染みの兼次と三成と清正も同門だ。",
            "抱きしめられている、その現状を孫一の脳味噌が理解するより慶次の方が早かった。",
        ]
        self.tp.generate_wordcloud(target_texts, outputpath, jsw, esw)
        file = "jp_wordcloud.png"
        expected_filepath = outputpath + file
        self.assertTrue(
            os.path.exists(expected_filepath),
            f"File '{expected_filepath}' does not exist.",
        )
        os.remove(expected_filepath)
        # 英語のみ
        print("english omly-->>")
        target_texts = [
            "Washington,[4] is a state in the Pacific Northwest region of the Washington United States. ",
            "Washington,[4] is a state in the Pacific Northwest region of the Western United States. ",
        ]
        self.tp.generate_wordcloud(target_texts, outputpath, jsw, esw)
        file = "en_wordcloud.png"
        expected_filepath = outputpath + file
        self.assertTrue(
            os.path.exists(expected_filepath),
            f"File '{expected_filepath}' does not exist.",
        )
        os.remove(expected_filepath)
