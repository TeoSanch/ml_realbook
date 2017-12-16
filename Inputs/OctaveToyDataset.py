# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 16:24:31 2017

@author: octav
"""

import os
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
(between 1 and 5). We then divide the rows by the sum of their respective 
weights to create a probability density.

For the sake of simplicity, we will only use the mixolydian major scale and 
the melodic descending minor scale for our dataset. We give a weight of zero 
to any chord out of these scale.
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
ChordWeights.append([
        1, 5, 0, 0, 0, 0, 2, 0, 0, 0, 1, 4, 0,
        0, 0, 4, 0, 0, 0, 0, 2, 0.5 ,0 ,0 ,0
        ])

ChordSumMaj = sum(ChordWeights[1][1:25])
ChordWeights[1][1:25] = [x/ChordSumMaj for x in ChordWeights[1][1:25]]


"""Change this row if you want to change the probabilities for a minor scale.
Do not change the first number as it's the reference for the chord to which 
these probabilities are defined 
"""
ChordWeights.append([
        2, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,
        0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0
        ])

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
The weighted_sequence_generator(n) function uses the previous probability 
matrix to generate a chord sequence of length n. For each instance, the 
function will draw a random scale from our list and choose a random sequence 
of chords from its scale, using the probability density of the scale selected. 
The function returns a list containing the chords names and the scale from 
which the chords are drawn.
"""
def weighted_sequence_generator(n):
    ScaleNumber = randint(1,24)
    ScaleName = Chords[ScaleNumber]
    ChordSequenceNumber = []
    ChordSequenceName = []
    
    p = ChordWeights[ScaleNumber][1:25]
    
    for i in range(n):
        NextChord = np.random.choice(np.arange(1,25), p = p)
        ChordSequenceNumber.append(NextChord)
        ChordSequenceName.append(Chords[ChordSequenceNumber[i]])
    
    return ChordSequenceName, ScaleName


#%%
"""
The period_w_seq_generator(n) function uses the same structure as the 
weighted_sequence_generator, but gives the chord progression a periodic 
structure of 4 beats as well. The probabilities of getting 1,2 or 4 chords 
in a row are given by the SwitchChordProba list.
"""

SwitchChordProba = [
        [1, 2, 4],
        [0, 1, 0],
        ]
def period_w_seq_generator(n):
    ScaleNumber = 7 #randint(1,24)
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
The scale generator is based on the ChordWeights matrix. IF YOU CHANGE THIS 
MATRIX, YOU WILL NOT GET A SCALE !!
"""

def period_scale_generator(n):
    ScaleNumber = 7 #randint(1,24)
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
The function cadence_chord_progession(n) generates the standard II-V-I chord 
progression massively present in western music for a given scale, using chords 
II and V on bar 1 and chord I on bar 2. n is the number of 
chords generated.
"""
def cadence_chord_progression(n):
    ScaleNumber = randint(0,23)
    ScaleName = Chords[ScaleNumber + 1]

    
    if ScaleNumber%2 == 1: #Minor Scale
        ChordSuite = [
                (ScaleNumber + 4)%24, (ScaleNumber + 13)%24,
                ScaleNumber, ScaleNumber
                ]
    elif ScaleNumber%2 == 0: #Major scale
        ChordSuite = [
                (ScaleNumber + 5)%24, (ScaleNumber + 14)%24,
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
            (ScaleNumber + 14)%24, (ScaleNumber + 14)%24
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

def rhythmchanges_chord_progression(n):
    ScaleNumber = randint(0, 11)*2
    ScaleName = Chords[ScaleNumber + 1]
    
    ChordSuite = [
            ScaleNumber, ScaleNumber, 
            (ScaleNumber - 5)%24, (ScaleNumber - 5)%24,
            (ScaleNumber + 5)%24, (ScaleNumber + 5)%24,
            (ScaleNumber + 14)%24, (ScaleNumber + 14)%24,
            (ScaleNumber + 9)%24, (ScaleNumber + 9)%24,
            (ScaleNumber - 6)%24, (ScaleNumber - 6)%24,
            (ScaleNumber + 5)%24, (ScaleNumber + 5)%24,
            (ScaleNumber + 14)%24, (ScaleNumber + 14)%24
            ]
    
    ChordSequenceName = []
    
    for i in range(n):
        ChordSequenceName.append(Chords[ChordSuite[i%16] + 1])
        
    return ChordSequenceName, ScaleName
#%%
"""
The function descending_modulate_progression(n) generates ii-V-I chord 
progression with modulation for each iteration, the I chord becoming the ii 
chord of the next modulation. Chords ii and V on first bar, chord I on second 
bar. n is the length of the sequence. This function returns the sequence and 
the first scale of the descent.
"""

def descending_modulate_progression(n):
    FirstScaleNumber = randint(0, 11)*2
    FirstScaleName = Chords[FirstScaleNumber + 1]
    
    ChordSuite = [
            (FirstScaleNumber + 5)%24, (FirstScaleNumber + 5)%24,
            (FirstScaleNumber + 14)%24, (FirstScaleNumber + 14)%24,
            FirstScaleNumber, FirstScaleNumber,
            FirstScaleNumber, FirstScaleNumber
                ]
    ChordSequenceName = []
    ModulationNumber = 0
    
    for i in range(n):
        if i>0 and i%8 == 0:
            ModulationNumber = ModulationNumber + 1 
        ChordSequenceName.append(Chords[
                ((ChordSuite[i%8] -4*ModulationNumber)%24) + 1
                ])
    return ChordSequenceName, FirstScaleName


#%% Some exemple of generated Toy Data Set

# Sequence of 4 chords each time, in the C maj scale.
def write_toy_dataset(function, name,  K, N):
    subdirectory = os.getcwd()
    fd = open(os.path.join(subdirectory, name + '.txt'), 'a')
    for k in range(K):
        out = function(N)
        fd.write('Start ')
        fd.writelines(["%s " % item  for item in out[0]])
        fd.write('End ')
    fd.close()
    