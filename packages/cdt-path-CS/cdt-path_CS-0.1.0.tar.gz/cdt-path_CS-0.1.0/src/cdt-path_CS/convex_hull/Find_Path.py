def find_path(edges):  
    # 创建一个字典来存储每个点的邻居  
    graph = {}  
    for edge in edges:  
        start, end = edge  
        if start not in graph:  
            graph[start] = [end]
        else:  
            graph[start].append(end)  
        if end not in graph:  
            graph[end] = [start] if start != end else []  # 避免自环  
        else:  
            if start not in graph[end]:  # 避免重复添加边  
                graph[end].append(start)  
      
    # 选择一个起始点（可以是列表中的任意一个点）  
    start_point = list(graph.keys())[0]  
      
    # 初始化路径和访问过的点集合  
    path = [start_point]  
    visited = set([start_point])  
      
    # 当前点  
    current_point = start_point  
      
    # 当路径没有闭合且还有未访问的点时，继续遍历  
    while current_point not in path[0:-1] and len(visited) < len(graph):  
        # 获取当前点的邻居中未访问过的点  
        neighbors = [n for n in graph[current_point] if n not in visited]  
          
        # 如果没有未访问的邻居，说明路径中断了，返回None  
        if not neighbors:  
            return None  
          
        # 选择一个邻居作为下一个点（这里简单地选择第一个）  
        next_point = neighbors[0]  
          
        # 将下一个点添加到路径中，并标记为已访问  
        path.append(next_point)  
        visited.add(next_point)  
          
        # 移动到下一个点  
        current_point = next_point  
      
    # 如果回到了起始点，返回完整的路径  
    if current_point == path[0]:  
        return path  
    else:  
        # 如果没有回到起始点，路径不闭合，返回None  
        return None  
  
# 示例边列表  
edges = [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E'], ['E', 'A']]  
  
# 调用函数找到路径  
path = find_path(edges)  
  
# 打印结果  
if path:  
    print(path)  
else:  
    print("无法找到闭合路径")