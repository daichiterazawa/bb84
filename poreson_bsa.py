"""
Eveの盗聴はBSAを想定
ぽあそんぶんぷにしたがう

"""
import numpy as np
import matplotlib.pyplot as plt

def poreson(ave):
    p = 1 - np.exp(-ave)
    return p

distance_start = 0
distance_end = 200
mesure_rate = 0.2 #測定率
Bob_filter = 0.5 #測定フィルタ正解率
Eve_filter = 0.5
photon_rate = 0.1

distance = distance_start
distance_list = []
R_list = []

while distance < distance_end:
    loss = 10**(-0.1 * 0.2 * distance) #透過率
    photon_B = poreson(photon_rate * loss) #Bobが光子を受信する確率
    photon_E = poreson(photon_rate * (1-loss)) #Eveが光子を受信する確率
    
    ##### Alice,Bobの関係 #####
    #Alice,Bob同時確率
    P_AB = np.zeros((2,3))
    P_AB[0,0] = 0.5 * photon_B * Bob_filter * mesure_rate
    P_AB[0,1] = 0
    P_AB[0,2] = 0.5 - P_AB[0,0]
    P_AB[1,0] = 0
    P_AB[1,1] = 0.5 * photon_B * Bob_filter * mesure_rate 
    P_AB[1,2] = 0.5 - P_AB[1,1]
    
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
    
    #相互情報量を求める(?以下の計算だと微小な値を切り捨ててしまう可能性がある?)
    I_AB = H_A + H_B - H_AB
    
    ##### Bob,Eveの関係 #####
    #Bob,Eve同時確率
    P_BE = np.zeros((3,3))
    P_BE[0,0] = P_B[0] * photon_E * Eve_filter
    P_BE[0,1] = 0
    P_BE[0,2] = P_B[0] - P_BE[0,0]
    P_BE[1,0] = 0
    P_BE[1,1] = P_B[1] * photon_E * Eve_filter
    P_BE[1,2] = P_B[1] - P_BE[1,1]
    P_BE[2,0] = 0
    P_BE[2,1] = 0
    P_BE[2,2] = P_B[2]
    
    #Eveの確率
    P_E = np.zeros((3))
    P_E[0] = sum(P_BE[:,0])
    P_E[1] = sum(P_BE[:,1])
    P_E[2] = sum(P_BE[:,2])
    
    #Eveのエントロピー
    H_E = -sum([x*np.log2(x) if x !=0 else 0 for x in P_E.reshape((-1,1))])
    
    #Eve,Bobのエントロピー
    H_BE = -sum([x*np.log2(x) if x !=0 else 0 for x in P_BE.reshape((-1,1))])
    
    #Bob,Eveの相互情報量
    I_BE = H_B + H_E - H_BE
    ######
    
    
    distance_list.append(distance)
    R_list.append(I_AB)
    distance += 1
    
# グラフを書く
plt.plot(distance_list, R_list, marker="x")

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