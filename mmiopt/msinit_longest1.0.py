#coding: UTF-8
# minimum Mean Initialize and 2-opt.
# -> MMI-OPT
#   this version is approximataly solve "longest path" from TSP Input.
#
#   This argolithm developed for solve TSP approximately fast.
#   (TSP=Traveling Salesman Problem. )
#
# Confirmed operating environment.
#   CentOS Linux release 7.2.1511 (Core)
#   Python 2.7.5
#   Python 3.8.0
#   numpy  1.16.5
#
# How to use this software from command line?
# > python msinit_longest1.0.py filename.npz txt 0.01 single  no2-opt
#                                            ^^^A solution is output as .npz
#                               ^^^^^^^^^^^^int or float valuses square matrix
#                                           of np.savez_compressed(filename.npz,array_=matrix)
#                                  type
#  Input:filename                   int or float 
#  Output:ansedge.npz or txt        int
#         ansnode.npz or txt        int
#         accumulation.npz or txt   float
#                                        developer "Ryota Tanaka"
import numpy as np
import csv
import sys
import time
import itertools as itr
def main():
   argv = sys.argv
   if len(argv) != 6:
     print("File name may not be specified,or may contain extra options.")
     exit()
   print("start load file!")
   data = np.load(argv[1])['array_']
   data=np.array(data,dtype='int32')
   print(data)
   print("end load file!")
   start = time.time()
   searched = [data.shape[1]]
   if data.shape[0] != data.shape[1]:
     print("Please check if it is a square matrix.")
   #array init
   flags = np.zeros(data.shape[0],dtype='int32')
   print("flags =",flags)
   ansnode = np.array([],dtype='int32')
   ansedge = np.array([],dtype='int32')
   #ansedge = np.array([])
   accumulation = 0 #累積距離の初期化
   print("start min mean initalize.")
   er=float(argv[3])
   print("er="+str(er))
   dm1=data.shape[0]-1
   if er < 0.0 or 0.99 < er:
     print("inputed error rate is out of range.")
     exit()
   elif er <=0.0:
     n=dm1
   else:
     n=int((1.96*0.2857884/er)**2)
   print("n="+str(n))
   if n > dm1:
      n=dm1
   index,dataeva = calc_minevaindex(data,n,dm1)
   print("end min mean initialize.")
   flags[index] = 0 #訪問済みにする
   ansnode=np.append(ansnode,int(index)) #答えとなるノード番号をキューに入れる
   num = data.shape[0] - 1
   print("start search max edges.")
   while num > 0:
     beforeindex = index #ひとつ前のindexとして保持する
     data[index]=np.add(data[index],flags)
     if argv[4] == 'single':
       index = np.argmax(data[index])
     else:
       #multi
       xmax = np.max(data[index])
       maxindexes = [i for i,x in enumerate(data[index]) if x == xmax]
       if len(maxindexes) > 1:
         mindataevai = np.argmin(dataeva[maxindexes])
         index = maxindexes[mindataevai] #maxindexesの内、評価値が最大のノード番号を取り出す
       else:
         index = maxindexes[0]

     flags[index] = 0 #訪問済みにする
     ansnode=np.append(ansnode,int(index)) #答えとなるノード番号をキューに入れる
     accumulation += data[beforeindex,index] #累積距離に加算する
     num-=1
     #print(num)
   print("end search max edges.")
   print("start make ansedge from ansnode.")
   for i in range(len(ansnode)-1):
     ansedge=np.append(ansedge,data[int(ansnode[i]),int(ansnode[i + 1])])
   print("end make ansedge from ansnode.")
     #ansedge = np.append(ansedge,data[int(ansnode[i]),int(ansnode[i + 1])])
   #2-opt法による解のworst除去
   if argv[5] == '2-opt':
     print("start 2-opt")
     num = data.shape[0] - 1
     tempedge0=np.zeros(4)#従来のエッジ長集合
     tempedge1=np.zeros(4)#swap後エッジ長集合
     templist=np.zeros(6)  
     while num > 0:
       worst_node_i = np.argmin(ansedge)#解の経路から、最長のエッジを出す
       #次のループのために、現在見つかった最大値の要素を削除
       ansedge = np.delete(ansedge,worst_node_i,axis=0)
       worst_maxnode=np.argmax(data[int(ansnode[worst_node_i])])
       #◆交換なし
       #交換元
       worst_maxnode_i_list=np.where(ansnode-worst_maxnode==0)#array[]->intに変換は[0]を参照すればよい
       worst_maxnode_i=worst_maxnode_i_list[0]
       #print("worst_maxnode_i");#print(worst_maxnode_i)

       worst_node_i_next = worst_node_i+1
       #以下のif文は、worst_maxnode_iが解の先頭か、最後である場合、前がなかったり後がなかったりするので、その境界の処理
       templist[1]=ansnode[worst_maxnode_i]
       if worst_maxnode_i-1 > 0 :
          templist[0]=ansnode[worst_maxnode_i-1]
          tempedge0[0]=data[int(templist[0]),int(templist[1])]
       if worst_maxnode_i+1 < len(ansnode)-1 :
          templist[2]=ansnode[worst_maxnode_i+1]
          tempedge0[1]=data[int(templist[1]),int(templist[2])]
       #交換先
       templist[4]=ansnode[worst_node_i_next]
       if worst_node_i-1 > 0 :
          templist[3]=ansnode[worst_node_i_next-1]
          tempedge0[2]=data[int(templist[3]),int(templist[4])]
       if worst_node_i+1 < len(ansnode)-1 :
          templist[5]=ansnode[worst_node_i_next+1]
          tempedge0[3]=data[int(templist[4]),int(templist[5])]

       #◆交換した場合
       #交換元
       templist[1]=ansnode[worst_node_i_next]#swaped
       if worst_maxnode_i-1 > 0 :
          templist[0]=ansnode[worst_maxnode_i-1]
          tempedge1[0]=data[int(templist[0]),int(templist[1])]
       if worst_maxnode_i+1 < len(ansnode)-1 :
          templist[2]=ansnode[worst_maxnode_i+1]
          tempedge1[1]=data[int(templist[1]),int(templist[2])]
       #交換先
       templist[4]=ansnode[worst_maxnode_i]#swaped
       if worst_node_i-1 > 0 :
          templist[3]=ansnode[worst_node_i_next-1]
          tempedge1[2]=data[int(templist[3]),int(templist[4])]
       if worst_node_i+1 < len(ansnode)-1 :
          templist[5]=ansnode[worst_node_i_next+1]
          tempedge1[3]=data[int(templist[4]),int(templist[5])]
       #print("sum(tempedge0)");#print(np.sum(tempedge0))
       #print("sum(tempedge1)");#print(np.sum(tempedge1))
       #距離判定
       if(np.sum(tempedge1)>np.sum(tempedge0)):
         #node swap
         tempnode=             ansnode[worst_node_i_next]
         ansnode[worst_node_i_next]=ansnode[worst_maxnode_i]
         ansnode[worst_maxnode_i]=tempnode
       #decrement
       num-=1
     #while num end
     print("end 2-opt")

   print("search end ansnode->",ansnode)
   ansedge =[]
   for i in range(len(ansnode)-1):
     ansedge = np.append(ansedge,data[int(ansnode[i]),int(ansnode[i + 1])])
   accumulation=np.sum(ansedge)
   print("Accumulation Distance = ",accumulation)
   print("ansedge = ",ansedge)
   if argv[2] == 'txt':
     np.savetxt("ansnode.txt", ansnode,fmt ='%d')
     np.savetxt("ansedge.txt", ansedge,fmt ='%d')
     np.savetxt("accumulation.txt", [accumulation],fmt ='%f')
   elif argv[2] == 'npz':
     np.savez_compressed("ansnode.npz", array_=ansnode)
     np.savez_compressed("ansedge.npz", array_=ansedge)
     np.savez_compressed("accumulation.npz", array_=accumulation)
   else:
     print("!none output files!")
   t = time.time() - start
   print("calculation elapsed time="+str(t))


def calc_minevaindex(data,n,dm1):
   minj=dm1
   #before half(row number 0 to n-1 -> sum(0 to n)  (n+1 elements,include 0))
   dataeva=[np.sum(data[0:n,:n+1],axis=1)]
   datamax=[np.sum(data[0:n,:n+1],axis=1)]

   #after half(row number n to minj -> sum(0 to n-1 (n elements))
   dataeva=np.append(dataeva,np.sum(data[n:minj+1,:n],axis=1))
   datamax=np.append(datamax,np.min(data[n:minj+1,:n],axis=1))

   dataeva_results=1/(1+datamax)*dataeva
   evamin_i=np.argmin(dataeva_results)
   return evamin_i,dataeva

if __name__  == "__main__":
  try:
    start = time.time() 
    main() #main処理
    t = time.time() - start
    print("total elapsed time="+str(t))

  #errorハンドリング
  except IOError as error:
    print("Make sure the files are on the same level")
