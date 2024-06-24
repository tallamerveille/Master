# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:14:28 2024

@author: Acta
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
from torch             import device
from torch.cuda        import is_available as is_cuda_available
from create_mkdir_or_not import create_mkdir_or_not
import pywt
import seaborn as sns
from pathlib import Path
from rotationnelle import rotationnelle 

 


def reconstruct_small_resolution(J,approximation, wavelet, border_condition):
    for j in range(J-1, -1, -1):
        print(approximation.shape)
        coeff_diag  = np.zeros(approximation .shape)
        coeff_horiz = np.zeros(approximation .shape)
        coeff_vert = np.zeros(approximation .shape)
        print(np.max(coeff_diag))
        approximation = pywt.idwt2((approximation , (coeff_horiz, coeff_vert, coeff_diag)), wavelet=wavelet, mode=border_condition)   
    return approximation



def reduce_approx_result(data0,approximation):
    NB=approximation.shape[0]-data0.shape[0]
# Indice de la ligne à supprimer (par exemple, la deuxième ligne, donc index 1)
    for j in range(NB):
        index_to_remove = -1 
        # Suppression de la ligne
        approximation = np.delete(approximation, index_to_remove, axis=1)
        approximation = np.delete(approximation, index_to_remove, axis=0) 
    return approximation



def plot ():
    
    chemin0="D:\\Merveille_TALLA\\codes\\vitesse_2D_devis_1\\composante_UV\\test\\0\\B2002_UV.npy"
    chemin0 = Path(chemin0)
    data0 = np.load( chemin0,allow_pickle=True)
    # for i in range(data0.shape[0]):
    #     plt.figure()
    #     titre=chemin0.name+" j=0_"+ str(i)
    #     plt.title(titre)
    #     plt.imshow(data0[i] , vmin=-6, vmax=6 )
    #     plt.colorbar()
    #     print(data0.shape) 
    name = chemin0.name+"( Image originale)"
    rotationnelle(data0, name, composante='V')
    
    J=1
    chemin1="D:\\Merveille_TALLA\\codes\\vitesse_2D_devis_1\\composante_UV\\test\\"+str(J)+"\\B2002_UV.npy"
    chemin1 = Path(chemin1)
    data1 = np.load( chemin1,allow_pickle=True) 
    wavelet = 'db4' 
    border_condition = 'symmetric' #'periodic'
    
    Approximation=[]
    for i in range (data1.shape[0]): 
        approximation= reconstruct_small_resolution(J,data1[i][0], wavelet, border_condition)
        print(" approximation.shape",approximation.shape) 
        approximation = reduce_approx_result(data0[i],approximation) 
        Approximation.append(approximation)
        # plt.figure()
        # titre=chemin1.name+" "+ str(i)+", j="+str(J)
        # plt.title(titre)
        # plt.imshow(approximation , vmin=-6, vmax=6 )
        # plt.colorbar()
    Approximation=np.array(Approximation) 
    name = chemin0.name+"( Image petite echelle)"+", j="+str(J)
    rotationnelle(Approximation, name, composante='V')
    # plt.figure()
    # titre=chemin0.name+" "+str(J)+" iwt"
    # plt.title(titre)
    # plt.imshow(approximation , vmin=-6, vmax=6 )
    # plt.colorbar()
    
    chemin2="D:\\Merveille_TALLA\\codes\\DiffusionWavelet\\logs\\sentinel-db4-periodic-1-all-quadratic-cmult12244-sample300000-uniform128\\B2002_UV_wavelet_x2.npy"
    chemin2 = Path(chemin2)
    data = np.load( chemin2,allow_pickle=True)  
    Approximation=[]
    for i in range (data.shape[0]):  
        approximation = reduce_approx_result(data[i],approximation)  
        print(" approximation.shape",approximation.shape) 
        Approximation.append(approximation)
        # plt.figure()
        # titre=chemin2.name+" "+ str(i)+", j="+str(J)
        # plt.title(titre)
        # plt.imshow(approximation , vmin=-6, vmax=6 )
        # plt.colorbar()
    Approximation=np.array(Approximation) 
    name = chemin2.name+"( Image echantillonée)"+", j="+str(J)
    rotationnelle(Approximation, name, composante='V')
    # for i in range(approximation.shape[0]):
    #     plt.figure()
    #     titre=chemin2.name+" j=0_"+ str(i)
    #     plt.title(titre)
    #     plt.imshow(data0[i] , vmin=-6, vmax=6 )
    #     plt.colorbar()
    #     print(data0.shape) 
    # name = chemin0.name+"( Image originale)"
    # rotationnelle(data0, name, composante='V')
    # plt.figure() 
    # plt.title(chemin0.name )
    # plt.imshow(approximation , vmin=-6, vmax=6 )
    # plt.colorbar()
    plt.show()
    

plot()