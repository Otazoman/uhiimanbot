import itertools
import re
import traceback
import urllib.request
from difflib import SequenceMatcher

import emoji
import matplotlib
import matplotlib.pyplot as plt
import MeCab
import neologdn
import nltk
from ja_stopword_filter import JaStopwordFilter
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer
from textblob import TextBlob
from wordcloud import WordCloud

from .applicationlogs import ApplicationLogs
from .configreader import Configreader


class TextProcessing:
    def __init__(self, mode: str):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        config = Configreader(mode)
        logpath = config.get_filepath("applog")
        self.fontpath = config.get_filepath("fontfilepath")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.checked_jpn = re.compile(
            "[\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEF]+"
        )

    """ Get stopwords """

    def get_english_stopwords(self) -> list:
        try:
            nltk.download("stopwords")
            result = stopwords.words("english")
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get english stopwords exception!!")

    def get_japanese_stopwords(self) -> list:
        try:
            url = "https://raw.githubusercontent.com/stopwords-iso/stopwords-ja/master/stopwords-ja.txt"
            response = urllib.request.urlopen(url)
            stopwords = response.read().decode("utf-8")
            result = stopwords.splitlines()
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get japanese stopwords exception!!")

    """ Cleanup sentence """

    def clean_text(self, text: str = None) -> str:
        try:
            str = neologdn.normalize(text)
            str = re.sub(r"(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?", "", str)
            str = re.sub("<.*?>", "", str)
            str = re.sub(r"(\d)([,.])(\d+)", r"\1\3", str)
            str = re.sub(r"[!-/:-@[-`{-【】「」~]", r" ", str)
            str = re.sub("[■-♯]", " ", str)
            str = re.sub(r"\d+", "0", str)
            str = re.sub(r"0", "", str)
            str = re.sub(r"\n", "", str)
            str = re.sub(r"\r", "", str)
            str = "".join(["" if c in emoji.UNICODE_EMOJI else c for c in str])
            if self.checked_jpn.search(text):
                str = re.sub(r" ", "", str)
            return str
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("clean text exception!!")

    """ Extract nouns with Mecab """

    def get_nonus_list(self, doc: str, stopwords: list) -> list:
        try:
            tagger = MeCab.Tagger(
                "-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
            )
            tagger.parse("")
            # Extract only nouns
            result = [
                line.split("\t")[0]
                for line in tagger.parse(doc).splitlines()
                if "名詞" in line.split()[-1]
                and len(line.split("\t")[0]) > 1
                and line.split("\t")[0] not in stopwords
            ]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("Mecab operation exception!!")

    """ Summarize the text """

    # def get_summarize_text(self, doc, lang: str = None):
    def get_summarize_text(self, doc: str) -> list:
        try:
            language = {"en": "english", "jp": "japanese"}
            tokenizer_lang = ""
            if self.checked_jpn.search(doc):
                tokenizer_lang = language["jp"]
            else:
                tokenizer_lang = language["en"]
            # @title Set number of summary sentences (Defalt = 3) { run: "auto" }
            # @param {type:"slider", min:3, max:30, step:1}
            # Sentences = 3  # @param {type:"slider", min:3, max:30, step:1}
            Sentences = int(len(doc) / 10 * 2)
            parser = PlaintextParser.from_string(doc, Tokenizer(tokenizer_lang))
            summarizer = LexRankSummarizer()
            # Spaces are also recognized as one word, so exclude them by making
            # them stop words
            summarizer.stop_words = [" "]
            # sentencres_count　setting
            summary = summarizer(document=parser.document, sentences_count=3)
            # Output summary statement
            result = [sentence.__str__() for sentence in summary]
            return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("summarize exception!!")

    """ Obtain the best label candidates """

    def get_label_candidate(
        self, words: str = None, category: str = None, sw: list = None
    ) -> list:
        try:
            DF_PARAM = 0.0
            nounlist = ""
            if len(words) == 0:
                result = [category]
                return result
            # Obtain a list of nouns to be parsed
            if self.checked_jpn.search(words):
                nounlist = self.get_nonus_list(self.clean_text(words), sw)
            else:
                wordtokenizer = TextBlob(self.clean_text(words))
                nounlist = [i for i in wordtokenizer.noun_phrases]

            # Analysis to produce label candidates
            if nounlist == []:
                result = [category]
                return result

            vectorizer = TfidfVectorizer(min_df=DF_PARAM)
            x = vectorizer.fit_transform(nounlist)
            words = vectorizer.get_feature_names_out()
            wordslist = []
            for vec in x.toarray():
                for w_id, tfidf in sorted(
                    enumerate(vec), key=lambda x: x[1], reverse=True
                ):
                    if (
                        words[w_id]
                        and len(words[w_id]) > 3
                        and words[w_id] not in category
                    ):
                        wordslist.append(words[w_id])
            # Merging duplicates and extracting the top 3 words
            tmpresult = list(dict.fromkeys(wordslist))
            if tmpresult:
                result = tmpresult[0:3]
                return result
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("label candidate exception!!")

    """ Generate a word and sentence summation to measure similarity """

    def check_word_include(self, words: list, doc: str, sw: list) -> list:
        try:
            results = set()
            SIMILARITY_VALUE = 0.75

            if not words or not doc:
                return []

            if self.checked_jpn.search(doc):
                nounlist = self.get_nonus_list(self.clean_text(doc), sw)
            else:
                wordtokenizer = TextBlob(self.clean_text(doc))
                nounlist = [i for i in wordtokenizer.noun_phrases]

            for word, noun in itertools.product(words, nounlist):
                similarity_rate = SequenceMatcher(None, word, noun).ratio()
                if similarity_rate >= SIMILARITY_VALUE:
                    results.add(noun)
            return list(results)
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("check word include exception!!")

    """ Generate a word and sentence summation to measure similarity """

    def generate_wordcloud(
        self, docs: list, outputpath: str, jp_stopwords: list, en_stopwords: list
    ):
        try:
            jp_wordcloud_source = []
            en_wordcloud_source = []
            for doc in docs:
                work_doc = self.clean_text(doc)
                if self.checked_jpn.search(work_doc):
                    noun = self.get_nonus_list(work_doc, jp_stopwords)
                    jp_wordcloud_source.extend(noun)
                else:
                    en_words = [
                        word
                        for doc in docs
                        for word in nltk.word_tokenize(doc.lower())
                        if word.isalpha()
                    ]
                    if en_stopwords is not None:
                        en_words = [
                            word for word in en_words if word not in en_stopwords
                        ]
                        en_wordcloud_source.extend(en_words)
            titles = []
            file_names = []
            wordcloud_sources = []
            if jp_wordcloud_source:
                wordcloud_sources.append(jp_wordcloud_source)
                titles.append("Japanese WordCloud")
                file_names.append("jp_wordcloud.png")
            if en_wordcloud_source:
                wordcloud_sources.append(en_wordcloud_source)
                titles.append("English WordCloud")
                file_names.append("en_wordcloud.png")
            if not wordcloud_sources:
                return False
            for title, file_name, wordcloud_source in zip(
                titles, file_names, wordcloud_sources
            ):
                wordcloud = WordCloud(
                    font_path=self.fontpath,
                    width=800,
                    height=800,
                    background_color="black",
                ).generate(" ".join(wordcloud_source))
                plt.figure(figsize=(8, 8))
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.title(title)
                plt.savefig(outputpath + file_name)
                plt.show()
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("generate wordcloud exception!!")
