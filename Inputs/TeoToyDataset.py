# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:57:30 2017

@author: teo
"""

from random import randint
import numpy as np
import os

tonality = 'C'
N = 12
pPeriod = [0, 0, 1.0]

def WriteToyDataset(function, name,  K, N):
#    import pdb
#    pdb.set_trace()
    subdirectory = os.getcwd()
    fd = open(os.path.join(subdirectory, name + '.txt'), 'a')
    for k in range(K):
        out = function(N)
        fd.writelines(["%s " % item  for item in out])
    fd.close()
    
def GetProgression(N, tonality, pDegre, pPeriod, notes, scales, Scale, mode, modes):
    sequence = ['Start']
    NoteIncr = np.where(notes==tonality)
    for elmt in scales.items():
        scales[str(elmt[0])] = notes[list((elmt[1]+NoteIncr)%12)]
    
    scale = list()
    for i in range(7):
        scale.append(scales[mode][i] + ':' + modes[Scale[mode][i]])
        
        
    while N > 0:
        chord = np.random.choice(scale, p=pDegre)
        repetition = np.random.choice([1, 2, 4], p = pPeriod)
        N -= repetition
        sequence.extend([chord] * repetition)
    sequence.append('End\n')
    
    return sequence

def GetProgressionScaled(N, tonality, pDegre, pPeriod, notes, scales, Scale, mode, modes):
    sequence = ['Start']
    NoteIncr = np.where(notes==tonality)
    for elmt in scales.items():
        scales[str(elmt[0])] = notes[list((elmt[1]+NoteIncr)%12)]
    
    scale = list()
    for i in range(7):
        scale.append(scales[mode][i] + ':' + modes[Scale[mode][i]])
        
    chord = np.random.choice(scale, p=pDegre)
    sequence.append(chord)
    while N > 0:
        chord = scale[(scale.index(chord)+1)%len(scale)]
        repetition = np.random.choice([1, 2, 4], p = pPeriod)
        N -= repetition
        sequence.extend([chord] * repetition)
    sequence.append('End\n')
    
    return sequence

def BuildSequenceModel(N):
    tonality = 'C'
    
    modes = ['maj', 'min']
    mode = 'maj' #modes[randint(0,len(modes))-1]
    Scale = {'maj' : [0, 1, 1, 0 , 0, 1, 1], 'min' : [1, 1, 0, 0, 1, 1, 0]}    #Dorien

    pDegre = np.zeros(7)
    tmp = 5, 2, 1, 3, 4, 2, 0.5
    pDegre[:] = tmp
    pDegre = pDegre/np.sum(pDegre)
    
    notes = np.array(['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'])
    majeur =  np.zeros(7, dtype='int'); majeur[:] = 0, 2, 4, 5, 7, 9, 11
    mineur = np.zeros(7, dtype='int'); mineur[:] = 0, 2, 3, 5, 7, 9, 10 #Dorien
    scales = {'maj' : majeur, 'min' : mineur}
    
    return GetProgressionScaled(N, tonality, pDegre, pPeriod, notes, scales, Scale, mode, modes)
