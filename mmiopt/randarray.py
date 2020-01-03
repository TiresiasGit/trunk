import sys
import numpy as np
import csv
# How to use this software?
# ex. >python randarray.py 100000x100000.csv 100000
#
args = sys.argv
print(args)
with open(args[1],'w') as f:
   a = np.random.randint(1,100,(int(args[2]),int(args[2])))
   #diagonal element must be 0.
   for i in range(int(args[2])):
     a[i][i]=0
   for i in a:
     csv.writer(f).writerow(i)

