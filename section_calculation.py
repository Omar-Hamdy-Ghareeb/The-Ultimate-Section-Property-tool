
import numpy as np
import matplotlib.pyplot as plt

# comment
class section:
        
    def __init__(self,nw,X1,X2,Y1,Y2,t,nb,XB,YB,B):
      self.nw = nw 
      self.web = np.full((nw,4),np.nan)
      self.X1points = X1
      self.X2points = X2
      self.Y1points = Y1
      self.Y2points = Y2
      self.w_len_total = 0
      self.nb = nb
      self.xboom = XB
      self.yboom = YB
      self.B = B
      self.t = t
      self.b_area_total = np.sum(self.B)
      self.Xpoints = np.concatenate((self.X1points,self.X2points))
      self.Ypoints = np.concatenate((self.Y1points,self.Y2points))
      self.points = np.column_stack((self.Xpoints,self.Ypoints))
      self.get_CG()
      self.get_ik()
      self.get_end()
      self.get_principal_axes()

      
    def get_CG(self):
        
        self.length = np.full((self.nw,1),np.nan)

        self.xcgw = 0
        self.ycgw = 0
        self.xcgb = 0
        self.ycgb = 0

        self.xcge = (self.X1points+self.X2points)/2
        self.ycge = (self.Y1points+self.Y2points)/2
        self.length = np.sqrt((self.X2points-self.X1points)**2 + (self.Y2points-self.Y1points)**2)

        self.w_len_total = np.sum(self.length)
        self.w_area_total =  np.sum(np.sqrt((self.X2points-self.X1points)**2 + (self.Y2points-self.Y1points)**2)*self.t)
      
        if(self.w_len_total != 0):
            self.xcgw  = np.sum(self.xcge*self.length*self.t/self.w_area_total)
            self.ycgw  = np.sum(self.ycge*self.length*self.t/self.w_area_total)


        if (self.b_area_total != 0):
            self.xcgb = np.sum(self.xboom * self.B/ self.b_area_total)
            self.ycgb = np.sum(self.yboom * self.B/ self.b_area_total)

        self.xcg = self.xcgb + self.xcgw
        self.ycg = self.ycgb + self.ycgw
        
    def get_ik(self):
        
            iy_axis = self.t*self.length**3/12
            theta = np.zeros(self.nw)
            
            self.ixw = 0
            self.iyw = 0
            self.ixyw = 0
            self.ixb = 0
            self.iyb = 0
            self.ixyb = 0

            if(self.w_len_total != 0):      
                
                    theta = np.atan2(self.Y2points-self.Y1points,self.X2points-self.X1points)
                    ixe = iy_axis * np.sin(theta)**2
                    iye = iy_axis * np.cos(theta)**2
                    ixye = iy_axis/2 * np.sin(2*theta)
        
                    self.ixw = np.sum(ixe + self.length*self.t*(self.ycge-self.ycg)**2)
                    self.iyw = np.sum(iye + self.length*self.t*(self.xcge-self.xcg)**2)
                    self.ixyw = np.sum(ixye + self.length*self.t*(self.ycge-self.ycg)*(self.xcge-self.xcg))
             

            if (self.b_area_total != 0):    
                self.ixb = np.sum(self.B * (self.yboom - self.ycg)**2)
                self.iyb = np.sum(self.B * (self.xboom- self.xcg)**2)
                self.ixyb = np.sum(self.B * (self.yboom- self.ycg)*(self.xboom - self.xcg))
            
            self.ix = self.ixb+self.ixw
            self.iy = self.iyb+self.iyw
            self.ixy = self.ixyb+self.ixyw
            
            self.kb = self.ix * self.iy - self.ixy**2
            self.kx = self.ix/self.kb
            self.ky = self.iy/self.kb
            self.kxy = self.ixy/self.kb
            
            self.slope = -2*self.ixy/(self.ix-self.iy)
            self.beta = 0.5 * np.atan2(-2*self.ixy,self.ix-self.iy)
            
    def get_principal_axes(self):
        
            self.p_axes_scale = 0.1
            
            if (self.w_len_total != 0 ):
                self.p_axes_minx = np.minimum(np.min(self.X1points),np.min(self.X2points))
                self.p_axes_maxx = np.maximum(np.max(self.X1points),np.max(self.X2points))
                self.p_axes_miny = np.minimum(np.min(self.X1points),np.min(self.X2points))
                self.p_axes_maxy = np.maximum(np.max(self.Y1points),np.max(self.Y2points))
            elif (self.b_area_total != 0):
                self.p_axes_minx = np.min(self.xboom)
                self.p_axes_maxx = np.max(self.xboom)
                self.p_axes_miny = np.min(self.yboom)
                self.p_axes_maxy = np.max(self.yboom)
            else:
                self.p_axes_minx = 0 
                self.p_axes_maxx = 1

    def get_end(self):
        
        is_open_end = False
       
        self.open_end = self.points[0,0:2] 
        while not is_open_end:
            for i in range(self.points.shape[0]):
                for j in range(self.points.shape[0]):
                    if np.array_equal(self.points[i,0:2], self.points[j,0:2]):
                        self.open_end = self.points[i,0:2]
                        is_open_end = True
                    else:
                        is_open_end = False
                        
                if is_open_end:
                    break

      

    # =============================================================================
    # 
    # def shear_center(self):
    #   TODO
    # =============================================================================

      

n_b = 1
nw = 1
thickness = np.ones(nw)
boom = np.zeros((1,3))
shape = np.zeros((1,4))

# ------------------------------------Uncomment if testing a section-----------------------------------------
# while(True):
#     is_boom  = input("Does the section contain booms? [Y], [N] ").lower()
    
#     if(is_boom == 'y'):
#         n_b = int(input("Enter Number of booms: "))
#         print()
#         boom = np.zeros((n_b,3))

#         for i in range(n_b):
#              print(f"################# Boom {i+1} #################")
#              print()
#              boom[i,0] = float(input("x: "))
#              boom[i,1] = float(input("y: "))
#              boom[i,2] = float(input("A: "))
#              print("------------------------------------------------------------")
#              print()
#         break
#     elif(is_boom == 'n'):
#         break
    
# while(True):
#     is_web  = input("Does the section contain webs? [Y], [N] ").lower()
#     if(is_web == 'y'):
#         while(True):
#             is_t_const = input("Is the cross section constant (It doesn't work for now')? [Y], [N] ").lower()
#             if(is_t_const == 'y'):
#                 t_const = True
#                 break
#             elif(is_t_const == 'n'):
#                 t_const = False
#                 break
        
#         nw = int(input("Enter Number of webs: "))
#         print()
#         shape = np.zeros((nw,4))
#         if(t_const):
#             thickness = np.ones(nw)
#         else:
#             thickness = np.zeros(nw)

#         for i in range(nw):
#              print(f"################# Web {i+1} #################")
#              print()
#              shape[i,0] = float(input("x1: "))
#              shape[i,2] = float(input("y1: "))
#              print()
#              shape[i,1] = float(input("x2: "))
#              shape[i,3] = float(input("y2: "))
#              if (not t_const):
#                  thickness[i] = input("t: ")
#              print("------------------------------------------------------------")
#              print()
             
#         break
    
#     elif(is_web == 'n'):
#         break
    
# ----------------------------------------- END Of CLI ------------------------------------------------
       


  # -----------------  Example (comment if testing a section) ----------------- 
# nw = 4 
# shape = np.array([[0,1,0,0],[0.5,0.5,0,1],[1,1,0,1],[0.5,1.5,1,1]])
 

# length = np.zeros(nw)
    
# ----------------------------------------------------------------------------- 


# -----------------  Example (comment if testing a section) ----------------- 
nw = 10 
shape = np.array([[0,0,1.2,-1.2,1],    #1
                 [0,6.4,1.2,5.6/2,1], #1
                 [0,6.4,-1.2,-5.6/2,1],   #1
                 [6.4,6.4,5.6/2,-5.6/2,4],    #4
                 [6.4,16.8,5.6/2,3.91/2,2],   #2
                 [6.4,16.8,-5.6/2,-3.91/2,2], #2
                 [16.8,16.8,3.91/2,-3.91/2,2], #2
                 [16.8,22.4,3.91/2,3/2,1],    #1
                 [16.8,22.4,-3.91/2,-3/2,1],  #1
                 [22.4,22.4,3/2,-3/2,1],  #1
                 ])
thickness = shape[:,4]
 

length = np.zeros(nw)
    
# ----------------------------------------------------------------------------- 


# Initializing
shape = section(nw,shape[:,0],shape[:,1],shape[:,2],shape[:,3],thickness[:],n_b,boom[:,0],boom[:,1],boom[:,2])



################  Plotting

# Plotting lines

for i in range(nw):
    
    plt.plot((shape.X1points,shape.X2points),(shape.Y1points,shape.Y2points))
    
    
    
# Plotting principal axes

xp = np.linspace(shape.p_axes_scale*shape.xcg - shape.p_axes_minx ,shape.p_axes_maxx-shape.p_axes_scale*shape.xcg,30)
yp1 = shape.slope* xp - shape.slope *shape.xcg + shape.ycg
yp2 =  -xp/shape.slope + 1/shape.slope *shape.xcg + shape.ycg
plt.plot(xp,yp1,'--')

tol = 1e-6

if abs(shape.slope) < tol:
    plt.plot([shape.xcg, shape.xcg],
    np.linspace(1.2*shape.p_axes_miny,1.2*shape.p_axes_maxy, 2), '--')
    
else:
    plt.plot(xp,yp2,'--')
    
# Plotting booms
for i in range(n_b):
    plt.plot(shape.xboom[i], shape.yboom[i],'o' )
    
    
    
plt.plot(shape.xcg,shape.ycg,'x')
plt.axis('equal')


plt.suptitle( f"Ix = {shape.ix:.4f} d³t | Iy = {shape.iy:.4f} d³t | Ixy = {shape.ixy:.4f} d³t\n" f"kx = {shape.kx:.4f}/(d³t) | ky = {shape.ky:.4f}/(d³t) | kxy = {shape.kxy:.4f}/(d³t)\n" f"β = {np.degrees(shape.beta):.2f}° \n Xg = {shape.xcg:.4f} | Yg = {shape.ycg:.4f}", y=0.98,fontsize=10)
print(f"Ix ={shape.ix:.4f} d^3t ")
print(f"Iy ={shape.iy:.4f} d^3t ")
print(f"Ixy ={shape.ixy:.4f} d^3t ")
print(f"kx = {shape.kx:.4f}/(d^3 t)")
print(f"ky = {shape.ky:.4f}/(d^3 t)")
print(f"kxy = {shape.kxy:.4f}/(d^3 t)")
print(f"beta = {np.degrees(shape.beta):.4f}°")
print()
plt.show()


# =============================================================================
# 
# def shear_center(shape,kx,ky,kxy):
#     is_open_end = False
#     points = np.column_stack((np.concatenate((shape[:,0],shape[:,1])),np.concatenate((shape[:,2],shape[:,3]))))
#     open_end = points[0,0:2]
#     while not is_open_end:
#         for i in range(points[0]):
#             for j in range(points[0]):
#                 if points[i,0:2] != points[j,0:2]:
#                     open_end = points[i,0:2]
#                     is_open_end = True
#                 else:
#                     is_open_end = False
#                     
#             if is_open_end:
#                 break
# =============================================================================

  
