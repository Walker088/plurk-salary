#!/usr/bin/env python3
from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests, re, csv

url = "https://www.plurk.com/p/mtxvw5"

def writeCsv(fileName, path='./results/'):
    pass

def replyFormat(reply):
    regex = re.compile("^\d*([\u2E80-\u9FFF]|)/[\u2E80-\u9FFF]*/[\u2E80-\u9FFF]*")
    if re.search(regex, reply) != None:
        return True
    return False

def buildAgeTable(replyLst):
    pass

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
    pprint(replyLst)
    return replyLst

def main():
    replyLst = crawler()
    buildAgeTable(replyLst)

if __name__=="__main__":
    main()
#######################################################
