# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:38:17 2017

@author: font
"""

import numpy as np
import math
from Chords2Vec_fun import*
from chordUtil import *
import pickle
import keras.backend as K


#%%
#dist=0 pour une distance en terme de euclid en note, =1 pour une distance euclidean
# Necessite une réduction avant comparaison car ne peux lire uniquement les accord de type maj/min/dim/aug/maj7/min7/7/dim7/hdim7/minmaj7/maj6/min6/9/maj9/min9/sus2/sus4
def distance(A_1,A_2,dist):
    
    #choix distance euclid
    if dist==0:
        
        #créeation d'un euclid note à note
        a=1
        euclid=np.zeros((12,12))
        Ligne_1=np.array([0,2*a,2*a,a,a,a,2*a,a,a,a,2*a,2*a]) #distance par rapport au Do
        euclid[0][:]=Ligne_1   
            
        for i in range (0,11):
            for j in range (0,12):
                euclid[i+1][j]=euclid[i][j-1] #transposition pour toute les autres notes
        
        
        #initialisation 
        
        Accord_1_euclid=mir_label_to_bin_chroma_vec(A_1)
        Accord_2_euclid=mir_label_to_bin_chroma_vec(A_2) 
        #print Accord_1_euclid
        #print Accord_2_euclid
        i_1=[]
        i_2=[]
        distance =0 
        
        #on cherche les "1" dans nos accords
        for k in range (0,12):
            if Accord_1_euclid[k]==1: 
                i_1.append(k)
        
            if Accord_2_euclid[k]==1:
                i_2.append(k)
        
        N_1=len(i_1)
        N_2=len(i_2)
        
        
        #moyenne distance entre une note et toutes les autres de l'autre accord + entre la deuxieme et toute les autre notre de l'autre accord ...          
        for k in range(0,N_1):
                for l in range(0,N_2):
                    distance+=euclid[i_1[k]][i_2[l]]
         
         #renvoi distance normalisé (par rapport au pire cas) et centré
        print ("d_euclid")
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
        

        return distance_eucl/math.sqrt(4*11)
        

        
#%%

def euclid_matrix(mapping):
    dict_alphabet = mapping[1]
    key, alphabet = zip(*dict_alphabet.items())
    key = list(key)
    alphabet = list(alphabet)
    
    cost_start_end = 1
    
    matrix  = [[]]
    
    for i in key:
        print(i)
        matrix_line = []
        for j in key:
            if alphabet[i] in ['_START_','_END_','Start','End'] or alphabet[j] in ['_START_','_END_','Start','End']:
                if alphabet[i] == alphabet[j]:
                    matrix_line.append(0)
                else:
                    matrix_line.append(cost_start_end)
            else:
                cost = distance(alphabet[i], alphabet[j],1)
                matrix_line.append(cost)
            
            
        matrix.append(matrix_line)
        
    return matrix

#%%
def save_euclid_matrix():
    inputs, alphabet, mapping = ParseInput()
    inputs0, alphabet, mapping0 = ReduSeq(inputs, 'a0')
    matrix = euclid_matrix(mapping0)
    pickle.dump(matrix, open('Distances/matrix_eucl_0.p','wb'))

    inputs1, alphabet, mapping1 = ReduSeq(inputs, 'a1')
    matrix = euclid_matrix(mapping1)
    pickle.dump(matrix, open('Distances/matrix_eucl_1.p','wb'))
    
    inputs2, alphabet, mapping2 = ReduSeq(inputs, 'a2')
    matrix = euclid_matrix(mapping2)
    pickle.dump(matrix, open('Distances/matrix_eucl_2.p','wb'))
    
    
    inputs3, alphabet, mapping3 = ReduSeq(inputs, 'a3')
    matrix = euclid_matrix(mapping3)
    pickle.dump(matrix, open('Distances/matrix_eucl_3.p','wb'))
        
    #inputsN, alphabet, mappingN = ReduSeq(inputs, 'N')
    matrix = euclid_matrix(mapping)
    pickle.dump(matrix, open('Distances/matrix_eucl_N.p','wb'))

def load_euclid_matrix(reduction_type):
    if reduction_type == 'N':
        matrix = pickle.load(open('Distances/matrix_eucl_N.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a3':
        matrix = pickle.load(open('Distances/matrix_eucl_3.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a2':
        matrix = pickle.load(open('Distances/matrix_eucl_2.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)        
    elif reduction_type == 'a1':
        matrix = pickle.load(open('Distances/matrix_eucl_1.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)        
    elif reduction_type == 'a0':
        matrix = pickle.load(open('Distances/matrix_eucl_0.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)    
    return tensor_matrix
    
#****************************PROGRAMME PRINCIPAL*************************************
# exemple d'utilisation
"""
A_1="C#:maj"
A_2="F:maj"

print distance (A_1,A_2,0)
print distance(A_1,A_2,1)
"""
