import matplotlib.pyplot as plt
import numpy as np
def ToLeft(a,b,c):
	return a[0]*(b[1]-c[1])+a[1]*(c[0]-b[0])+b[0]*c[1]-c[0]*b[1]>0
	
#4 *	3 -		2 +
def Qdet(a,b,c):
	return a[0]*(b[1]-c[1])+a[1]*(c[0]-b[0])+b[0]*c[1]-c[0]*b[1]
	
def LogLeft(a,b,c):
	O=Qdet(a,b,c)
	if O==0:
		return 0
	elif O>0:
		return 1
	return -1
	
	
#输入：P[[x1,y1],[x2,y2],……]点集序列
#注意：该函数会对输出进行改变精简
#若不想改变P，则在传参时使用list(P)
#输出为L[顶点序列1,顶点序列2,……]
#输出点集序列，服从精简原则，即若[1,2,3]和[1,3]表示的是同一直线，则输出[1,3]
def Gift_Warpping(P):
	l=len(P)
	i_ymin=i=0
	ymin=P[0][1]
	while i<l:
		if P[i][1]<ymin:
			ymin=P[i][1]
			i_ymin=i
		
		i+=1
		
	i=i_ymin+1
	i_xmin=i_xmax=i_ymin
	xmin=xmax=P[i_ymin][0]
	while i<l:
		if P[i][1]==ymin:
			if P[i][0]>xmax:
				xmax=P[i][0]
				i_xmax=i
			elif P[i][0]<xmin:
				xmin=P[i][0]
				i_xmin=i
		i+=1
		
	if xmin==xmax:
		L=[i_ymin]
	else:
		L=[i_xmin,i_xmax]
	
	while 1:
		i=0
		while i<l:
			if L[-1]==i:
				i+=1
				continue
			j=i+1
			while j<l:
				if L[-1]==j:
					j+=1
					continue
				O=Qdet(P[L[-1]],P[i],P[j])
				if O<0:
					i=j
					break
				elif O==0:
					if abs(P[i][0]-P[L[-1]][0])+abs(P[i][1]-P[L[-1]][1])<abs(P[j][0]-P[L[-1]][0])+abs(P[j][1]-P[L[-1]][1]):
						i=j
						break
						
				j+=1
			if j==l:
				L.append(i)
				break
		if i==L[0]:
			break
					
	return L
	
