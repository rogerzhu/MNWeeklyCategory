#! /usr/local/bin/python3
# coding:utf-8
# author:rogerzhu@126.com

import requests
from urllib import parse
import os
import click
from threading import Thread
import fake_useragent


def get_header():
    location = os.getcwd() + '/agent.json'
    ua = fake_useragent.UserAgent(path=location)
    return ua.random


def CountMDFileInAFolder(folder):
    file_names = os.listdir(folder)
    md_file_names = []
    for item in file_names:
        if '.md' in item:
            md_file_names.append(item)

    return md_file_names


@click.command()
@click.option('--folder', default='.',
              help='The folder that contains markdown files to be processed,\
                   default is current folder.')
def DeleteUnreachable(folder):
    if not os.path.exists('filtered'):
        os.mkdir('filtered')

    threads = []
    md_file_names = CountMDFileInAFolder(folder)

    for x in range(len(md_file_names)):
        thread = Thread(target=DeleteUnreachableCore,
                        args=(md_file_names[x], ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def DeleteUnreachableCore(file_name):
    r = open(file_name, 'r')

    for line in r:
        # modified because the url format changed from serires #283
        url = ''
        index_of_url = int(line.find('url='))
        index_of_aid = int(line.find('&aid'))
        if index_of_url < index_of_aid:
            url = line[line.find('url=')+4:line.find('&aid')]
        else:
            url = line[line.find('url=')+4:-2]

        if 'http' not in url:
            continue

        real_url = parse.unquote(parse.unquote(url))
        print(real_url)
        if 'toutiao.io' not in real_url:
            try:
                headers = {"User-Agent": get_header()}
                r = requests.get(real_url, timeout=15, headers=headers)
                print(r.status_code)
                if r.status_code == 200:
                    with open('./filtered/' + file_name, 'a+') as w:
                        w.write(line)
            except Exception:
                print('Not OK!')
                pass

        else:
            with open('./filtered/' + file_name, 'a+') as w:
                w.write(line)

    r.close()


if __name__ == '__main__':
    processed_files = DeleteUnreachable()
