import os
import re
import time
from time import sleep

import requests
from lxml import etree
from selenium import webdriver

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument(
    "User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
options.add_argument("Referer=https://javdb.com/tags/uncensored?c10=2")
options.add_argument(
    "Cookie=theme=auto; locale=zh; _ym_uid=1636389848888165840; _ym_d=1636389848; _ym_isad=2; over18=1; _jdb_session=cdUMfS7UlVElYK6BNlzXFuKFd4XEyOm9jeF9UUsiaKU1bi9a7ZgpcjaPkX8qc3%2Fowtnf8JH2oTD1mAc8pel91X6SLAhG%2B0IKYaxy7Na5WDQdNVJ1GGiiX4xL4SwQw18F1GMxsqFVhQQ3itwybgUrImo5v6buRbXcNUciZkeastKA1ldsmp4yIcOj7O2VUtD%2FzzAr7sJXdxCGA7a5HGp9nKr8p7yfkiqOQmwdU9hIEFGmhhLEmvDWDfmIdw3aWTWUsdTvkIdzgf1vOuyth2GVBoEfRmj4TSKWJaAxFXBgnIyEOt%2FHKcU%2BUOKO--kTMcJRWuG%2Bwbvh00--%2FHjliopiiXSYJU5vBpXs1A%3D%3D")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('blink-settings=imagesEnabled=false')
options.add_argument('--disable-gpu')
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument(
    'Cookie: ')

HOST = "https://javdb.com"
LIST = []
USER = []

class Test:
    def __init__(self, url, driver, file_name, is_zimu=False):
        self.url = url
        self.driver = driver
        self.file_name = file_name
        self.is_zimu = is_zimu

    def crawl_start(self):
        content = self.get_content(self.url)
        self.parse_detail(content)

    def get_content(self, url):
        self.driver.get(url)
        content = driver.page_source
        return content

    def get_list(self, list_url):
        self.driver.get(list_url)
        content = driver.page_source
        self.parse_list(content)

    def parse_list(self, content):
        html = etree.HTML(content)
        ul = html.xpath('//*[@id="actors"]/div//a')
        if len(ul) > 0:
            for li in ul:
                item = {}
                href = li.xpath('./@href')
                title = li.xpath('./strong/text()')
                style = li.xpath('.//span/@style')

                if len(href) > 0 and len(title) > 0 and len(style) > 0:
                    item['href'] = HOST + href[0]
                    item['title'] = title[0]
                    item['style'] = style[0]
                    LIST.append(item)

def save_img(path, file_name, url):
    # headers = {
    #     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    #     "referer": "https://javdb.com/"
    # }
    # s = requests.session()
    # s.keep_alive = False
    # response = s.get(url, headers=headers)
    # with open(path + "/" + file_name + ".jpg", "wb") as f:
    #     f.write(response.content)
    #     f.close()

    with open("./imgs/all" + "/无码女优.txt", "a+") as f:
        f.write(file_name+" "+ url+"\n")
        f.close()


def Find(string):
    # findall() 查找匹配正则表达式的字符串
    url = re.findall('https://jdbimgs.com/avatars.*\.jpg', string)
    if len(url) == 1:
        return url[0]
    else:
        return None


if __name__ == "__main__":
    try:

        mark_type = "all_wuma"  # zimu_youma  all_wuma  all_youma

        if mark_type == "zimu_wuma" or mark_type == "all_wuma":
            list_keyword = "/actors/uncensored"
        else:
            list_keyword = "/actors"

        list_first_url = HOST + list_keyword + "?page=1"
        driver = webdriver.Chrome(options=options)
        driver.get(list_first_url)
        login = driver.find_element_by_xpath("/html/body/div[1]/div[2]/footer/a[1]").click()

        for i in range(1, 31):
            list_url = HOST + list_keyword + "?page=" + str(i)
            test = Test(list_url, driver, "")
            test.get_list(list_url)

        for k in LIST:
            k['title'] = k['title'].strip()

            path = "./imgs/" + k['title']
            isExists = os.path.exists(path)
            if not isExists:
                os.makedirs(path)

            # 保存头像到目录
            avatar = Find(k['style'])

            item = {}
            if avatar is not None:
                item['name'] = k['title']
                item['avatar'] = avatar
                USER.append(item)
                save_img(path, k['title'], avatar)
                print(k['title'] + " " + avatar)
        print(USER)
        driver.quit()
        #     page = 60
        #     if mark_type == "zimu_wuma" or mark_type == "zimu_youma":
        #         first_url = k['href'] + "?t=c"
        #     else:
        #         first_url = k['href'] + "?t=d"
        #
        #     print("crawl ", first_url)
        #
        #     for i in range(1, page + 1):
        #         url = first_url + "&page=" + str(i)
        #         print("crawl page " + url)
        #         test = Test(url, driver, file_name, False)
        #         test.crawl_start()
        # driver.quit()

    except Exception as e:
        print(str(e))
        print(e.__traceback__.tb_frame.f_globals["__file__"])  # 发生异常所在的文件
        print(e.__traceback__.tb_lineno)
        driver.quit()