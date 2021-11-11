import sys

import requests


def crawl(cid):
    proxies = {
        'https': '127.0.0.1:7890'
    }
    headers = {'authority': 'api.cbbee0.com',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 115Browser/25.0.0.7',
               'referer': "https://sgptv.vip/",
               'accept-language': 'zh-CN,zh;q=0.9'
               }
    payload = {'id': cid, 'userToken': '', 'hm': "008-api"}
    r = requests.post("https://api.cbbee0.com/v1_2/movieInfo", data=payload, headers=headers, proxies=proxies)
    detail = r.json()
    return detail


def download_video(url, title):
    headers = {'authority': 'api.cbbee0.com',
               'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 115Browser/25.0.0.7',
               'referer': "https://sgptv.vip/",
               'accept-language': 'zh-CN,zh;q=0.9'
               }
    proxies = {
        'https': '127.0.0.1:7890'
    }
    r = requests.get(url, headers=headers, proxies=proxies)
    detail = r.content
    with open("./video/" + title + ".mp4", 'wb') as f:
        f.write(detail)
        f.close()


def save_file(url, title):
    with open("./video/url.txt", 'a+') as f:
        f.write(title)
        f.write("\n")
        f.write(url)
        f.write("\n")
        f.close()


list = []
if __name__ == "__main__":
    try:
        start = sys.argv[1]
        for i in range(int(start), 1000):
            print("开始采集 page ", i)
            content = crawl(i)
            if content['code'] == 1:
                data = content['data']
                print("采集成功 视频地址", str(data['sort']) + "-" + data['title'], data['download_url'])
                list.append(data)
                save_file(data['download_url'], str(data['sort']) + "-" + data['title'])
                #download_video(data['download_url'], str(data['sort']) + "-"+ data['title'])
            else:
                print("请求失败", content['code'])

    except Exception as e:
        print(str(e))
