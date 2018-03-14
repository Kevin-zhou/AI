# http://code.py40.com/42.html

import re
import os
import requests
import time

global PhotoNum
PhotoNum = 0
PWD = "E:/Python/ai2018-3-12/huaban/"
head = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
TimeOut = 30

url = "http://huaban.com/favorite/beauty/"
url_image = "http://hbimg.b0.upaiyun.com/"
urlNext = "http://huaban.com/favorite/beauty/?iqkxaeyv&limit=20&wfl=1&max="


def downfile(file, url):
    print("开始下载：", file, url)
    try:
        r = requests.get(url, stream=True)
        with open(file, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
    except Exception as e:
        print("下载失败了", e)


def requestpageText(url):
    try:
        Page = requests.session().get(url, headers=head, timeout=TimeOut)
        Page.encoding = "utf-8"
        return Page.text
    except Exception as e:
        print("联网失败了...重试中", e)
        time.sleep(5)
        print("暂停结束")
        requestpageText(url)


def requestUrl(url):
    global PhotoNum
    print("*******************************************************************")
    print("请求网址：", url)
    text = requestpageText(url)
    pattern = re.compile('{"pin_id":(\d*?),.*?"key":"(.*?)",.*?"like_count":(\d*?),.*?"repin_count":(\d*?),.*?}', re.S)
    items = re.findall(pattern, text)
    print(items)
    max_pin_id = 0
    for item in items:
        max_pin_id = item[0]
        x_key = item[1]
        x_like_count = int(item[2])
        x_repin_count = int(item[3])
        if (x_repin_count > 10 and x_like_count > 10) or x_repin_count > 100 or x_like_count > 20:
            print("开始下载第{0}张图片".format(PhotoNum))
            url_item = url_image + x_key
            filename = PWD + str(max_pin_id) + ".jpg"
            if os.path.isfile(filename):
                print("文件存在：", filename)
                continue

            downfile(filename, url_item)
            PhotoNum += 1
    requestUrl(urlNext + max_pin_id)


if not os.path.exists(PWD):
    os.makedirs(PWD)
requestUrl(url)