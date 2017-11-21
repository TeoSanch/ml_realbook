# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:24:31 2017

@author: octav
"""


import numpy as np
from random import randint

#%%

"""We use a probability matrix to define which chord is going to follow the 
previous one. For each chord, we give an arbitrary weight based on its relation 
with the previous chord (without considering the previous section). We then 
select a random weighted number to selected the next chord. These weight are 
stored in the ChordWeights list, containing the chords number (relative to their 
indices in the Chords list on first row and column and their relative weights 
(between 1 and 5). We then take these weights as power of 2 to increase 
differences and divide row by the sum of its weights to create a probability 
density.
"""

Chords = [
        "", "A", "Am", "Bb", "Bbm", "B", "Bm", "C", "Cm",
        "Db", "Dbm", "D", "Dm", "Eb","Ebm", "E", "Em", 
        "F", "Fm", "Gb", "Gbm", "G", "Gm", "Ab", "Abm"
        ]

ChordWeights = [[
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 
        13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
        ]]

"""
Change this row if you want to change the probabilities for a major scale
Do not change the first number as it's the reference for the chord to which 
these probabilities are defined 
"""
"""
ChordWeights.append([
        1, 5, 2, 1, 1, 2, 5, 2, 2, 3, 4, 5, 3,
        1, 1, 5,2, 2, 1, 2, 5, 3 ,2 ,1 ,1
        ])
"""
ChordWeights.append([
        1, 5, 0, 0, 0, 0, 4, 0, 0, 3, 4, 5, 2,
        0, 0, 5,0, 2, 0, 0, 5, 4 ,0 ,0 ,0
        ])

"""ChordWeights[1][1:25] = [(x^2) for x in ChordWeights[1][1:25]]"""
ChordSumMaj = sum(ChordWeights[1][1:25])
ChordWeights[1][1:25] = [x/ChordSumMaj for x in ChordWeights[1][1:25]]


"""Change this row if you want to change the probabilities for a minor scale.
Do not change the first number as it's the reference for the chord to which 
these probabilities are defined 
"""
"""
ChordWeights.append([
        2, 2, 5, 1, 1, 2, 4, 5, 2, 2, 2, 5, 5,
        1, 1, 5, 4, 3, 2, 2, 2, 3, 1, 1, 1
        ])
"""
ChordWeights.append([
        2, 0, 5, 0, 0, 1, 4, 5, 1, 0, 0, 4, 5,
        0, 0, 5, 0, 3, 0, 0, 0, 3, 0, 0, 0
        ])

"""ChordWeights[2][1:25] = [(x^2) for x in ChordWeights[2][1:25]]"""
ChordSumMaj = sum(ChordWeights[2][1:25])
ChordWeights[2][1:25] = [x/ChordSumMaj for x in ChordWeights[2][1:25]]

for i in range(3,25):
    NextChordWeight = [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]
    NextChordWeight[0] = ChordWeights [0][i]
    NextChordWeight[3:25] = (ChordWeights[i-2][1:23])
    NextChordWeight[1:3] = (ChordWeights[i-2][23:25])   
    ChordWeights.append(NextChordWeight)
    

#%%
"""
The weighted_sequence_generator(n) function uses the previous probability matrix 
to generate a chord sequence of length n. For each instance, the function will 
draw a random chord from our list and choose a random sequence of chords to 
follow, using the probability density of the first chord selected. The function 
returns a list containing the chords names. 
"""
def weighted_sequence_generator(n):
    ChordSequenceNumber = [randint(1,24)]
    ChordSequenceName = [Chords[ChordSequenceNumber[0]]]

    for i in range(1,n):
        p = ChordWeights[ChordSequenceNumber[0]][1:25]
        NextChord = np.random.choice(np.arange(1,25), p = p)
        ChordSequenceNumber.append(NextChord)
        ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
    
    return ChordSequenceName


#%%
"""
The period_w_seq_generator(n) function uses the same structure as the 
weighted_sequence_generator, but gives the chord progression a periodic 
structure of 4 beats as well. The probabilities of getting 1,2 or 4 chords 
in a row are given by the SwitchChordProba list.
"""

SwitchChordProba = [
        [1, 2, 4],
        [0.1, 0.3, 0.6],
        ]
def period_w_seq_generator(n):
    ScaleNumber = randint(1,24)
    ScaleName = Chords[ScaleNumber]
    ChordSequenceNumber = []
    ChordSequenceName = []
    p=ChordWeights[ScaleNumber][1:25]
    
    i = 0
    SwitchProba = 0
    LastSwitchProba = 0
    while i < n-1:
        if i%4 == 0:
            LastSwitchProba =0
        if LastSwitchProba == 1:
            NextChord = np.random.choice(np.arange(1,25), p = p)
            ChordSequenceNumber.append(NextChord)
            ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
            i = i+1
            LastSwitchProba = 2
            
        elif LastSwitchProba == 2:
            SwitchProba = randint(1,2)
            NextChord = np.random.choice(np.arange(1,25), p = p)
            for j in range(SwitchProba):
                ChordSequenceNumber.append(NextChord)
                ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
                i = i+1
            LastSwitchProba = SwitchProba
        else:
            SwitchProba = np.random.choice(SwitchChordProba[0],p = SwitchChordProba[1])
            NextChord = np.random.choice(np.arange(1,25), p = p)
            for j in range(SwitchProba):
                ChordSequenceNumber.append(NextChord)
                ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
                i = i+1
            LastSwitchProba = SwitchProba

    return ChordSequenceName, ScaleName
    
    
    