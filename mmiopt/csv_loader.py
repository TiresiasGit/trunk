#coding: UTF-8
# How to use this software?
#  python csv_loader.py filename

import csv
import sys
import time

def main() :
  argv = sys.argv
  with open(argv[1],"r") as f:
    data = csv.reader(f)
    line=[row for row in data]
    print(line[0])

if __name__ == "__main__":
  try:
    start = time.time()
    main()
    t = time.time() - start
    print("elapsed time="+str(t))
  #error handring
  except IOError as error:
    print("ファイルが同じ改装にあるか確認してね")
