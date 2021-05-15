#! /usr/bin/env python3
# coding:utf-8
from __future__ import with_statement,print_function
from urllib.request import urlopen,Request
import requests
from json import loads,dumps
from hashlib import sha3_224 as _sha3_224
from os.path import isdir
from pathlib import Path
from time import sleep
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
safety_header = {'User-Anget':
r'aria2/1.35.0'
}
sha3_224 = lambda x:_sha3_224(x.encode() if isinstance(x,str) else x).hexdigest()
URL = "https://api.lolicon.app/setu/?r18=%s&apikey=872375555e8585a40317f0&num=10"
def sb(uri):
    #uri = Request(uri,headers=safety_header)
    with requests.get(uri) as res:
        if res.status_code != 200:return False
        content = res.content
    with open('./URLs/img/'+uri.split('/')[-1],'wb') as f:f.write(content)
    return True
if __name__ == '__main__':
    print(u'您想要那种类型的图片？(0:不色1:色2:随机)')
    se = input()
    while se not in ('0','1','2'):
        print(u'请输入0,1或2')
        se = input()
    URL %= se
    req = Request(URL,headers={'Connection':'keep-alive','User-Anget':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'})
    buffer = 0
    with urlopen(req) as web:buffer = loads(web.read())
    if buffer['code'] != 0:
        print(u'出错了！原因：\n',buffer['msg'])
        print(u'敲击ENTER/RETURN键退出程序')
        input()
        exit()
    buffer = buffer['data']
    if not isdir('./URLs'):Path('./URLs').mkdir()
    if not isdir('./URLs/img'):Path('./URLs/img').mkdir()
    for x in buffer:
        print(x['url'])
        print(u'是' if x['r18'] else u'不是','r18内容',sep='')
    with open('./URLs/'+str(sha3_224(str(buffer)))+'.json','w',True,'utf-8') as f:f.write(dumps(buffer,indent=4))
    '''with ProcessPoolExecutor(max_workers=5) as pool:
        for i in buffer:
            pool.submit(sb,args=(i['url'],))'''
    with ThreadPoolExecutor(max_workers=5) as pool:
        for i in buffer:
            pool.submit(sb,i['url'])
    #for i in buffer:sb(i['url'])
    '''import webbrowser
    for i in buffer:
        webbrowser.open_new_tab(i['url'])
        sleep(0.5)
'''
    print(u'敲击ENTER/RETURN键退出程序')
    input()
