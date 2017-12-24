# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:38:17 2017

@author: font
"""

import numpy as np
import math
from Chords2Vec_fun import*
from chordUtil import *


#%%
#dist=0 pour une distance en terme de tonnetz en note, =1 pour une distance euclidean
# Necessite une réduction avant comparaison car ne peux lire uniquement les accord de type maj/min/dim/aug/maj7/min7/7/dim7/hdim7/minmaj7/maj6/min6/9/maj9/min9/sus2/sus4
def distance(A_1,A_2,dist):
    
    #choix distance tonnetz
    if dist==0:
        
        #créeation d'un Tonnetz note à note
        a=1
        Tonnetz=np.zeros((12,12))
        Ligne_1=np.array([0,2*a,2*a,a,a,a,2*a,a,a,a,2*a,2*a]) #distance par rapport au Do
        Tonnetz[0][:]=Ligne_1   
            
        for i in range (0,11):
            for j in range (0,12):
                Tonnetz[i+1][j]=Tonnetz[i][j-1] #transposition pour toute les autres notes
        
        
        #initialisation 
        
        Accord_1_Tonnetz=mir_label_to_bin_chroma_vec(A_1)
        Accord_2_Tonnetz=mir_label_to_bin_chroma_vec(A_2) 
        #print Accord_1_Tonnetz
        #print Accord_2_Tonnetz
        i_1=[]
        i_2=[]
        distance =0 
        
        #on cherche les "1" dans nos accords
        for k in range (0,12):
            if Accord_1_Tonnetz[k]==1: 
                i_1.append(k)
        
            if Accord_2_Tonnetz[k]==1:
                i_2.append(k)
        
        N_1=len(i_1)
        N_2=len(i_2)
        
        
        #moyenne distance entre une note et toutes les autres de l'autre accord + entre la deuxieme et toute les autre notre de l'autre accord ...          
        for k in range(0,N_1):
                for l in range(0,N_2):
                    distance+=Tonnetz[i_1[k]][i_2[l]]
         
         #renvoi distance normalisé (par rapport au pire cas) et centré
        print ("d_tonnetz")
        return ((distance/N_2)/8)-0.25
        
        
    #choix distance euclidiean
    if dist==1:
        
        #initialisaition
        A_1_red = reduChord(A_1,'N')
        A_2_red = reduChord(A_2, 'N')
        
        Accord_1_eucl=mir_label_to_semitones_vec(A_1_red)
        Accord_2_eucl=mir_label_to_semitones_vec(A_2_red)
        N_1=len(Accord_1_eucl)
        N_2=len(Accord_2_eucl)
        distance_all=np.zeros((N_1,N_2))
        distance_ligne=np.zeros((N_1))
        distance_eucl=0
        
        #print Accord_1_eucl
        #print Accord_2_eucl
        
        #Dictionnaire regroupant les distances euclédienne pour des distances >=7 demis tons
        D= { 11 : 1,
            10 : 2,
            9 : 3 ,
            8 : 4,
            7 : 5}
        
        for k in range (0,N_1):
            for l in range (0,N_2):
                d=Accord_1_eucl[k]-Accord_2_eucl[l]
                
                #lorsque l'intervalle est inférieur à 6 demis tons
                if abs(d)<=6:
                    distance_all[k][l]=math.pow(d, 2)
                
                #lorsque l'intervalle est supérieur à 6 demis tons on se sert du dictionnaire D
                if abs(d)>6:
                    distance_all[k][l]=math.pow(D[abs(d)], 2)
              
            #on concerve uniquement les distances minimum pour la note k_eme de l'accord 1
            distance_ligne[k]=min(distance_all[k])
            
            #on somme toute les distances minimum            
            distance_eucl+=distance_ligne[k]
        
        
        distance_eucl=math.sqrt(distance_eucl)
        
        #on renvoi la distance normalisé pour le pire cas
        
        print ("d_eucli")
        return distance_eucl/math.sqrt(4*11)
        

        
#%%
    
#****************************PROGRAMME PRINCIPAL*************************************
# exemple d'utilisation
"""
A_1="C#:maj"
A_2="F:maj"

print distance (A_1,A_2,0)
print distance(A_1,A_2,1)
"""
