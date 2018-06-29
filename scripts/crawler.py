#!/usr/bin/env python3
from bs4 import BeautifulSoup as bs
import numpy as np
import logging, logging.config
import requests, re, csv

logging.config.fileConfig("logging.conf")
log = logging.getLogger("root")

url = "https://www.plurk.com/p/mtxvw5"

def writeCsv(header, Dict, fileName, path='../results/'):
    log.info("-------In WriteCsv-------")
    with open(path+fileName, 'a', newline='') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(header)
        for key in Dict.keys():
            array = np.asarray(Dict[key])
            Key = key
            High = np.amax(array)
            Low = np.amin(array)
            Medium = np.median(array)
            UQ = np.percentile(array, 75)
            LQ = np.percentile(array, 25)
            Counts = len(array)
            Mean = np.mean(array)
            Std = np.std(array)
            csvWriter.writerow([Key, High, Low, Medium, UQ, LQ, Counts, Mean, Std])
    log.info("***Finished Writing***")

def replyFormat(reply):
    log.debug("checking reply format...")
    regex = re.compile("^\d*([\u2E80-\u9FFF]|)/[\u2E80-\u9FFF]*/[\u2E80-\u9FFF]*")
    if re.search(regex, reply) != None:
        return True
    return False

def clean(Lst):
    log.debug("clean duplicate elements within list...")
    return list(set(Lst))

def cleanSingle(Dct):
    log.debug("delete key-value with only one value...")
    singleKey = [key for key in Dct.keys() if len(Dct[key]) < 3]
    for k in singleKey:
        del Dct[k]
    return Dct

def mapDctToEmptyLst(Lst):
    log.debug("mapDctToEmptyLst...")
    Dct = {}
    for item in Lst:
        Dct[item] = []
    return Dct

def makeDigit(string):
    log.debug("Digit Making...")
    Lst = [s for s in list(string) if s.isdigit()]
    return int(''.join(Lst))

def makeSeniority(rawSen):
    # e.g., rawSen: '年資8年', '年資三年'
    log.debug("Seniority Making...")
    regex = re.compile("^([\u2E80-\u9FFF])*\d[\u2E80-\u9FFF]")
    match = re.search(regex, rawSen)
    if match != None:
        Lst = [char for char in list(match.group(0))]
        return makeDigit(Lst)
    return None

def convertSalary(string):
    log.debug("-------In Salary Converting-------")
    regex = re.compile("\d*(K|k)")
    match = re.search(regex, string)
    if match != None:
        log.debug("regex cmp result: {}\n{}".format(match, match.group))
        try:
            salary = match.group(0)
            return makeDigit(salary)*1000
        except:
            log.error("convertSalary ERR, string: {}, salary: {}".format(string, match.group(0)))
            return None
    log.debug("Failed: {}".format(string))
    return None

def makeSrcLst(replyLst):
    log.info("-------In makeSrcLst-------")
    return [raw.split("/") for raw in replyLst]

def makeAgeLst(srcLst):
    log.info("-------In makeAgeLst-------")
    ageLst = [makeDigit(src[0]) for src in srcLst]
    return clean(ageLst)

def makeCityLst(srcLst):
    log.info("-------In makeCityLst-------")
    cityLst = [src[2][:2] for src in srcLst]
    return clean(cityLst)

def makeSenLst(srcLst):
    log.info("-------In makeSenLst-------")
    senLst = [makeSeniority(src[-2]) for src in srcLst if makeSeniority(src[-2]) != None]
    return clean(senLst)

def buildAgeTable(srcLst):
    log.info("--------In BuildAgeTable--------")
    # Note: srcLst would be each column of the reply content from the src website
    # the format would be: ['36歲', '私立高職畢業', '台北', '印前美工', '年資8年', '40K']
    header = ['Age', 'High', 'Low', 'Medium', 'UQ', 'LQ', 'Count', 'Mean', 'Std']
    fileName = "ageTable.csv"
    log.debug("Start to build ageLst and ageDct")
    ageLst = makeAgeLst(srcLst)
    ageDct = mapDctToEmptyLst(ageLst)
    for item in srcLst:
        age = makeDigit(item[0])
        salary = convertSalary(item[-1])
        if salary != None:
            ageDct[age].append(salary)
    log.debug("Finished ageDct building,\n{}".format(ageDct))
    log.info("start to write the results")
    writeCsv(header, cleanSingle(ageDct), fileName)

def buildCityTable(srcLst):
    # Note: srcLst would be each column of the reply content from the src website
    # the format would be: ['36歲', '私立高職畢業', '台北', '印前美工', '年資8年', '40K']
    log.info("-------In BuildCityTable-------")
    header = ['City', 'High', 'Low', 'Medium', 'UQ', 'LQ', 'Count', 'Mean', 'Std']
    fileName = "CityTable.csv"
    log.debug("Start to build cityLst and cityDct")
    cityLst = makeCityLst(srcLst)
    cityDct = mapDctToEmptyLst(cityLst)
    for item in srcLst:
        city = item[2][:2]
        salary = convertSalary(item[-1])
        if salary != None:
            cityDct[city].append(salary)
    log.debug("Finished cityDct building,\n{}".format(cityDct))
    log.info("start to write the results")
    log.debug("Finished cityDct single deleting,\n{}".format(cleanSingle(cityDct)))
    writeCsv(header, cleanSingle(cityDct), fileName)

def buildSeniorityTable(srcLst):
    # Note: srcLst would be each column of the reply content from the src website
    # the format would be: ['36歲', '私立高職畢業', '台北', '印前美工', '年資8年', '40K']
    log.info("--------In BuildSenioriyTable--------")
    header = ['Seniority', 'High', 'Low', 'Medium', 'UQ', 'LQ', 'Count', 'Mean', 'Std']
    fileName = "SeniorityTable.csv"
    log.debug("Start to build SenLst and SenDct")
    senLst = makeSenLst(srcLst)
    senDct = mapDctToEmptyLst(senLst)
    for item in srcLst:
        sen = makeSeniority(item[-2])
        salary = convertSalary(item[-1])
        if (sen != None and salary != None):
            senDct[sen].append(salary)
    log.debug("Finished senDct building,\n{}".format(senDct))
    log.info("start to write the results")
    writeCsv(header, cleanSingle(senDct), fileName)

def crawler():
    log.info("-------Starting Crawler------")
    plurkHtml = requests.get(url)
    bsObj = bs(plurkHtml.text, "html.parser")
    log.debug("start to build replyLst")
    replyLst = [reply.text for reply in \
                bsObj.find("section", {"id":"plurk_responses"}) \
                     .findAll("span", {"class":"plurk_content"}) \
                     if replyFormat(reply.text)==True]
    log.debug("finished replyLst building")
    return replyLst

def main():
    log.info("***System Start Runing***")
    replyLst = crawler()
    srcLst = makeSrcLst(replyLst)

    buildAgeTable(srcLst)
    buildCityTable(srcLst)
    buildSeniorityTable(srcLst)

if __name__=="__main__":
    main()
#######################################################
