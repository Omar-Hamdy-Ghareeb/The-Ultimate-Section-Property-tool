from section_calculation_v2 import node, wall, boom, section
import numpy as np
import matplotlib.pyplot as plt


def ask_user():
    n = int(input("Enter number of nodes "))
    
    nodes = [node(0,0) for i in range(n)]
    for i in range(n):
        print(f"\nNode {i}: ")
        nodes[i].x = float(input(f"Enter x{i}: "))
        nodes[i].y = float(input(f"Enter y{i}: "))
        
    nw = int(input("\nEnter number of walls "))
    walls_arr = []
    print()
    
    for i in range(nw):
        for j in range(n):
            print(nodes[j])
    
        id_1 = int(input(f"\nChoose first node for wall no.{i+1}: "))
        id_2 = int(input(f"\nChoose second node for wall no.{i+1}: "))
        t = float(input(f"\nChoose thickness for wall no.{i+1}: "))
        walls_arr.append(wall(node.all_nodes[id_1],node.all_nodes[id_2],t))
        print()
    walls = wall.all_walls
        
    return walls, nodes, section.xg, section.yg, section.ix, section.iy, section.ixy

walls, nodes, xg, yg, ix, iy, ixy = ask_user()



