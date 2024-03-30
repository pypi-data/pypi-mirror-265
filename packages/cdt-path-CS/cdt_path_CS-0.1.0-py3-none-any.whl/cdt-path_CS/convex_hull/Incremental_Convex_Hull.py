import numpy as np
from .utils import *

def Incremental_Convex_Hull(P):
	l=len(P)
	if l==0:
		return []
		
	i1=1
	while i1<l:
		if np.array_equal(P[0],P[i1]):
			i1+=1
			continue
		break
	else:
		return [P[0]]
		
	i=i1+1
	while i<l:
		LogFlag=LogLeft(P[0],P[i1],P[i])
		if LogFlag==0:
			if abs(P[i][0]-P[0][0])+abs(P[i][1]-P[0][1])>abs(P[i1][0]-P[0][0])+abs(P[i1][1]-P[0][1]):
				i1=i
				
			i+=1
			continue
		elif LogFlag<0:
			L=[P[0],P[i],P[i1]]
			break
		else:
			L=[P[0],P[i1],P[i]]
			break
	else:
		return [P[0],P[i1]]
		
	i+=1
	while i<l:
		L=conv_2(L,P[i])
		i+=1
		
	return L
	
def conv(L,p):
	l=len(L)
	flag_f=flag_o=LogLeft(L[l-1],L[0],p)
	i=0
	i_r=i_l=-1
	while i<l-1:
		flag=LogLeft(L[i],L[i+1],p)
		if flag!=flag_o:
			if flag==0:
				ac=p-L[i]
				ab=L[i+1]-L[i]
				alpha=np.dot(ac, ab) / np.dot(ab, ab)
				if alpha>1:
					i_l=i
					if i_r!=-1:
						break
				elif alpha<0:
					if flag_o!=-1:
						print("This algorithm maybe wrong! conv")
					i_r=i
					if i_l!=-1:
						break
				else:
					return L
			elif flag==1:
				i_r=i
			else:
				i_l=i
			flag_o=flag
		i+=1
	else:
		if flag_f!=flag_o:
			if flag_f==1:
				i_r=i
			else:
				i_l=i
		
	if i_r==-1:
		return L
	if i_r<i_l:
		L=[p]+L[i_r:i_l+1]
	else:
		L=L[0:i_l+1]+[p]+L[i_r:]
	return L
	
def conv_2(L,p):
	l=len(L)
	flag_o=LogLeft(L[l-1],L[0],p)
	i=0
	i_r=i_l=-1
	L.append(L[0])
	while i<l:
		flag=LogLeft(L[i],L[i+1],p)
		if flag==0:
			ac=p-L[i]
			ab=L[i+1]-L[i]
			alpha=np.dot(ac, ab) / np.dot(ab, ab)
			if alpha>1:
				i_l=i
				if i_r!=-1:
					break
				flag_o=-1
			elif alpha<0:
				if flag_o!=-1:
					print("This algorithm maybe wrong! conv")
				i_r=i+1
				if i_l!=-1:
					break
				flag_o=1
			else:
				return L
		elif flag!=flag_o:
			if flag==1:
				i_r=i
				if i_l!=-1:
					break
			else:
				if flag_o==0:
					i_l=i-1
				else:
					i_l=i
				if i_r!=-1:
					break
			flag_o=flag
		i+=1
		
	del L[-1]
	
	if i_r==-1 and i_l==-1:
		return L
	if i_r<i_l:
		L=[p]+L[i_r:i_l+1]
	else:
		L=L[0:i_l+1]+[p]+L[i_r:]
	return L
	
	
def Incremental_Convex_Hull_Sort(P):
	return Incremental_Convex_Hull_Sorted_Simplified(Simplify_With_X_i(P[P[:,0].argsort()]))
	
def Incremental_Convex_Hull_Sorted_Simplified(P):
	l=len(P)
	if l<3:
		return P
		
	i1=1
	i=2
	while i<l:
		LogFlag=LogLeft(P[0],P[i1],P[i])
		if LogFlag==0:
			i1=i
			i+=1
			continue
		elif LogFlag<0:
			L=[P[0],P[i],P[i1]]
			i_xmax=1
			break
		else:
			L=[P[0],P[i1],P[i]]
			i_xmax=2
			break
	else:
		return [P[0],P[i1]]
		
	i+=1
	while i<l:
		L,i_xmax=Convex_Hull_Sorted_Increment(L,P[i],i_xmax)
		i+=1
		
	return L
	
	
def Convex_Hull_Sorted_Increment(A,p,a1=None):
	if a1==None:
		a1=max(enumerate(A), key=lambda x: x[1][0])[0]
	a2=a1
	la=len(A)
	if a1+1==la: a1=-1
	
	while LogLeft(p,A[a1],A[a1+1])!=1:
		a1+=1
		if a1+1==la: a1=-1
		
	while LogLeft(p,A[a2-1],A[a2])!=1:
		a2-=1
			
	if a1==0:
		return A[:a2+1]+[p],a2+1
	return A[:a2+1]+[p]+A[a1:],a2+1
	
def Convex_Hull_Sorted_Increment_New(A,p,a1=None):
	if a1==None:
		a1=max(enumerate(A), key=lambda x: x[1][0])[0]
	a2=a1
	la=len(A)
	if a1+1==la: a1=-1
	
	while LogLeft(p,A[a1],A[a1+1])!=1:
		a1+=1
		if a1+1==la: a1=-1
		
	while LogLeft(p,A[a2-1],A[a2])!=1:
		a2-=1
			
	if a1==0:
		return A[:a2+1]+[p],a2+1
	return A[:a2+1]+[p]+A[a1:],a2+1