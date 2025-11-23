import numpy as np
import matplotlib.pyplot as plt



class node:
    n_id = 0
    all_nodes = {}

    
    def __init__(self,x,y):
        self.id = node.n_id
        node.n_id +=1
        self.id_dict = {}
        
        self.x = x
        self.y = y
        
        node.all_nodes[self.id] = self
        
    def __repr__(self):
        return f"Node: {self.id}, x: {self.x}, y: {self.y}"

class wall:
    def __init__(self,node1,node2,t):
        # Nodes
        self.node1 = node1
        self.node2 = node2
        self.x1 = node1.x
        self.y1 = node1.y
        self.x2 = node2.x
        self.y2 = node2.y
        self.t = t
        
        self.adjacent()
        
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
        
    def adjacent(self):
        self.node1.id_dict[self.node2.id] = self
        self.node2.id_dict[self.node1.id] = self
        
class boom():
    def __init__(self,boom_node,A):
        self.node = boom_node
        self.A = A
        

def ask_user():
    n = int(input("Enter number of nodes "))
    
    nodes = [node(0,0) for i in range(n)]
    for i in range(n):
        print(f"\nNode {i}: ")
        nodes[i].x = float(input(f"Enter x{i}: "))
        nodes[i].y = float(input(f"Enter y{i}: "))
        
    nw = int(input("\nEnter number of walls "))
    walls = []
    print()
    
    for i in range(nw):
        for j in range(n):
            print(nodes[j])
    
        id_1 = int(input(f"\nChoose first node for wall no.{i+1}: "))
        id_2 = int(input(f"\nChoose second node for wall no.{i+1}: "))
        t = float(input(f"\nChoose thickness for wall no.{i+1}: "))
        walls.append(wall(node.all_nodes[id_1],node.all_nodes[id_2],t))
        print()