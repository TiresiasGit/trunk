#coding: UTF-8
# Maximum Mean Initialize and 2-opt. \
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
# > python mmiopt_shortest1.0.py filename
#                                ^^^^^^^^int or float valuses square matrix
#                                         of comma delimitered TSP Input file.
#
#                                        developer "Ryota Tanaka"
import numpy as np
import csv
import sys
import time

def main():
   argv = sys.argv
   if len(argv) != 2:
     print("File name may not be specified,or may contain extra options.")
     exit()
   print("start load file!")
   data = np.loadtxt(argv[1],delimiter=',',dtype='int32')
   print("end load file!")
   start = time.time()
   searched = [data.shape[1]]
   if data.shape[0] != data.shape[1]:
     print("Please check if it is a square matrix.")
   #array init
   flags = [0] * data.shape[0]
   anslist = np.array([],dtype='int32')
   ansedge = np.array([])
   accumulation = 0 #累積距離の初期化
   print("start max mean initalize.")
   index,dataeva = calc_maxevaindex(data)
   flags[index] = 1 #訪問済みにする
   anslist=np.append(anslist,int(index)) #答えとなるノード番号をキューに入れる
   num = data.shape[0] - 1
   while num > 0:
     beforeindex = index #ひとつ前のindexとして保持する
     indexes = [i for i, x in enumerate(data[index]) if 0 == flags[i]] #自分と訪問済みを除外したインデックスの集合を得る
     indexes = np.array(indexes)#ndarrayに変換
     xmin = min(data[index,indexes])
     #minindex = np.argmin(data[index,indexes])#意図的に探索終了してみる。->結果的に、複数最小値があった場合、エッジ長平均値によるノードの評価を省く方が、良解にたどり着くようだ。2-optでうまく補正できているのだろうか...？(未検証。原因不明。)
     minindexes = [i for i,x in enumerate(data[index,indexes]) if x == xmin] #最小値のインデックスの集合を得る
     if len(minindexes) > 1:
       index = np.argmin(dataeva[indexes[minindexes]])
       index = indexes[minindexes[index]] #最小値の行(移動先ノード)の中で評価値が最高のノード(スカラのノード番号)を取り出す
     else:
       index = indexes[minindexes[0]]
     #index = indexes[minindex]
     flags[index] = 1 #訪問済みにする
     anslist=np.append(anslist,int(index)) #答えとなるノード番号をキューに入れる
     accumulation += data[beforeindex,index] #累積距離に加算する
     num-=1
     #print(num)
   for i in range(len(anslist)-1):
     ansedge = np.append(ansedge,data[int(anslist[i]),int(anslist[i + 1])])
   print("end max mean initialize.")
   #2-opt法による解のworst除去
   print("start 2-opt")
   itr = 1
   while itr > 0 :
     num = data.shape[0] - 1
     tempedge0=np.zeros(4)#従来のエッジ長集合
     tempedge1=np.zeros(4)#swap後エッジ長集合
     templist=np.zeros(6)  
     while num > 0:
       worst_node_i = np.argmax(ansedge)#解の経路から、最長のエッジを出す
       #次のループのために、現在見つかった最大値の要素を削除
       ansedge = np.delete(ansedge,worst_node_i,axis=0)
       worst_minnode=np.argmin(data[int(anslist[worst_node_i])])
       #◆交換なし
       #交換元
       worst_minnode_i_list=np.where(anslist-worst_minnode==0)#array[]->intに変換は[0]を参照すればよい
       worst_minnode_i=worst_minnode_i_list[0]
       #print("worst_minnode_i");#print(worst_minnode_i)

       worst_node_i_next = worst_node_i+1

       templist[1]=anslist[worst_minnode_i]
       if worst_minnode_i-1 > 0 :
          templist[0]=anslist[worst_minnode_i-1]
          tempedge0[0]=data[int(templist[0]),int(templist[1])]
       if worst_minnode_i+1 < len(anslist)-1 :
          templist[2]=anslist[worst_minnode_i+1]
          tempedge0[1]=data[int(templist[1]),int(templist[2])]
       #交換先
       templist[4]=anslist[worst_node_i_next]
       if worst_node_i-1 > 0 :
          templist[3]=anslist[worst_node_i_next-1]
          tempedge0[2]=data[int(templist[3]),int(templist[4])]
       if worst_node_i+1 < len(anslist)-1 :
          templist[5]=anslist[worst_node_i_next+1]
          tempedge0[3]=data[int(templist[4]),int(templist[5])]

       #◆交換した場合
       #交換元
       templist[1]=anslist[worst_node_i_next]#swaped
       if worst_minnode_i-1 > 0 :
          templist[0]=anslist[worst_minnode_i-1]
          tempedge1[0]=data[int(templist[0]),int(templist[1])]
       if worst_minnode_i+1 < len(anslist)-1 :
          templist[2]=anslist[worst_minnode_i+1]
          tempedge1[1]=data[int(templist[1]),int(templist[2])]
       #交換先
       templist[4]=anslist[worst_minnode_i]#swaped
       if worst_node_i-1 > 0 :
          templist[3]=anslist[worst_node_i_next-1]
          tempedge1[2]=data[int(templist[3]),int(templist[4])]
       if worst_node_i+1 < len(anslist)-1 :
          templist[5]=anslist[worst_node_i_next+1]
          tempedge1[3]=data[int(templist[4]),int(templist[5])]
       #print("sum(tempedge0)");#print(np.sum(tempedge0))
       #print("sum(tempedge1)");#print(np.sum(tempedge1))
       #距離判定
       if(np.sum(tempedge1)<np.sum(tempedge0)):
         #node swap
         tempnode=             anslist[worst_node_i_next]
         anslist[worst_node_i_next]=anslist[worst_minnode_i]
         anslist[worst_minnode_i]=tempnode
       #decrement
       num-=1
     #while num end
     print("end 2-opt")
     print("search end anslist->",anslist)
     ansedge =[]
     for i in range(len(anslist)-1):
       ansedge = np.append(ansedge,data[int(anslist[i]),int(anslist[i + 1])])
     accumulation=np.sum(ansedge)
     print("Accumulation Distance = ",accumulation)
     print("ansedge = ",ansedge)
     itr-=1
     t = time.time() - start
     print("calculation elapsed time="+str(t))
   #while itr end   

def calc_maxevaindex(data):
   dataeva = np.mean(data,axis=1)
   evamax_i = dataeva.argmax()
   return evamax_i,dataeva

if __name__  == "__main__":
  try:
    start = time.time() 
    main() #main処理
    t = time.time() - start
    print("total elapsed time="+str(t))

  #errorハンドリング
  except IOError as error:
    print("ファイルが同じ階層にあるか確認してね")
