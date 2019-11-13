#! /usr/local/bin/python3
# coding:utf-8
# author:rogerzhu@126.com

import os
import click
from threading import Thread


def CountMDFileInAFolder(folder):
    file_names = os.listdir(folder)
    md_file_names = []
    for item in file_names:
        if '.md' in item:
            md_file_names.append(item)

    return md_file_names


@click.command()
@click.option('--folder', default='.',
              help='the folder name to omit duplications of markdowns.')
def OmitDup(folder):
    if not os.path.exists('nodup'):
        os.mkdir('nodup')

    threads = []
    md_file_names = CountMDFileInAFolder(folder)

    for x in range(len(md_file_names)):
        thread = Thread(target=OmitDupCore,
                        args=(folder, md_file_names[x], ))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return


def OmitDupCore(folder, file_name):
    no_dup_titles = []
    no_dup_lines_content = []
    with open(folder + '/' + file_name, 'r') as r:
        for line in r:
            title = line[line.find('[')+1:line.rfind(']')]
            if title not in no_dup_titles:
                no_dup_titles.append(title)
                no_dup_lines_content.append(line)

    w = open('./NoDup/' + file_name, 'a+')
    for line in no_dup_lines_content:
        w.write(line)
    w.close()


if __name__ == '__main__':
    OmitDup()
