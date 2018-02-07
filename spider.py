# -*- coding: utf-8 -*-

import requests
from requests import RequestException

import re
import json
#from multiprocessing import Pool

def get_one_page(url):
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Upgrade-Insecure-Requests':'1',
            'Referer':'http://maoyan.com/board',
            'Host':'maoyan.com',
            'Cookie':'uuid=1A6E888B4A4B29B16FBA1299108DBE9C3508BBFD21993C18E7F45912C85F750F; _csrf=f67ee11937a53d0d54563fde1ab820463c78c0ccbc1512b29858e9c6b523cbff; isWebp=1; __mta=147249672.1517492391667.1517540578646.1517540637067.32; _lxsdk_s=c1472b2e83fef8950de592e0892a%7C%7C113'
    }
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None
    
    
'''    
def parse_one_page(html):
    #print(type(html))  json.loads(html)为啥不行
    soup = BeautifulSoup(html,"lxml")
    #print(type(soup))
    #title = soup.select('title')[0].get_text()
    #print(title)
    result = soup.select('dd') #<class 'list'>
    for items in result:
        print(items)
        print('--'*30)
'''

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer'
                         +'">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    #print(items) lists contains 10 tuple
    for item in items:
        yield{
                'index':item[0],
                'image':item[1],
                'title':item[2],
                'actor':item[3].strip()[3:],
                'time':item[4].strip()[5:],
                'score':item[5]+item[6]     
        }
        
    
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + '\n')
        f.close()
    
            
    
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    #print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)
    
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    #pool = Pool()
    #pool.map(main,[i*10 for i in range(10)])