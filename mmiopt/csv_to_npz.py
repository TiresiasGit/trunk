#coding: UTF-8
# How to use this software?
#  python csv_loader.py InFile.csv OutFile.npz

import csv
import sys
import time
import numpy as np

def main() :
  argv = sys.argv
  with open(argv[1],"r") as f:
    a = csv.reader(f,delimiter=',', quotechar='"')
    data=[row for row in a]
    print(data)
    np.savez_compressed(argv[2],array_=data)
    #print(np.load(argv[2])['array_'])

if __name__ == "__main__":
  try:
    start = time.time()
    main()
    t = time.time() - start
    print("elapsed time="+str(t))
  #error handring
  except IOError as error:
    print("ファイルが同じ改装にあるか確認してね")
