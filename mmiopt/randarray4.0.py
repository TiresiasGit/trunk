#coding: UTF-8
# How to use this software?
# ex. >python randarray4.0.py 10000x10000.npz 10000 int32
#
import time
import sys
import numpy as np
import csv
def main():
  argv = sys.argv
  print(argv)
  a = np.random.randint(1,100,(int(argv[2]),int(argv[2])),dtype=argv[3])
  #diagonal element must be 0.
  for i in range(int(argv[2])):
    a[i][i]=0
  np.savez_compressed(argv[1],array_=a)
  print(np.load(argv[1])['array_'])

if __name__  == "__main__":
    start = time.time() 
    main() #main処理
    t = time.time() - start
    print("total elapsed time="+str(t))

