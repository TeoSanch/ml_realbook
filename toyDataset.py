# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:24:31 2017

@author: octav
"""

"""We use a probability matrix to define which chord is going to follow the 
previous one. For each chord, we give an arbitrary weight based on its relation 
with the previous chord (without considering the previous section). We then 
select a random weighted number to selected the next chord. These weight are 
stored in the ChordWeights list, containing the chords number (relative to their indices in the Chords list on first row and column and 
their relative weights (between 1 and 5).
"""
import numpy as np
from random import randint

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
ChordWeights.append([
        1, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0,
        0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0,  
        ])
"""

ChordWeights.append([
        1, 5, 2, 1, 1, 2, 5, 2, 2, 3, 4, 5, 3,
        1, 1, 5,2, 2, 1, 2, 5, 3 ,2 ,1 ,1
        ])


ChordWeights[1][1:25] = [(x^2) for x in ChordWeights[1][1:25]]
ChordSumMaj = sum(ChordWeights[1][1:25])
ChordWeights[1][1:25] = [x/ChordSumMaj for x in ChordWeights[1][1:25]]

"""
ChordWeights.append([
        2, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 
        0, 0, 5, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0
        ])
"""
ChordWeights.append([
        2, 2, 5, 1, 1, 2, 4, 5, 2, 2, 2, 5, 5,
        1, 1, 5, 4, 3, 2, 2, 2, 3, 1, 1, 1
        ])

ChordWeights[2][1:25] = [(x^2) for x in ChordWeights[2][1:25]]
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
    

    
n = 8
ChordNumber = [randint(1,24)]
ChordName = [Chords[ChordNumber[0]]]

for i in range(1,n):
    p=ChordWeights[ChordNumber[0]][1:25]
    print(p)
    print(ChordNumber)
    NextChord = np.random.choice(np.arange(1,25),p = p)
    print(NextChord)
    """
    NumberList = [randint(1,24), randint(1,24), randint(1,24)]
    WeightList = [
            ChordWeights[ChordNumber[i-1]][NumberList[0]],
            ChordWeights[ChordNumber[i-1]][NumberList[1]],
            ChordWeights[ChordNumber[i-1]][NumberList[2]]
            ]
    """
    ChordNumber.append(NextChord)
    ChordName.append(Chords[ChordNumber[i]])
    

print(ChordName)


    
    