#! /usr/local/bin/python3
# coding:utf-8

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import click


base_url = 'https://weekly.manong.io/issues/'


def GetLatestNumber():
    latest = -1
    driver = webdriver.Chrome()
    try:
        driver.get(base_url)
        html = driver.page_source
        all_content = BeautifulSoup(html)
        latest_href = all_content.find_all('h4')[0].a['href']
        latest = int(latest_href[latest_href.rfind('/')+1:])
    except Exception:
        return -1

    driver.quit()
    return latest


def GetAllFromWeeklyManong(start, end, filename='allLists.txt'):
    if end == -1:
        end = GetLatestNumber() + 1

    driver = webdriver.Chrome()
    for i in range(start, end):
        full_url = base_url + str(i)
        try:
            driver.get(full_url)
            html = driver.page_source
            all_content = BeautifulSoup(html)
            all_h4 = all_content.find_all('h4')
            all_lists_with_urls = ''
            for item in all_h4:
                one_list_with_url = str(i) + ':' + item.a.get_text() + '$' + \
                                    str(item.a['href']) + '\r'
                all_lists_with_urls += one_list_with_url

            with open(filename, 'a+') as f:
                f.write(all_lists_with_urls)
            sleep(5)
        except Exception:
            pass

    driver.quit()


@click.group()
def GetMNWeeklyContent():
    pass


@GetMNWeeklyContent.command()
@click.option('--fname', type=click.STRING,
              help='The output file name for all content, \
                    default file name is allLists.txt.')
def new(fname):
    GetAllFromWeeklyManong(1, -1)


@GetMNWeeklyContent.command()
@click.option('--start', type=click.INT, default=1,
              help='The start series number, if not set, \
                    start from the 1st series.')
@click.option('--end', type=click.INT, default=-1,
              help='The end series number, if not set, \
                    end to the lastest series.')
@click.option('--fname', type=click.STRING,
              help='The output file name for all content, \
                    default file name is allLists.txt.')
def update(start, end, fname):
    if fname is None:
        GetAllFromWeeklyManong(start, end)
    else:
        GetAllFromWeeklyManong(start, end, fname)


@GetMNWeeklyContent.command()
@click.option('--fname', type=click.STRING,
              help='The output file name for all content, \
                    default file name is allLists.txt.')
def latest(fname):
    latest = GetLatestNumber()
    if fname is None:
        GetAllFromWeeklyManong(latest, latest + 1)
    else:
        GetAllFromWeeklyManong(latest, latest + 1, fname)


if __name__ == '__main__':
    GetMNWeeklyContent()
