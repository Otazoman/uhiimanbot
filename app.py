import argparse
import time

from libs.applicationlogs import ApplicationLogs
from libs.configreader import Configreader
from uhiimanbot.afteroperationprocessing import AfterOperationProcessing
from uhiimanbot.articleposting import ArticlePosting
from uhiimanbot.labelandsummarydocument import LabelandSummaryDocument
from uhiimanbot.targetinformationacquisition import TargetInformationAcquisition


def parse_args():
    parser = argparse.ArgumentParser(description="uhiiman_bot モジュールの実行")
    parser.add_argument(
        "module",
        nargs="?",
        choices=["all", "targetinfo", "labelsummary", "articlepost", "afterprocess"],
        default="all",
        help="実行するモジュールを選択: all, targetinfo, labelsummary, articlepost, afterprocess",
    )
    parser.add_argument(
        "--mode", default="prod", help="モード: test または prod (デフォルト: prod)"
    )
    parser.add_argument(
        "--destinationtype",
        default="mongo",
        help="データベース指定: mongo または text mysql postgre (デフォルト: mongo)",
    )
    parser.add_argument(
        "--wordcloudtime",
        default=23,
        help="WordCloud指定用: 0-24までの数字 (デフォルト: 23)",
    )
    return parser.parse_args()


def run_all_modules(mode, destinationtype):
    targetinformationacquisition = TargetInformationAcquisition(mode, destinationtype)
    labelandsummarydocument = LabelandSummaryDocument(mode, destinationtype)
    articleposting = ArticlePosting(mode, destinationtype)
    afteroperationprocessing = AfterOperationProcessing(mode, destinationtype)

    print("start targetinformationacquisition")
    targetinformationacquisition.main()
    print("start labelandsummarydocument")
    labelandsummarydocument.main()
    print("start articleposting")
    articleposting.main(wc_post_time=int(args.wordcloudtime))
    print("start afteroperationprocessing")
    afteroperationprocessing.main()


def run_module(module, mode, destinationtype):
    if module == "targetinfo":
        targetinformationacquisition = TargetInformationAcquisition(
            mode, destinationtype
        )
        targetinformationacquisition.main()
    elif module == "labelsummary":
        labelandsummarydocument = LabelandSummaryDocument(mode, destinationtype)
        labelandsummarydocument.main()
    elif module == "articlepost":
        articleposting = ArticlePosting(mode, destinationtype)
        articleposting.main(wc_post_time=int(args.wordcloudtime))
    elif module == "afterprocess":
        afteroperationprocessing = AfterOperationProcessing(mode, destinationtype)
        afteroperationprocessing.main()


if __name__ == "__main__":
    args = parse_args()
    module = args.module
    mode = args.mode
    destinationtype = args.destinationtype

    name = __name__
    config = Configreader(mode)
    logpath = config.get_filepath("applog")
    applog = ApplicationLogs(name, mode, logpath)

    applog.output_log("INFO", "uhiiman_bot 全体処理開始")
    starttime = time.perf_counter()
    print("---- start uhiimanbot ----")

    if module == "all":
        run_all_modules(mode, destinationtype)
    else:
        run_module(module, mode, destinationtype)

    endtime = time.perf_counter()
    processtime = endtime - starttime

    applog.output_log("INFO", f"処理時間: {processtime}秒 uhiiman_bot 全体処理完了")
    print("---- end uhiimanbot ----")
