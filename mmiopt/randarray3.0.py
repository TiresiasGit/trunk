#coding: UTF-8
# How to use this software?
# ex. >python randarray.py 100000x100000.csv 100000
#
import sys
import numpy as np
import csv
def main():
  argv = sys.argv
  print(argv)
  a = np.random.randint(1,100,(int(argv[2]),int(argv[2])))
  #diagonal element must be 0.
  for i in range(int(argv[2])):
    a[i][i]=0
  np.savez_compressed(argv[1],array_=a)
  print(np.load(argv[1])['array_'])

if __name__  == "__main__":
  try:
    main() #mainˆ—

  #errorƒnƒ“ƒhƒŠƒ“ƒO
  except IOError as error:
    print("Make sure the files are on the same level")