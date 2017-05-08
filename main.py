#/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from core.user_get import get_users
from core.uc_server_Blasting import Uc_Blasting
from core.User_Blasting import Blasting
from core.plugins_Blasting import Plugin_Blast
import sys

parse = argparse.ArgumentParser()
parse.add_argument('-u',"--url", dest="url", default='', help='The scan target')
parse.add_argument('-f',"--file", dest="file", default='', help='The scan targets')

def run(url):
    Plugin_Blast(url)
    exploit = get_users(url)
    userlists = exploit
    Blasting(url, userlists)
    Uc_Blasting(url)

def main(args):
    if args.url!='':
        target=args.url
        if target[:-1]=='/':
            target=target[-1:]
        if 'http' not in target:
            target = 'http://' + target
        run(target)

    if args.file!='':
        file=args.file
        for t in file:
            target = t.strip()
            if target[:-1] == '/':
                target = target[-1:]
            if 'http' not in target:
                target='http://'+target
            run(target)

if __name__=='__main__':
    if len(sys.argv) < 2:
        parse.print_help()
    else:
        main(parse.parse_args())

