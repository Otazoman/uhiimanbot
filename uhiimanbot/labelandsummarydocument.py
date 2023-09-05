import time
import traceback

from libs.applicationlogs import ApplicationLogs
from libs.configreader import Configreader
from libs.datacrud import Datacrud
from libs.textprocessing import TextProcessing
from tqdm import tqdm


class LabelandSummaryDocument:
    def __init__(self, mode: str = "prod", destinationtype: str = "mongo"):
        self.mode = mode
        name = __name__
        logmode = "prod"
        self.loglevel = "CRITICAL"
        self.config = Configreader(mode)
        logpath = self.config.get_filepath("applog")
        self.applog = ApplicationLogs(name, logmode, logpath)
        self.datacrud = Datacrud(mode, destinationtype)
        self.textprocessing = TextProcessing(mode)

    """ Obtain stored RSS data """

    def get_article(self) -> list:
        try:
            condition = {}
            results = self.datacrud.read_data(condition)
            return results
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("get_article exception!!")

    """ Generate a label and summary text and  set the addlabel flag """

    def create_labels_and_summary(self, articles: object) -> bool:
        try:
            stopwords = self.textprocessing.get_japanese_stopwords()
            for article in tqdm(list(articles)):
                keyid = article["_id"]
                title = article["title"]
                description = article["description"]
                category = article["category"]
                labelword = ""
                summary = ""

                if "labelstat" in article:
                    article["category"] == "added"
                    continue

                # clean_description = self.textprocessing.clean_text(description)
                if title and description:
                    labelword = title + description
                elif title:
                    labelword = title
                elif description:
                    labelword = description

                label = self.textprocessing.get_label_candidate(
                    labelword, category, stopwords
                )
                update_condition = {"_id": keyid}
                labelupdate_value = {"$set": {"addlabel": label}}
                self.datacrud.update_data(update_condition, labelupdate_value)
                summarywords = self.textprocessing.get_summarize_text(description)
                if len(summarywords) > 0:
                    summary = " ".join(summarywords)
                elif len(label) > 0:
                    summary = ",".join(label)
                else:
                    summary = title
                summary_update_value = {
                    "$set": {"summary": summary, "labelstat": "added"}
                }
                self.datacrud.update_data(update_condition, summary_update_value)
            return True
        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("create_labels_and_summary exception!!")

    def main(self):
        try:
            starttime = time.perf_counter()

            articles = self.get_article()
            self.create_labels_and_summary(articles)

            articles_count = len(list(articles))
            endtime = time.perf_counter()
            processtime = endtime - starttime
            self.applog.output_log(
                "INFO", f"処理時間:{processtime}秒 処理件数:{articles_count}件"
            )

        except Exception:
            self.applog.output_log(self.loglevel, traceback.format_exc())
            raise Exception("LabelandSummaryDocument exception!!")
