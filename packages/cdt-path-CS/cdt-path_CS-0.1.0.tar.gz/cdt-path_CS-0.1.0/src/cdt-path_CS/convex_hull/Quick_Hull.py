import numpy as np
import matplotlib.pyplot as plt
from Utils import *

def Find_Extreme_Points(P):
	l=len(P)
	i=1
	xmax=xmin=P[0][0]
	while i<l:
		if P[i][0]>xmax:
			xmax=P[i][0]
		elif P[i][0]<xmin:
			xmin=P[i][0]
		i+=1
		
	i=0
	ymin_xmax=-np.inf
	ymax_xmin=np.inf
	while i<l:
		if xmax==P[i][0] and ymin_xmax<P[i][1]:
			ymin_xmax=P[i][1]
			i_xmax=i
			
		elif xmin==P[i][0] and ymax_xmin>P[i][1]:
			ymax_xmin=P[i][1]
			i_xmin=i
			
		i+=1
	
	return i_xmax,i_xmin
	
def Quick_Hull(P):
	i_xmax,i_xmin=Find_Extreme_Points(P)
	a=P[i_xmin]
	b=P[i_xmax]
	S1,S2=[],[]
	i=0
	while i<len(P):
		if i==i_xmax or i==i_xmin:
			i+=1
			continue
		if LogLeft(a,b,P[i])>=1:
			S1.append(P[i])
		elif LogLeft(a,b,P[i])==-1:
			S2.append(P[i])
		i+=1
	return [a]+Hull_Loop(a,b,S2)+[b]+Hull_Loop(b,a,S1)
	
def Hull_Loop(a,b,S):
	if len(S)<=1:
		return S
		
	d=0
	i=0
	while i<len(S):
		if Distance_S(a,b,S[i])>d:
			d=Distance_S(a,b,S[i])
			i_d=i
		i+=1
	i=0
	S1,S2=[],[]
	while i<len(S):
		if i==i_d:
			i+=1
			continue
		if LogLeft(a,S[i_d],S[i])==-1:
			S1.append(S[i])
		elif LogLeft(S[i_d],b,S[i])==-1:
			S2.append(S[i])
		i+=1
		
	return Hull_Loop(a,S[i_d],S1)+[S[i_d]]+Hull_Loop(S[i_d],b,S2)
	

if __name__ == "__main__":
	num=40
	X = np.random.rand(40) * 10  # 横坐标范围0到10  
	Y = np.random.rand(40) * 7   # 纵坐标范围0到7  
	
	# 将横坐标和纵坐标组合成点集  
	P = np.column_stack((X, Y))  
	# print(P)
	# 打印生成的点  
	plt.scatter(X,Y)
	i1,i2=Find_Extreme_Points(P)
	plt.scatter(P[i1][0],P[i1][1])
	plt.scatter(P[i2][0],P[i2][1])
	convex_hull=Quick_Hull(P)
	print(convex_hull)
	X_l=[]
	Y_l=[]
	for c in convex_hull:
		X_l.append(c[0])
		Y_l.append(c[1])
		
	X_l.append(X_l[0])
	Y_l.append(Y_l[0])
	plt.plot(X_l,Y_l)
	plt.show()