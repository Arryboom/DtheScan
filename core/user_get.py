#!/usr/bin/env python
#-*-coding=utf-8-*-
import Queue
import gevent
from gevent import monkey
monkey.patch_all()
import re
import requests
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Get_User():
    def __init__(self,url):
        self.url=url
        self.queue=Queue.Queue()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': '*/*',
            'Referer': '{}'.format(self.url),
            'Cookie': 'whoami=21232f297a57a5a743894a0e4a801fc3'
        }
        self.user_lists=set()
        if self.url[-1:]=='/':
            self.url=self.url[:-1]
        self.run()

    def load_worker(self):
        with open('config/setting.ini','r') as f:
            scan_parameters=f.readlines()

        flag=False
        count=0
        for i in scan_parameters:
            if flag:break
            _parameter=eval(i.strip())
            for i in _parameter:
                if i.lower()=='user_count':
                    count=int(_parameter[i])
                    flag=True
                    break

        for i in range(1,count+1):
            i=str(i)
            if len(i)==1:
                i='00'+i
            if len(i)==2:
                i='0'+i

            uri='/home.php?mod=space&uid={}'.format(i)
            self.queue.put(self.url+uri)

    def _request(self,url):
        try:
            html=requests.get(url,headers=self.headers,timeout=110)
            if html.status_code==200:
                return html.text
        except Exception as e:
            return False

    def get_name(self,_html):
        r=u'<title>(.*?)的'
        try:
            _compile=re.search(r,_html)
            #print _html
            if _compile and '<div id="messagetext" class="alert_error">' not in _html:
                name= _compile.group(1)
                print '\r[ {time} ] get user to : {user}\t\t'.format(time=time.strftime('%X', time.localtime()),
                                                               user=name)
                self.user_lists.add(name)
        except UnicodeEncodeError as e:
            print e

    def scan(self):
        while not self.queue.empty():
            target=self.queue.get()
            req_result=self._request(target)
            if not isinstance(req_result,bool):
                self.get_name(req_result)

    def run(self):
        self.load_worker()
        jobs = []
        for i in range(10):
            jobs.append(gevent.spawn(self.scan))
        gevent.joinall(jobs)

def get_users(url):
    e = Get_User(url)
    return e.user_lists



