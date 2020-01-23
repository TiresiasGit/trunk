#coding: UTF-8
# How to use this software?
# ex. >python npz_reader.py ansnode.npz
#
import sys
import numpy as np
import csv


def main():
  argv = sys.argv
  print(np.load(argv[1])['array_'])

if __name__  == "__main__":
  try:
    main() #main処理

  #errorハンドリング
  except IOError as error:
    print("Make sure the files are on the same level")
