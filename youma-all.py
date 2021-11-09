import re
import time
from time import sleep

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


class Test:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.file_name="youma-all.txt-wuma"
        content = self.get_content(url)

    def crawl_start(self):
        content = self.get_content(self.url)
        self.parse_detail(content)

    def get_content(self, url):
        self.driver.get(url)
        content = driver.page_source
        return content

    def parse_detail(self, content):
        html = etree.HTML(content)
        ul = html.xpath('//*[@id="videos"]//a')
        if len(url) > 0:

            open(self.file_name)
            for li in ul:
                item = {}
                href = li.xpath('./@href')[0]

                item['href'] = "https://javdb.com" + href
                driver.get(item['href'])
                html = etree.HTML(driver.page_source)
                details = html.xpath('//*[@id="magnets-content"]/table/tbody/tr[1]/td[1]/a/@href')
                title = html.xpath('/html/body/section/div/h2/strong/text()')
                if len(details) > 0 and len(title) > 0 :
                    details = details[0]
                    item['detail'] = details
                    title = title[0]
                    item['title'] = title
                    print(item['title'])
                    self.save_to_file(self.file_name, title, details)
                    #time.sleep(1)


    def save_to_file(self, file_name, title, content):
        with open(file_name, 'a+') as f:
            f.write(title + '\n')
            f.write(content)
            f.write('\n')
            f.close()


if __name__ == "__main__":
    first_url = "https://javdb.com/tags?c10=1"
    driver = webdriver.Chrome(options=options)
    page = 60
    try:
        driver.get(first_url)

        login = driver.find_element_by_xpath("/html/body/div[1]/div[2]/footer/a[1]").click()

        for i in range(1,page + 1 ):
            url = first_url+"&page="+str(i)
            print("crawl page "+url )
            test = Test(url, driver)
            test.crawl_start()
        driver.quit()

    except Exception as e:
        print(str(e))

