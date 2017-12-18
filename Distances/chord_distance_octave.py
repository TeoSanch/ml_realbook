# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 21:02:30 2017

@author: octav
"""

""" 
The function distance_tonnetz returns a distance measurement based on the 
number of trasnformations in the tonnetz space necessary to go from one chord 
to another. It can only perform this result for major and minor chords.
"""

from Chords2Vec_fun import*
from chordUtil import*

root_list = ["c", "c#", "d", "eb", "e", "f", "f#", "g", "g#", "a", "bb", "b"]
             
def distance_tonnetz(Chord1, Chord2):
    
    
    #use Chords2Vec functions to get the chords roots and types
    
    root_1, type_1 = parse_mir_label(Chord1)
    root_2, type_2 = parse_mir_label(Chord2)
    
    #use Chords2Vec functions to normalize the chords roots 
    #(matching the root_list above)
    root_1 = normalized_note(root_1)
    root_2 = normalized_note(root_2)
    
    #define the costs of each Tonnetz movement
    L_cost = 1
    R_cost = 1
    P_cost = 1
    
    #define the cost of a noneType chord (augmented, diminished etc)
    noneType_cost = 1
    
    #define the cost of a reduction
    reduction_cost = 0.2
    
    suite = ['L']
    
    costs = []
    
    matching_suite = []
    
    #if the two chords are the same, the cost is zero
    if root_1 == root_2 and type_1 == type_2:
        costs.append(0)
    else:
        
        #Reduce chords to maj, min or noneType
        a,type_1 = parse_mir_label(reduChord(Chord1,'a0'))
        a,type_2 = parse_mir_label(reduChord(Chord2, 'a0'))
        
        
        #test if the chords matches after reduction
        if root_2 == root_1:
            if type_2 == type_1:
                matching_suite.append("")
                costs.append(reduction_cost)
            elif type_2 == "n" or type_1 == "n":
                matching_suite.append("")
                costs.append(reduction_cost+noneType_cost)
                
                
        #if at least one of the chord is a noneType, perform the 
        #distance_tonnetz by replacing its type. The function will return the 
        #smallest distance between a major or minor chord for the replacing 
        #type, added to the noneType_cost 
        
        if type_1 == "n" and type_2 == "n":
            costs.append(distance_tonnetz(root_1+":maj",root_2+":maj")+noneType_cost)
            costs.append(distance_tonnetz(root_1+":maj",root_2+":min")+noneType_cost)
            costs.append(distance_tonnetz(root_1+":min",root_2+":maj")+noneType_cost)
            costs.append(distance_tonnetz(root_1+":min",root_2+":min")+noneType_cost)
        elif type_1=="n":
            costs.append(distance_tonnetz(root_1+":maj",root_2+":"+type_2)+noneType_cost)
            costs.append(distance_tonnetz(root_1+":min",root_2+":"+type_2)+noneType_cost)
        elif type_2 == "n":
            costs.append(distance_tonnetz(root_1+":"+type_1,root_2+":maj")+noneType_cost)
            costs.append(distance_tonnetz(root_1+":"+type_1,root_2+":min")+noneType_cost)
        
        #perform the tonnetz_distance for major and minor chords
        else:
        
            #loop to test all combined suites of 4 tonnetz transformations (4 is enough as it'll render all major and minor chords)   
            while len(suite)<5:
           
                root_transform = root_2
                type_transform = type_2
            
            

                #for each element in the tranformation suite, apply the transform
                for i in suite:
                    if i == 'L':
                        root_transform, type_transform = L_transform(root_transform, type_transform)
                    
                    elif i=='R':
                        root_transform, type_transform = R_transform(root_transform, type_transform)
                    elif i=='P':
                        root_transform, type_transform = P_transform(root_transform, type_transform)
            
            #if the transformed chord matches the first chord, store the suite and its cost
                if root_transform == root_1:
                    if type_transform == type_1:
                        matching_suite.append(list(suite))
                        costs.append(int(cost_count(suite,L_cost, R_cost, P_cost))+reduction_cost)
                   

            #change the suite 
                for i in range(len(suite)):
                    if suite[i]=='L':
                        suite[i] = 'R'                 
                        break
                
                    elif suite[i]=='R':
                        suite[i] = 'P'
                        break
                
                    elif suite[i]=='P':
                        if i == len(suite)-1:
                            suite.append('L')
                            suite[i]='L'
                            break
                        else:
                            suite[i] = 'L'
                        
    #Search fo the minimal cost inside all possible suites               
    cost = min(costs)
                
    return cost


#Perfom a  L-transform to the given chord
def L_transform(chord_root,chord_type):
    if chord_type == "maj":
        n = (root_list.index(chord_root)+4)%12
        chord_root = root_list[n]
        chord_type = "min"
    elif chord_type == "min":
        n = (root_list.index(chord_root)-4)%12
        chord_root = root_list[n]
        chord_type = "maj"
    return chord_root, chord_type

#Perform a R-transform to the given chord
def R_transform(chord_root, chord_type):
    if chord_type == "maj":
        n = (root_list.index(chord_root)-3)%12
        chord_root = root_list[n]
        chord_type = "min"
    elif chord_type == "min":
        n = (root_list.index(chord_root)+3)%12
        chord_root = root_list[n]
        chord_type = "maj"
    return chord_root, chord_type

#Perform a P-transform to the given chord             
def P_transform(chord_root, chord_type):
    if chord_type == "maj":
        chord_type = "min"
    elif chord_type == "min":
        chord_type = "maj" 
    return chord_root, chord_type


#Count the cost of a given transform suite based on the transformation cost
def cost_count(suite,L_cost,R_cost,P_cost):
    cost = 0
    for i in suite:
        if i=='L':
            cost = cost+L_cost
        elif i=='R':
            cost = cost+R_cost
        elif i=='P':
            cost=cost+P_cost
    
    return cost
    
    