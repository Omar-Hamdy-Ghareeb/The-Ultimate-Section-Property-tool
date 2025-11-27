import numpy as np
import matplotlib.pyplot as plt



class node:
    n_id = 0
    all_nodes = {}

    
    def __init__(self,x,y):
        
        self.id = node.n_id
        node.n_id +=1
        self.adj_dict = {}
        self.rank = 0
        self.x = x
        self.y = y
        
        node.all_nodes[self.id] = self
        
    def __repr__(self):
        return f"{self.id}:{self.x},{self.y}"

class wall:
    
    wall_id = 0
    
    all_walls = {}

    
    def __init__(self,node1,node2,t):
        # Nodes
        self.id = wall.wall_id
        self.node1 = node1
        self.node2 = node2
        wall.all_walls[self.id] = self
        
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
        
        section.get_cg()
        section.get_i()
        
    
    def adjacent(self):
        self.node1.adj_dict[self.node2.id] = self
        self.node2.adj_dict[self.node1.id] = self
        self.node1.rank = len(self.node1.adj_dict)
        self.node2.rank = len(self.node2.adj_dict)
   
        
     
class boom():
    
    all_booms = {}
    
    def __init__(self,boom_node,A):
        self.node = boom_node
        boom.all_booms[node] = self
        self.A = A
        self.x = node.x
        self.y = node.y
        
        section.get_cg()
        section.get_i()
        
        
class section():
    
    def get_cg():
        
        area_w = 0
        area_b = 0
        xgw = 0
        ygw = 0
        xgb = 0
        ygb = 0
        
        # Area first
        
        for wall_i in wall.all_walls.values():
            area_w += wall_i.area
            
            
        for boom_i in boom.all_booms.values():
            section.area_b += boom_i.A
            
        section.total_area = area_w + area_b ### Total Area
            
        # Wall CG
        
        for wall_i in wall.all_walls.values():
            xgw += wall_i.xcge*wall_i.area/section.total_area
            ygw += wall_i.ycge*wall_i.area/section.total_area
        
        # Boom CG
        for boom_i in boom.all_booms.values():
            xgb += boom_i.x * boom_i.A/section.total_area
            ygb += boom_i.y * boom_i.A/section.total_area
        
        section.xg = xgb + xgw ## Xcg
        section.yg = ygb + ygw ## Ycg
            
        return section.xg,section.yg
        
    def get_i():
        
        ixw = 0
        iyw = 0
        ixyw = 0
        ixb = 0
        iyb = 0
        ixyb = 0
        
        for wall_i in wall.all_walls.values():
            ixw += wall_i.ixe + wall_i.area*(wall_i.ycge-section.yg)**2
            iyw += wall_i.iye + wall_i.area*(wall_i.xcge-section.xg)**2
            ixyw += wall_i.ixye + wall_i.area*(wall_i.ycge-section.yg)*(wall_i.xcge-section.xg)
        
        for boom_i in boom.all_booms.values():
            ixb += boom_i.A*(boom_i.y-section.yg)**2
            iyb += boom_i.A*(boom_i.x-section.xg)**2
            ixyb += boom_i.A*(boom_i.y-section.yg)*(boom_i.x-section.xg)
            
        section.ix = ixw + ixb
        section.iy = iyw + iyb
        section.ixy = ixyw + ixyb
        
        return section.ix,section.iy,section.ixy

    