# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:24:31 2017

@author: octav
"""


import numpy as np
from random import randint

#%%

"""
We use a probability matrix to define which chord is going to follow the 
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
        1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0,
        0, 0, 1, 0, 0, 0, 0, 1, 1 ,0 ,0 ,0
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
        2, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,
        0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0
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
                if i != n-1:
                    ChordSequenceNumber.append(NextChord)
                    ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
                    i = i+1
            LastSwitchProba = SwitchProba
        else:
            SwitchProba = np.random.choice(SwitchChordProba[0],p = SwitchChordProba[1])
            NextChord = np.random.choice(np.arange(1,25), p = p)
            for j in range(SwitchProba):
                if i != n-1:
                    ChordSequenceNumber.append(NextChord)
                    ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
                    i = i+1
            LastSwitchProba = SwitchProba

    return ChordSequenceName, ScaleName

#%%
"""
The scale_generator(n) function generates a chord progression following the 
scale defined by a random chord selected on call. The first chord will be 
selected randomly within the chord pool of the scale, either using the 
mixolydian mode for a major scale, or the melodic descending scale for a minor 
scale. The direction of the chord progession will also be picked randomly.
The function returns the chord progression and the scale name.
The scale generator is based on the ChordWeights matrix. IF YOU CHANGE THIS 
MATRIX, YOU WILL NOT GET A SCALE !!
"""

def scale_generator(n):
    ScaleNumber = randint(1,24)
    ScaleName = Chords[ScaleNumber]
    ChordSequenceNumber = []
    ChordSequenceName = []
    
    p=ChordWeights[ScaleNumber][1:25]
    FirstChord = np.random.choice(np.arange(1,25), p = p)
    ChordSequenceNumber.append(FirstChord)
    ChordSequenceName.append(Chords[ChordSequenceNumber[0]])
    
    ScaleDirection = randint(0,1)*2-1
    
    for i in range(1,n):
        ChordSearch = ChordSequenceNumber[i-1] + ScaleDirection
        if ChordSearch%24 == 1:
            ChordSearch = 1
        elif ChordSearch%24 == 0:
            ChordSearch = 24
        while ChordWeights[ScaleNumber][ChordSearch] == 0:
            ChordSearch = ChordSearch + ScaleDirection
            if ChordSearch%24 == 1:
                ChordSearch = 1
            elif ChordSearch%24 == 0:
                ChordSearch = 24

        ChordSequenceNumber.append(ChordSearch)
        ChordSequenceName.append(Chords[ChordSearch])
    return ChordSequenceName, ScaleName
        
#%%
"""
The period_scale_generator(n) function uses the same structure as the 
scale_generator, but gives the chord progression a periodic 
structure of 4 beats as well. The probabilities of getting 1,2 or 4 chords 
in a row are given by the SwitchChordProba list 
(found in the period_w_seq_generator section).
"""

def period_scale_generator(n):
    ScaleNumber = randint(1,24)
    ScaleName = Chords[ScaleNumber]
    ChordSequenceNumber = []
    ChordSequenceName = []
    
    p=ChordWeights[ScaleNumber][1:25]
    FirstChord = np.random.choice(np.arange(1,25), p = p)

    
    ScaleDirection = randint(0,1)*2-1
    
    i = 0
    SwitchProba = np.random.choice(SwitchChordProba[0],p = SwitchChordProba[1])
    for j in range(SwitchProba):
        ChordSequenceNumber.append(FirstChord)
        ChordSequenceName.append(Chords[FirstChord])
        i = i+1
    LastSwitchProba = SwitchProba
    
    while i < n-1:
        ChordSearch = ChordSequenceNumber[i-1] + ScaleDirection
        if ChordSearch%24 == 1:
            ChordSearch = 1
        elif ChordSearch%24 == 0:
            ChordSearch = 24
        while ChordWeights[ScaleNumber][ChordSearch] == 0:
            ChordSearch = ChordSearch + ScaleDirection
            if ChordSearch%24 == 1:
                ChordSearch = 1
            elif ChordSearch%24 == 0:
                ChordSearch = 24

        if i%4 == 0:
            LastSwitchProba =0
        if LastSwitchProba == 1:
            ChordSequenceNumber.append(ChordSearch)
            ChordSequenceName.append(Chords[ChordSearch])
            i = i+1
            LastSwitchProba = 2
            
        elif LastSwitchProba == 2:
            SwitchProba = randint(1,2)
            for j in range(SwitchProba):
                if i != n-1:
                    ChordSequenceNumber.append(ChordSearch)
                    ChordSequenceName.append(Chords[ChordSearch])
                    i = i+1
            LastSwitchProba = SwitchProba
        else:
            SwitchProba = np.random.choice(SwitchChordProba[0],p = SwitchChordProba[1])

            for j in range(SwitchProba):
                if i != n-1:
                    ChordSequenceNumber.append(ChordSearch)
                    ChordSequenceName.append(Chords[ChordSearch])
                    i = i+1
            LastSwitchProba = SwitchProba

    return ChordSequenceName, ScaleName

#%%
"""
The function 251_chord_progession(n) generates the standard II-V-I chord 
progression massively present in jazz music for a given scale, using chords 
II and V on bar 1 and chord I on bar 2. n is the number of 
chords generated.
"""
def cadence_chord_progression(n):
    ScaleNumber = randint(0,23)
    ScaleName = Chords[ScaleNumber + 1]
    ChordNumber = range(24)
    
    if ScaleNumber%2 == 0: #Minor Scale
        ChordSuite = [
                (ScaleNumber +4)%24, (ScaleNumber + 13)%24,
                ScaleNumber, ScaleNumber
                ]
    elif ScaleNumber%2 == 1: #Major scale
        ChordSuite = [
                (ScaleNumber +4)%24, (ScaleNumber + 13)%24,
                ScaleNumber, ScaleNumber
                ]
    ChordSequenceNumber = []
    ChordSequenceName = []
    
    for i in range(n):
        ChordSequenceNumber.append(ChordSuite[i%4] + 1)
        ChordSequenceNumber.append(ChordSuite[i%4] + 1)
        ChordSequenceName.append(Chords[ChordSuite[i%4] + 1])
        ChordSequenceName.append(Chords[ChordSuite[i%4] + 1])

    return ChordSequenceName, ScaleName

#%%
"""
The function anatole_chord_progression(n) generates the I-VI-II-V major chord 
progression for a random major chord. Each chord will last 2 beats 
(2 instances of the chord). n is the length of our chord sequence.
"""

def anatole_chord_progression(n):
    ScaleNumber = randint(0,11)*2
    ScaleName = Chords[ScaleNumber + 1]
    
    ChordSuite = [
            ScaleNumber, ScaleNumber, 
            (ScaleNumber - 5)%24, (ScaleNumber - 5)%24,
            (ScaleNumber + 5)%24, (ScaleNumber + 5)%24,
            (ScaleNumber +13)%24, (ScaleNumber +13)%24
            ] 
    
    ChordSequenceName = []
    
    for i in range(n):
        ChordSequenceName.append(Chords[ChordSuite[i%8] + 1])
        
    return ChordSequenceName, ScaleName
     
#%%
"""
The function rhythmchanges_chord_progression(n) generates the Rhythm Changes 
major chord progression (I-vi-ii-V-iii-VI-ii-V) for a random major chord. 
Each chord will last 2 beats. n is the length of the sequence. 
"""

#%%
"""
The function descending_modulate_progression(n) generates ii-V-I chord 
progression with modulation for each iteration, the I chord becoming the ii 
chord of the next modulation. Chords ii and V on first bar, chord I on second 
bar. n is the length of the sequence."""