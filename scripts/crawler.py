#!/usr/bin/env python3
from pprint import pprint
from bs4 import BeautifulSoup as bs
import numpy as np
import requests, re, csv

url = "https://www.plurk.com/p/mtxvw5"

def writeCsv(header, Dict, fileName, path='../results/'):
    with open(path+fileName, 'a', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(header)
        for key in Dict.keys():
            array = np.asarray(Dict[key])
            Age = key
            High = np.amax(array)
            Low = np.amin(array)
            Medium = np.median(array)
            UQ = np.percentile(array, 75)
            LQ = np.percentile(array, 25)
            Counts = len(array)
            csvWriter.writerow([Age,High, Low, Medium, UQ, LQ, Counts])

def replyFormat(reply):
    regex = re.compile("^\d*([\u2E80-\u9FFF]|)/[\u2E80-\u9FFF]*/[\u2E80-\u9FFF]*")
    if re.search(regex, reply) != None:
        return True
    return False

def clean(Lst):
    return list(set(Lst))

def mapDctToEmptyLst(Lst):
    Dct = {}
    for item in Lst:
        Dct[item] = []
    return Dct

def convertSalary(string):
    regex = re.compile("^\d*([K]|)")
    match = re.search(regex, string)
    if match != None:
        try:
            salary = match.group(0)
            return int(string[:2])*1000
        except:
            #print(string)
            pass
    return False

def buildAgeTable(replyLst):
    ageLst = []
    srcLst = []
    header = ['Age', 'High', 'Low', 'Medium', 'UQ', 'LQ', 'Count']
    fileName = 'ageTable.csv'
    for item in replyLst:
        try:
            rawLst = item.split("/")
            age = int(rawLst[0][:2])
            ageLst.append(age)
            srcLst.append(rawLst)
        except ValueError as verr:
            print("ValueError", item)
    ageLst = clean(ageLst)
    ageDct = mapDctToEmptyLst(ageLst)
    for item in srcLst:
        age = int(item[0][:2])
        salary = convertSalary(item[-1])
        if salary != False:
            ageDct[age].append(salary)
    writeCsv(header, ageDct, fileName)
    pprint(ageDct)

def buildLocationTable(replyLst):
    pass

def buildSeniorityTable(replyLst):
    pass

def crawler():
    plurkHtml = requests.get(url)
    bsObj = bs(plurkHtml.text, "html.parser")
    replyLst = [reply.text for reply in \
                bsObj.find("section", {"id":"plurk_responses"}) \
                     .findAll("span", {"class":"plurk_content"}) \
                     if replyFormat(reply.text)==True]
    return replyLst

def main():
    replyLst = crawler()
    buildAgeTable(replyLst)

if __name__=="__main__":
    main()
#######################################################
