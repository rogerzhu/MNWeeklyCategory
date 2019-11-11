#! /usr/local/bin/python3
# coding:utf-8
# author:rogerzhu@126.com

import os
import click


@click.command()
@click.option('--src', type=click.STRING,
              help='Sorce folder that contains markdown files to be merged.')
@click.option('--dst', type=click.STRING,
              help='Destination folder that contains existing,\
                   categorized markdown files.')
def MergeFiles(src, dst):
    src_file_names = os.listdir(src)
    for name in src_file_names:
        dst_file_name = os.path.join(dst, name)
        src_file_name = os.path.join(src, name)
        if os.path.exists(dst_file_name):
            dst_file = open(dst_file_name, 'a+')
            src_file = open(src_file_name, 'r')

            for line in src_file:
                dst_file.write(line)

            dst_file.close()


if __name__ == '__main__':
    MergeFiles()
