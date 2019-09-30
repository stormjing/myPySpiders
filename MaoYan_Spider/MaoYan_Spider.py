import requests
import re
import json
import time
from requests.exceptions import RequestException

def get_one_page(url):  
    """
    获取当前 url 的网页源码
    """
    try:
        headers = {     # 构造请求头
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
             (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:    # 返回异常
        return None

def parse_one_page(html):
    pattern = re.compile(       # 构造正则表达式对象
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.'
        +'*?releasetime.*?>(.*?)</p>.*?integer.*?(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S)
    items = re.findall(pattern, html)  # items 是列表，每一个元素都是字符串元组
    for item in items:
        yield {             # 返回一个生成器，每个元素是字典
            'index' : item[0],
            'image' : item[1],
            'title' : item[2],              # strip 移除字符串头尾空格换行
            'actor' : item[3].strip()[3:],  # "主演：" 后面的字符
            'time' : item[4].strip()[5:],   # "上映时间：" 后面的字符
            'score' : item[5] + item[6]
        }

def write_to_file(content):     # 传入的是一个字典，这里用到了 json 的加载文件
    with open('result.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
    f.close()

def main(offset):       # 每次爬取一个页面的 10 部电影的信息
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)        # 获得网页
    for item in parse_one_page(html):   # 解析网页并写入文件
        # print(item)
        write_to_file(item)

if __name__ == "__main__":
    for i in range(10):         # 设置偏移量，
        main(offset=i * 10)
        time.sleep(0.5)         # 每次等待 0.5 秒，防止反爬

