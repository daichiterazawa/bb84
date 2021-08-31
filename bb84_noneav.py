# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 13:21:01 2021

@author: terad
"""
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
distance_start = 5
distance_end = 300
mesure_rate = 0.2 #測定率
filter_rate = 0.5 #測定フィルタ正解率

distance = distance_start
distance_list = []
IAB_list = []

while distance < distance_end:
    loss = 10**(-0.1 * 0.2 * distance)
    
    #Alice,Bob同時確率
    P_AB = np.zeros((2,3))
    P_AB[0,0] = 0.5 * loss * filter_rate * mesure_rate
    P_AB[0,1] = 0
    P_AB[0,2] = 0.5 - 0.5 * loss * filter_rate * mesure_rate
    P_AB[1,0] = 0
    P_AB[1,1] = 0.5 * loss * filter_rate * mesure_rate
    P_AB[1,2] = 0.5 - 0.5 * loss * filter_rate * mesure_rate
    y=P_AB.reshape((1,-1))
    #Bob同時確率
    P_B = np.zeros((3))
    P_B[0] = P_AB[0,0] + P_AB[1,0]
    P_B[1] = P_AB[0,1] + P_AB[1,1]
    P_B[2] = P_AB[0,2] + P_AB[1,2]
    
    #Aliceエントロピー
    H_A = -sum([x*np.log2(x) if x !=0 else 0 for x in [0.5,0.5]])
    
    #Bobエントロピー
    H_B = -sum([x*np.log2(x) if x !=0 else 0 for x in P_B.reshape((-1,1))])
    
    #Alic,Bob結合エントロピー
    H_AB = -sum([x*np.log2(x) if x !=0 else 0 for x in P_AB.reshape((-1,1))])
    
    #相互情報量を求める(以下の計算は微小な値を切り捨ててしまう可能性がある)
    I_AB = H_A + H_B - H_AB
    
    """
    #相互情報量を求める
    I_AB = 0
    for i in range(3):
        for j in range(2):
            if P_AB[j,i] != 0:
                I_AB += P_AB[j,i]*np.log2(P_AB[j,i]/0.5/P_B[i])
    
    """        
    distance_list.append(distance)
    IAB_list.append(I_AB)
    distance += 5
    
# グラフを書く
plt.plot(distance_list, IAB_list, marker="x")

# グラフのタイトル
plt.title("Quantum Key Distribution ")

# x軸のラベル
plt.xlabel("distance")

#yのスケール
ax = plt.gca()
ax.set_yscale('log')
# y軸のラベル
plt.ylabel("final key rate")

# グリッドを表示する
plt.grid(True)

# 表示する
plt.show()