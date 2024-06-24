# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:22:06 2024

@author: Acta
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 10:45:09 2024

@author: Acta
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def compute_curl_2d(u, v, x, y):
    N=x.shape[0] 
    M=y.shape [0]
    print(M,N) 
    curl =np.zeros((M,N))
    for j in range(M ):
        for i in range(N ):
            
            if j==0: 
                if  i==0:
                    # aa=x[i+1]-x[i]
                    # print(aa)
                    a=(v[j ,i+1]-v[j ,i])/(x[i+1]-x[i])
                    b=(u[j+1 ,i ]-u[j ,i])/(y[j+1]-y[j])
                    curl[j ,i]=a -b 
                elif i==N-1:
                    a=(v[j ,i]-v[j  ,i-1 ])/(x[i ]-x[i-1])
                    b=(u[j+1 ,i ]-u[j ,i])/(y[j+1]-y[j])
                    curl[j ,i]=a -b  
                else:
                    # aa=y[j+1]-y[j]
                    # print(aa)
                    a=(v[j ,i+1]-v[j  ,i-1 ])/(x[i+1]-x[i-1])
                    b=(u[j+1 ,i ]-u[j ,i])/(y[j+1]-y[j])
                    curl[j ,i]=a-b 
            elif j==M-1: 
                if   i==0:
                    a=(v[j ,i+1]-v[j ,i])/(x[i+1]-x[i])
                    b=(u[j ,i]-u[j -1 ,i])/(y[j]-y[j-1])
                    curl[j ,i]=a -b 
                elif  i==N-1:
                    a=(v[j ,i]-v[j  ,i-1 ])/(x[i ]-x[i-1])
                    b=(u[j ,i]-u[j -1 ,i])/(y[j]-y[j-1])
                    curl[j ,i]=a -b 
                else:
                    a=(v[j ,i+1]-v[j  ,i-1 ])/(x[i+1]-x[i-1])
                    b=(u[j ,i]-u[j -1 ,i])/(y[j]-y[j-1])
                    curl[j ,i]=a -b 
            else:        
                if  i==0:
                    a=(v[j ,i+1]-v[j ,i])/(x[i+1]-x[i])
                    b=(u[j+1 ,i ]-u[j -1 ,i])/(y[j+1]-y[j-1])
                    curl[j ,i]=a-b 
                    #print(a,b)
                elif i==N-1:
                    a=(v[j ,i]-v[j  ,i-1 ])/(x[i ]-x[i-1])
                    b=(u[j+1 ,i ]-u[j -1 ,i])/(y[j+1]-y[j-1])
                    curl[j ,i]=a -b 
                else: 
                    a=(v[j ,i+1]-v[j  ,i-1 ])/(x[i+1]-x[i-1])
                    b=(u[j+1 ,i ]-u[j -1 ,i])/(y[j+1]-y[j-1])
                    curl[j ,i]=a -b  
    return curl

def reduce_matrice (matrice):
   # Supprimer la deuxième ligne
   mask_u = (matrice[:, 2] == 0)
   mask_v = (matrice[:, 3] == 0) 
   # Trouver les indices où les deux vecteurs ne sont pas zéro simultanément
   indices_non_zero = np.where(~(mask_u & mask_v))[0] 
   # Réécrire les vecteurs sans les zéros aux deux endroits
   u  = matrice[:, 2][indices_non_zero]
   v  = matrice[:, 3][indices_non_zero]
   x = matrice[:, 0][indices_non_zero]
   y = matrice[:, 1][indices_non_zero]
   return  x,y,u,v

def val_uniques(name,x):
    valeurs_uniques, occurrences = np.unique(x, return_counts=True) 
    nombre_valeurs_uniques = len(valeurs_uniques) 
    # print("Nombre de valeurs différentes de ",name,":", nombre_valeurs_uniques)
    return nombre_valeurs_uniques,valeurs_uniques

def axis_Interval(name_axis,axis1,  axis2  , u ,v, axis_min= None,axis_max=None): 
    if axis_max is not None and axis_min is not None:
        indices_restant = np.where((axis1 >= axis_min) & (axis1 <= axis_max))[0]
        axis1=axis1[indices_restant]  
        nombre_valeurs_uniques , zz  = val_uniques(name_axis,axis1)
        axis2=axis2[indices_restant]
        u=u[indices_restant] 
        v=v[indices_restant] 
    return axis1, axis2 , u ,v,nombre_valeurs_uniques

def reshape_all(x,y,u,v,Y_grid_pt_nber,X_grid_pt_nber):
    u=u.reshape(Y_grid_pt_nber,X_grid_pt_nber)
    v=v.reshape(Y_grid_pt_nber,X_grid_pt_nber)
    x=x.reshape(Y_grid_pt_nber,X_grid_pt_nber)
    y=y.reshape(Y_grid_pt_nber,X_grid_pt_nber)
    return x,y,u,v

def axis_Interval_1(name_axis,axis1,  axis2  , u ,v,NBR, axis_min= None ): 
    if  axis_min is not None:
        indices_restant = np.where( axis1 >= axis_min  )[0] 
        axis=axis1[indices_restant]  
        nombre_valeurs_uniques,valeurs_uniques = val_uniques(name_axis,axis) 
        axis1, axis2 , u ,v,nombre_valeurs_uniques=axis_Interval(name_axis,axis1,  axis2  , u ,v, axis_min= valeurs_uniques[0],axis_max=valeurs_uniques[NBR-1])
    else: 
        nombre_valeurs_uniques, zz = val_uniques(name_axis,axis1)
    return axis1, axis2 , u ,v,nombre_valeurs_uniques

def run():
    chemin="D:\\Merveille_TALLA\\PIV_MPd(2x16x16_75%ov_ImgCorr)\\B0200.txt"
    with open(chemin , 'r') as fichier:
            lignes = fichier.readlines()[1:]
    # Construire la matrice à partir des données lues
            matrice = []
            for ligne in lignes:
                elements = ligne.strip().split(';')
                elements_numeriques = [float(element) for element in elements]
                matrice.append(elements_numeriques)
        # Convertir la liste de listes en un tableau NumPy
            matrice = np.array(matrice)
            
            mat_shape=matrice.shape
            print("ligne_mat_size=",mat_shape)
            x = matrice[:, 0]
            y = matrice[:, 1]
            u = matrice[:, 2]
            v = matrice[:, 3] 
            
            x,y,u,v, X_grid_pt_nber=axis_Interval_1('x',x, y, u ,v,NBR=480, axis_min= -40     )
            y,x,u,v, Y_grid_pt_nber=axis_Interval_1('y',y, x, u ,v,NBR=480, axis_min= -38     ) 
            x,y,u,v=reshape_all(x,y,u,v,Y_grid_pt_nber,X_grid_pt_nber) 
            # print("u_shape:", u.shape)
            # print("v_shape:", v.shape)
 

            curl_F = compute_curl_2d( u, v,x[0,:],y[:,0])
            print("Rotationnel de F  ", curl_F.shape)
            #print("Rotationnel de F :\n", curl_F)
            plt.figure()
            plt.imshow(curl_F,vmin=-5, vmax=5)
            plt.colorbar()
 
# run()

def rotationnelle(data, name, composante='V'): 
    grid_path="D:\\Merveille_TALLA\\codes\\vitesse_2D_devis_1\\grid_x_y_"+composante+"\\xy_grid_points.npy" 
    grid_XY = np.load( grid_path,allow_pickle=True)   
    # print("nom_fichier=",chemin ) 
    # data = np.load( chemin ,allow_pickle=True)
    # print(data[1,:,:,0].shape)
    curl_F=[]
    if len(data)==4:
        curl_F = compute_curl_2d( data[0,:,:,0], data[1,:,:,0],grid_XY[0,0,:],grid_XY[1,:,0])
    else:
        curl_F = compute_curl_2d( data[0,:,:], data[1,:,:],grid_XY[0,0,:],grid_XY[1,:,0])
    print("Rotationnel de F :\n", curl_F.shape) 
    plt.figure()
    plt.title( f"Rot  de { name }")
    plt.imshow(curl_F,vmin=-5, vmax=5)
    plt.colorbar()
 
def from_npy_file_folder1(chemin,N_image,composante):
    count=0
    grid_path="D:\\Merveille_TALLA\\codes\\vitesse_2D_devis\\grid_x_y_"+composante+"\\xy_grid_points.npy" 
    grid_XY = np.load( grid_path,allow_pickle=True)
    
    for nom_fichier in os.listdir( chemin ):
        if nom_fichier.lower().endswith(('.npy')) and not nom_fichier.lower().endswith(('final.npy')): 
            if count < N_image:  
                print("nom_fichier=",nom_fichier)
                fichier = os.path.join(chemin , nom_fichier) 
                data = np.load( fichier,allow_pickle=True)
                # print(data[1,:,:,0].shape)
                curl_F = compute_curl_2d( data[0,:,:,0], data[1,:,:,0],grid_XY[0,0,:],grid_XY[1,:,0])
                print("Rotationnel de F :\n", curl_F.shape) 
                plt.figure()
                plt.title( f"Rot  de {nom_fichier}")
                plt.imshow(curl_F,vmin=-5, vmax=5)
                plt.colorbar()
            count+=1

# chemin="D:\Merveille_TALLA\codes\DiffusionWavelet\logs\sentinel-db4-periodic-1-all-quadratic-cmult12244-sample90000-uniform128"
# N_image=4
# composante='V'
# from_npy_file_folder1(chemin,N_image,composante) 