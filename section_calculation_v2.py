import numpy as np
import matplotlib.pyplot as plt

class node:
    def __init__(self,idx,x,y):
        self.idx = idx
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Node: {self.idx}, x: {self.x}, y: {self.y}"

class wall:
    def __init__(self,node1,node2,t):
        # Nodes
        self.node1 = node1
        self.x1 = node1.x
        self.y1 = node1.y
        self.x2 = node2.x
        self.y2 = node2.y
        self.t = t
        
        # CG and length
        self.xcge = (self.x1+self.x2)/2
        self.ycge = (self.y1+self.y2)/2 
        self.length = np.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2)
        self.area = self.length*self.t
        # Web moment od inertia
        self.iy_axis = self.length**3/12*self.t
        self.theta = np.atan2(self.y2-self.y1,self.x2-self.x1)
        self.ixe = self.iy_axis * np.sin(self.theta)**2
        self.iye = self.iy_axis * np.cos(self.theta)**2
        self.ixye = self.iy_axis/2 * np.sin(2*self.theta)
        
class boom(node):
    def __init__(self,x,y,A):
        super().__init__(x,y)
        self.A = A
        
class seq(node):
    
    pass

n = int(input("Enter number of nodes "))
print()
nodes = [node(0,0,0) for i in range(n)]
for i in range(n):
    print(f"Node: {i}")
    nodes[i].idx = i
    nodes[i].x = float(input(f"Enter x{i}: "))
    nodes[i].y = float(input(f"Enter y{i}: "))
    
nw = int(input("Enter number of walls "))
walls = [wall(0,0,0) for i in range(nw)]
print()

for i in range(n):
    for j in range(n):
        print(nodes[j])
    print()
    walls[i].node1.idx = int(input(f"Choose first node for wall no.{i+1}"))
    walls[i].node2.idx = int(input(f"Choose second node for wall no.{i+1}"))