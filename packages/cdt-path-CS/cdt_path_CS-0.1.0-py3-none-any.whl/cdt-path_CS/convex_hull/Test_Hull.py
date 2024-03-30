import numpy as np
import matplotlib.pyplot as plt
from Incremental_Convex_Hull import *
from Divide_And_Conquer_Convex_Hull import Divide_And_Conquer_Convex_Hull,Combin_Convex_Hull_M_2
from .utils import *
from Display import Display_Convex_Hull
num=40

# np.random.seed(42)
X = np.random.rand(num) * 10  # 横坐标范围0到10  
Y = np.random.rand(num) * 7   # 纵坐标范围0到7  

P = np.column_stack((X, Y))  
plt.scatter(X,Y)

# convex_hull=Incremental_Convex_Hull(P)
# convex_hull=Divide_And_Conquer_Convex_Hull(P)
# Display_Convex_Hull(convex_hull)
# convex_hull=Incremental_Convex_Hull(P)

def T(P):
	P=Simplify_With_X_i(P[P[:,0].argsort()])
	l=len(P)
	A,ia=II(P[:l//2])
	B,ib=II(P[l//2:])
	Display_Convex_Hull(A)
	plt.scatter(A[ia][0],A[ia][1])
	plt.scatter(A[0][0],A[0][1])
	Display_Convex_Hull(B)
	plt.scatter(B[ib][0],B[ib][1])
	plt.scatter(B[0][0],B[0][1])
	C=Combin_Convex_Hull_M_2(A,B,ia)[0]
	Display_Convex_Hull(C)
	
# T(P)
def II(P):
	L=Incremental_Convex_Hull(P)
	i_xmin=min(enumerate(L), key=lambda x: x[1][0])[0]
	if i_xmin!=0:
		L=L[i_xmin:]+L[:i_xmin]
	return L, max(enumerate(L), key=lambda x: x[1][0])[0]
	
	
T(P)


def T2(P):
	C=Divide_And_Conquer_Convex_Hull(P)
	Display_Convex_Hull(C)
	
	
# T2(P)

def T3(P):
	C=Incremental_Convex_Hull_Sort(P)
	Display_Convex_Hull(C)
	
# T3(P)

def T4(P):
	C=Incremental_Convex_Hull_Sort(P)
	Display_Convex_Hull(C)
	x = np.random.uniform(10, 20)
	# 生成纵坐标，范围在-1到7之间  
	y = np.random.uniform(-1, 7)  
	# 创建一个一维数组包含x和y  
	point = np.array([x, y])
	plt.scatter(x,y)
	D,_=Convex_Hull_Sorted_Increment(C,point)
	Display_Convex_Hull(D)
	
# T4(P)
# i_xmin=min(enumerate(convex_hull), key=lambda x: x[1][0])[0]
# if i_xmin!=0:
# 	convex_hull=convex_hull[i_xmin:]+convex_hull[:i_xmin]
# i_xmax=max(enumerate(convex_hull), key=lambda x: x[1][0])[0]
# i_xmin=0
# convex_hull=Combin_Convex_Hull_M_2(A,B,a1)
# plt.scatter(convex_hull[i_xmax][0],convex_hull[i_xmax][1])
# plt.scatter(convex_hull[i_xmin][0],convex_hull[i_xmin][1])
# print("i_xmin:",i_xmin)

plt.show()