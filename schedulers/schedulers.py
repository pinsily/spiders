from datetime import datetime, timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from newspaper import Newpaper


def rmrb_newpaper():
    """
    人民日报定时爬虫推送
    :return:
    """
    yesterday = datetime.now() + timedelta(days=-1)
    print(yesterday)
    paper = Newpaper(yesterday.strftime("%Y-%m/%d"), yesterday.strftime("%Y%m%d"))
    paper.crawl()


if __name__ == '__main__':

    rmrb_newpaper()
    # BlockingScheduler
    # scheduler = BlockingScheduler()
    # scheduler.add_job(rmrb_newpaper, 'cron', year="*", month="*", day="*", week="*",
    #                   day_of_week="*", hour="09", minute="15", second="0", misfire_grace_time=3600)
    # scheduler.start()