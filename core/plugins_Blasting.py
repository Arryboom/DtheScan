#!/usr/bin/env python
#-*-coding=utf-8-*-
import Queue
import gevent
from gevent import monkey
monkey.patch_all()
import requests
import time
import re
from random import randint as rand

class Plugin_Blast():
    def __init__(self,url):
        self.url=url
        self.queue=Queue.Queue()
        self.run()


    def load_worker(self):
        with open('dict/plugins_name.txt','r') as f:
            plugin_name=f.readlines()
        for i in plugin_name:
            self.queue.put(i.strip())


    def _req(self,_plugin):
        ip = '{}.{}.{}.{}'.format(rand(100, 254), rand(100, 254), rand(100, 254), rand(100, 254))
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Referer': 'http://www.baidu.com',
            'X-Forwarded-For': ip,
            'Cookie': 'discuz=discuz'
        }
        url=self.url+'/plugin.php?id={}'.format(_plugin)
        try:
            return requests.get(url,headers=headers,timeout=10,allow_redirects=False).content
        except Exception as e:
            return False

    def scan(self):
        while not self.queue.empty():
            plugin_name=self.queue.get()
            print '\r[ Scaning... ] scan plugin to {}\t\t\t\t'.format(plugin_name),
            html=self._req(plugin_name)
            if not isinstance(html,bool):
                compile_result=re.search('source/plugin/(.*?)/',html)
                if compile_result:
                    print '\r[ {time} ] find plugin to {plugin}\t\t'.format(time=time.strftime('%X', time.localtime()),plugin=plugin_name)

    def run(self):
        self.load_worker()
        jobs = []
        for i in range(40):
            jobs.append(gevent.spawn(self.scan))
        gevent.joinall(jobs)