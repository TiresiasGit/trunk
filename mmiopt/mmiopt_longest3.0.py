#coding: UTF-8
# Maximum Mean Initialize and 2-opt. 
# -> MMI-OPT
#   this version is approximataly solve "shortest path" from TSP Input.
#
#   This argolithm developed for solve TSP approximately fast.
#   (TSP=Traveling Salesman Problem. )
#
# Confirmed operating environment.
#   CentOS Linux release 7.2.1511 (Core)
#   Python 2.7.5
#   numpy  1.16.5
#
# How to use this software from command line?
# > python mmiopt_shortest3.0.py filename npz
#                                         ^^^A solution is output as .npz
#                                ^^^^^^^^int or float valuses square matrix
#                                         of comma delimitered TSP Input file.
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

def main():
   argv = sys.argv
   if len(argv) != 3:
     print("File name may not be specified,or may contain extra options.")
     exit()
   print("start load file!")
   data = np.load(argv[1])['array_']
   print("end load file!")
   start = time.time()
   searched = [data.shape[1]]
   if data.shape[0] != data.shape[1]:
     print("Please check if it is a square matrix.")
   #array init
   flags = [0] * data.shape[0]
   ansnode = np.array([],dtype='int32')
   ansedge = np.array([])
   accumulation = 0 #累積距離の初期化
   print("start min mean initalize.")
   index,dataeva = calc_minevaindex(data)
   flags[index] = 1 #訪問済みにする
   ansnode=np.append(ansnode,int(index)) #答えとなるノード番号をキューに入れる
   num = data.shape[0] - 1
   while num > 0:
     beforeindex = index #ひとつ前のindexとして保持する
     indexes = [i for i, x in enumerate(data[index]) if 0 == flags[i]] #自分と訪問済みを除外したインデックスの集合を得る
     indexes = np.array(indexes)#ndarrayに変換
     xmax = max(data[index,indexes])
     #maxindex = np.argmax(data[index,indexes])
     maxindexes = [i for i,x in enumerate(data[index,indexes]) if x == xmax] #最小値のインデックスの集合を得る
     if len(maxindexes) > 1:
       index = np.argmax(dataeva[indexes[maxindexes]])#最大の評価を持つノードを選択する
       index = indexes[maxindexes[index]] #最小値の行(移動先ノード)の中で評価値が最低のノード(スカラのノード番号)を取り出す
     else:
       index = indexes[maxindexes[0]]
     #index = indexes[maxindex]
     flags[index] = 1 #訪問済みにする
     ansnode=np.append(ansnode,int(index)) #答えとなるノード番号をキューに入れる
     accumulation += data[beforeindex,index] #累積距離に加算する
     num-=1
     #print(num)
   for i in range(len(ansnode)-1):
     ansedge = np.append(ansedge,data[int(ansnode[i]),int(ansnode[i + 1])])
   print("end min mean initialize.")
   #2-opt法による解のworst除去
   print("start 2-opt")
   itr = 1
   while itr > 0 :
     num = data.shape[0] - 1
     tempedge0=np.zeros(4)#従来のエッジ長集合
     tempedge1=np.zeros(4)#swap後エッジ長集合
     templist=np.zeros(6)  
     while num > 0:
       worst_node_i = np.argmin(ansedge)#解の経路から、最短のエッジを出す
       #次のループのために、現在見つかった最大値の要素を削除
       ansedge = np.delete(ansedge,worst_node_i,axis=0)
       worst_maxnode=np.argmax(data[int(ansnode[worst_node_i])])#最長のエッジを探索
       #◆交換なし
       #交換元
       worst_maxnode_i_list=np.where(ansnode-worst_maxnode==0)#array[]->intに変換は[0]を参照すればよい
       worst_maxnode_i=worst_maxnode_i_list[0]
       #print("worst_maxnode_i");#print(worst_maxnode_i)

       worst_node_i_next = worst_node_i+1

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
     itr-=1
     t = time.time() - start
     print("calculation elapsed time="+str(t))
   #while itr end   

def calc_minevaindex(data):
   dataeva = np.mean(data,axis=1)
   evamin_i = dataeva.argmin()
   return evamin_i,dataeva

if __name__  == "__main__":
  try:
    start = time.time() 
    main() #main処理
    t = time.time() - start
    print("total elapsed time="+str(t))

  #errorハンドリング
  except IOError as error:
    print("Make sure the files are on the same leve")
