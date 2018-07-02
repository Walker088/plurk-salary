# plurk-salary

## Usage

1. crawler.py  
This script will crawl the [plurk src website](https://www.plurk.com/p/mtxvw5) and output four .csv file into results/ folder.

```python
rm ./results/*.csv
cd ./scripts
./crawler.py
```

2. plot.py
This script will plot results charts into charts/ folder.
For now the script only support the boxplot for ***Age City Seniority*** to be the control variable.

```python
cd ./scripts
./plot.py -p boxplot -x Age
```