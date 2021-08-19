import os
from datetime import datetime, timedelta

import requests
from scrapy import Selector
from PyPDF2 import PdfFileMerger, PdfFileReader


class Newpaper:

    def __init__(self, today, today_join):
        """
        参数用于测试, 半夜的时候还没有发布报纸
        :param today:
        :param today_join:
        """
        # 今天的日期格式 2021-08/18，用于拼接链接
        if today:
            self.today = today
            self.today_join = today_join
        else:
            self.today = datetime.now().strftime("%Y-%m/%d")
            self.today_join = datetime.now().strftime("%Y%m%d")
        self.base_url = f"http://paper.people.com.cn/rmrb/html/{self.today}/nbs.D110000renmrb_01.htm"

    def get_page_num(self):
        """
        获取当前报纸的所有页数
        :return:
        """
        print(f"开始获取当前报纸页面数, url=>{self.base_url}")
        response = requests.get(self.base_url)
        # print(response.text)
        selector = Selector(text=response.text)
        pages = selector.xpath("//div[@class='swiper-slide']/a/@href").re(".*renmrb_(.*).htm")
        print(f"当前报纸页面数获取完成, pages=>{pages}")
        return pages

    def get_page_pdf_name(self, page: str):
        """
        获取单页pdf文件名
        :param page:
        :return:
        """
        return f"{os.path.dirname(os.path.abspath(__file__))}/newpapers/{self.today_join}_{page}.pdf"

    def get_pdf_name(self):
        """
        获取整合的pdf文件名
        :return:
        """
        return f"{os.path.dirname(os.path.abspath(__file__))}/newpapers/{self.today_join}.pdf"

    def get_pdf_download_url(self, page):
        """
        获取每页pdf的下载链接
        :param page:
        :return:
        """
        # 下载链接 http://paper.people.com.cn/rmrb/images/2021-08/14/05/rmrb2021081405.pdf
        return f"http://paper.people.com.cn/rmrb/images/{self.today}/{page}/rmrb{self.today_join}{page}.pdf"

    def download_pages_pdf(self, pages: list):
        """
        下载所有页面PDF, 并保存为单页pdf
        :param pages:
        :return:
        """
        # 开始爬取
        for page in pages:
            download_url = self.get_pdf_download_url(page)
            print(f"开始下载, url=>{download_url}")
            response = requests.get(download_url)
            with open(self.get_page_pdf_name(page), 'wb') as f:
                f.write(response.content)
            print(f"下载完成, filename=>{self.get_page_pdf_name(page)}")

    def merge_pdf(self, pages):
        """
        合并pdf
        :param pages:
        :return:
        """
        print(f"开始合并当天报纸")
        # 获取当天的pdf列表
        pdf_list = [self.get_page_pdf_name(page) for page in pages]
        print(f"pdf_list=>{pdf_list}")
        file_merger = PdfFileMerger(strict=False)

        for pdf in pdf_list:
            file_merger.append(pdf)

        file_merger.write(self.get_pdf_name())
        file_merger.close()

        # 删除每页文件
        for pdf in pdf_list:
            os.remove(pdf)

        print("当前报纸合并完成")

    def crawl(self):
        """
        爬取主流程
        :return:
        """
        # 页数
        pages = self.get_page_num()
        if not pages:
            print("页面不存在, 停止爬取")
            return
        # 下载所有页数pdf
        self.download_pages_pdf(pages)
        # 合并pdf
        self.merge_pdf(pages)


if __name__ == '__main__':
    yesterday = datetime.now() + timedelta(days=-1)
    print(yesterday)
    paper = Newpaper(yesterday.strftime("%Y-%m/%d"), yesterday.strftime("%Y%m%d"))
    paper.crawl()
