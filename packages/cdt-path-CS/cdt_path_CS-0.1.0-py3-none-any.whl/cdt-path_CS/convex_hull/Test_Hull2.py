import matplotlib.pyplot as plt  
from scipy.spatial import ConvexHull  
import numpy as np  
  
# 生成一些随机点  
points = np.random.rand(30, 2)   
  
# 计算凸包  
hull = ConvexHull(points)  
print(hull)
print(type(hull))
# 绘制原始点  
plt.plot(points[:,0], points[:,1], 'o')  
  
# 绘制凸包  
for simplex in hull.simplices:  
	plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
	print(points[simplex, 0])
	print(type(points[simplex, 0]))
  
plt.show()