#! /usr/local/bin/python3
# coding:utf-8
import os
import json
import click

def LoadJsonFilters():
    settings = {}
    f = open('./category.json','r',encoding='utf-8') 
    settings = json.load(f)
     
    f.close()
    return settings

def DeleteAllHireInfoFromListsFile():
    count = 0
    lines = []
    with open('./allLists.txt','r') as r:
        lines=r.readlines()
    
    os.remove('./allLists.txt')
    
    with open('./allLists.txt','a+') as w:
        for line in lines:
            count = count + 1
            url = line[line.find('$')+1:-1]
            if not "job" in url:
                w.write(line)
    
    return count
 
def GetFiltersOnDemand(*args):
    filters = LoadJsonFilters()
    demand_filters = {'root':[]}
    if len(args) == 0:
        return filters
    
    for keyword in args:
        for item in filters['root']:
            if keyword.lower() == item['keywords'].lower():
                demand_filters['root'].append(item)
        
    return demand_filters

@click.command()
@click.option('--fname', default = 'allLists.txt', type = click.STRING, help = 'The raw file name for crawling file, default is allList.txt.')
@click.option('--filters', default = '', type = click.STRING, help ='Input the filers that you need, seperate by \',\',  if no keywords, means use all filters by default.')
def GenerateMDs(fname,filters):
    filter_list = []

    if filters is not None and filters is not '':
        filter_list = filters.split(',')

    original_file_line_number = DeleteAllHireInfoFromListsFile()   
    count = 0  

    filters = GetFiltersOnDemand(*filter_list) 

    f = open(fname,'r',encoding='utf-8') 
    for line in f: 
        count = count + 1
        url = line[line.find('$')+1:-1]
        ori_name = line[line.find(':')+1:line.find('$')]
        name = ori_name.lower()
        is_categorized = False 
        for item in filters['root']: 
            filter_words = item['filters']
            rejector_words = item['rejecters']
            if any(s in name for s in filter_words) and not any(s in name for s in rejector_words):
                with open(item['fileName'],'a+') as mdf:
                    mdf.write("1. [{0}]({1})\r\n".format(ori_name,url))
                is_categorized = True
        
        if not is_categorized:
            with open('./uncategorized1.md','a+') as mdf:
                mdf.write("1. [{0}]({1})\r\n".format(ori_name,url))

    f.close()
    return count

if __name__ == '__main__':
    md_line_number = GenerateMDs() 
