# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:55:40 2024

@author: Acta
"""

import os
import shutil

def create_mkdir_or_not(Liste_chemin):
   for chemin_dossier in   Liste_chemin :
       if os.path.exists(chemin_dossier ):
           shutil.rmtree(chemin_dossier  )
           os.mkdir(chemin_dossier ) 
       else: 
           os.mkdir(chemin_dossier)



# Liste_chemin=["D:/Merveille_TALLA/codes/vitesse_2D_devis/train/0","D:/Merveille_TALLA/codes/vitesse_2D_devis/train/1","D:/Merveille_TALLA/codes/vitesse_2D_devis/train/2"]
# create_mkdir_or_not(Liste_chemin)