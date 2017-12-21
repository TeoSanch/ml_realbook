# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 13:38:17 2017

@author: font
"""

import numpy as np
import math
from Chords2Vec_fun import*

#%%
def Chord_decomposition(initChord, alpha= 'a1'):
    
    QUALITIES = {
    #           1     2     3     4  5     6     7
    'maj':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'min':     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'aug':     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'dim':     [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'sus4':    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    'sus2':    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    '7':       [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'maj7':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min7':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'minmaj7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'maj6':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'min6':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    'dim7':    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    'hdim7':   [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'maj9':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min9':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '9':       [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'b9':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '#9':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'min11':   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '11':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '#11':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'maj13':   [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min13':   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '13':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'b13':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '1':       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    '5':       [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    '': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    
    a1 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'N',
    'dim':     'dim',
    'sus4':    'N',
    'sus2':    'N',
    '7':       'maj',
    'maj7':    'maj',
    'min7':    'min',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj',
    'min9':    'min',
    '9':       'maj',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'min',
    '1':       'N',
    '5':       'N',
    '': 'N'}

    a2 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'N',
    'dim':     'dim',
    'sus4':    'N',
    'sus2':    'N',
    '7':       '7',
    'maj7':    'maj7',
    'min7':    'min7',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim7',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj7',
    'min9':    'min7',
    '9':       '7',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'min',
    '1':       'N',
    '5':       'N',
    '': 'N'}

    a3 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'aug',
    'dim':     'dim',
    'sus4':    'sus2',
    'sus2':    'sus2',
    '7':       '7',
    'maj7':    'maj7',
    'min7':    'min7',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim7',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj7',
    'min9':    'min7',
    '9':       '7',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'min',
    '1':       'N',
    '5':       'N',
    '': 'N'}

    
    root, qual = initChord.split(":") if ":" in initChord else (initChord, "")
    qual, up = qual.split("(") if "(" in qual else (qual, "")
    qual, up = qual.split("/") if "/" in qual else (qual, "")
    
    if alpha == 'a1':
        qual = a1[qual]
    elif alpha == 'a2':
        qual = a2[qual]
    elif alpha == 'a3':
        qual = a3[qual]
    else:
        print("wrong alphabet value")
        #break
    if qual == "N":
        finalChord = "N"
        Accord_new=finalChord
    else:
        finalChord = [root,qual]      
    
    
        Note_label=np.array(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])

    
        Accord_new=QUALITIES[finalChord[1]]
        
    
        incr=np.where(finalChord[0]==Note_label)
        incr=incr[0][0]
        
        for k in range (0,12):
            while Accord_new[k]==1:
                Accord_new[k]=Note_label[(k+incr)%12]
                
        Accord_new = [i for i in Accord_new  if i != 0] 

        
        
    return Accord_new    
        

#%%
#dist=0 pour une distance en terme de tonnetz en note, =1 pour une distance euclidean

def distance(A_1,A_2,dist):
    
    Note_label=np.array(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])    
    
    
    #création du Tonnetz avec pour longueur caractéristique "a"       
    a=1
    Tonnetz=np.zeros((12,12))
    Ligne_1=np.array([0,2*a,2*a,a,a,a,2*a,a,a,a,2*a,2*a]) #distance de Do avec toutes les autre notes
    Tonnetz[0][:]=Ligne_1
            
           
    for i in range (0,11):
        for j in range (0,12):
            Tonnetz[i+1][j]=Tonnetz[i][j-1]

    
    
   
    #choix distance tonnetz
    if dist==0:
        
        #initialisation 
        Accord_1_Tonnetz=Chord_decomposition(A_1,"a3")
        print(Accord_1_Tonnetz)
        Accord_2_Tonnetz=Chord_decomposition(A_2,"a3") 
        print(Accord_2_Tonnetz)
        
        N_1=len(Accord_1_Tonnetz)
        N_2=len(Accord_2_Tonnetz)
        i_1=np.zeros((N_1,1))
        i_2=np.zeros((N_2,1))
        distance =0 
    
    
        #recherche indice 
        for k in range(0,N_1): 
            if np.any(Note_label==Accord_1_Tonnetz[k]):
                i_1[k]=np.where(Note_label==Accord_1_Tonnetz[k])
            
        for k in range(0,N_2):
            if np.any(Note_label==Accord_2_Tonnetz[k]):
                i_2[k]=np.where(Note_label==Accord_2_Tonnetz[k])
        
    
        #moyenne distance entre une note et tout les autres de l'autre accord + entre la deuxieme et toute les autre notre de l'autre accord ...          
        for k in range(0,N_1):
                for l in range(0,N_2):
                    distance+=Tonnetz[int(i_1[k][0])][int(i_2[l][0])]
        return distance/N_1-2
     
     
    #choix distance euclidiean
    if dist==1:
        
        #initialisaition
        Accord_1_eucl=mir_label_to_semitones_vec(A_1)
        Accord_2_eucl=mir_label_to_semitones_vec(A_2)
        N_1=len(Accord_1_eucl)
        N_2=len(Accord_2_eucl)
        distance_all=np.zeros((N_1,N_2))
        distance_ligne=np.zeros((N_1))
        distance_eucl=0
        
        
        for k in range (0,N_1):
            for l in range (0,N_2):
                distance_all[k][l]=math.pow((Accord_2_eucl[l] - Accord_1_eucl[k]), 2)
            distance_ligne[k]=min(distance_all[k])
            distance_eucl+=distance_ligne[k]
        
        distance_eucl=math.sqrt(distance_eucl)
        
        return distance_eucl
        

        
#%%
    
#****************************PROGRAMME PRINCIPAL*************************************
# exemple d'utilisation

"""A_1="A:min7"
A_2="E:dim"

print distance(A_1,A_2,0)
print distance(A_1,A_2,1)"""
