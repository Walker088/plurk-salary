#!/usr/bin/env python3
from argparse import ArgumentParser as ap
import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging, logging.config

logging.config.fileConfig("plotlog.conf")
log = logging.getLogger("root")

def initArgParser():
    parser = ap()
    parser.add_argument("-p", "--plot", help="Parameter for chart type generate, can be boxplot", dest="plot")
    parser.add_argument("-x", "--xaxis", help="Parameter for chart xAxis generate,\
                                                can be Age, City or Seniority", dest="xAxis")
    args = parser.parse_args()
    if not len(sys.argv) > 1:
        log.error("Plz try: plot.py -p [chartType] -x [xAxis]")
        sys.exit(0)
    return args

def makeChartData(rawData, xAxis):
    chartData = rawData[rawData.loc[:,"Salary"] < 100000]
    if xAxis == "Age":
        return chartData.loc[:,[xAxis,"Salary"]]
    elif xAxis == "City":
        citydf = chartData.groupby("City").sum()
        citydf = citydf[citydf.loc[:, "Age"] > 55]
        chartData = chartData[chartData.City.isin(citydf.index)]
        log.debug("\n{}".format(citydf.index))
        log.debug("\n{}".format(chartData))
        return chartData.loc[:,["City", "Salary"]]
    elif xAxis == "Seniority":
        chartData = chartData[chartData.loc[:, "Seniority"] > 0]
        chartData = chartData[chartData.loc[:, "Salary"] > 0]
        return chartData.loc[:,["Seniority", "Salary"]]
    else:
        log.error("Input parameter: {}\nInput parameter haven't been support yet, \
                  try Age, City or Seniority.".format(xAxis))
        return None

def plot(chartType, xAxis, rawData, fileName):
    if chartType == "boxplot":
        chartData = makeChartData(rawData, xAxis)
        print(chartData.head(10))
        boxplot(chartData, fileName)
    else:
        log.error("Do not support such chartType")

def boxplot(chartData, fileName, path="../charts/"):
    chart = sns.boxplot(x=chartData.columns[0], y=chartData.columns[1], data=chartData)
    fig = chart.get_figure()
    fig.savefig(path+fileName)
    plt.show()

def main():
    args = initArgParser()
    fileName = args.xAxis+args.plot+".png"
    rawData = pd.read_csv('../results/rawTable.csv')
    plot(args.plot, args.xAxis, rawData, fileName)

if __name__=="__main__":
    main()
##############################################3
