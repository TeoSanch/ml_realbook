# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:10:03 2017

@author: teo
"""
from distance_tonnetz_alexis import *
from chord_distance_octave import *
import numpy as np


def onehot2chord(y, mapping):
    alphabet_len = len(mapping[0])
    import pdb
    pdb.set_trace()
    chord = mapping[1][np.where(y == True)[0][0]]
    return chord

def chord2onehot(chord, mapping):
    alphabet_len = len(mapping[0])
    y = np.zeros((alphabet_len), dtype=np.bool)
    y[mapping[0][chord]] = 1
    return y
    
def wrap_euclidian(mapping):
    def euclidian(y_true, y_pred):
        chord_true = onehot2chord(y_true, mapping)
        chord_pred = onehot2chord(y_pred, mapping)
        return distance(chord_true, chord_pred, 1)
    return euclidian  

def wrap_tonnetz(mapping):  
    def tonnetz(y_true, y_pred):
        chord_true = onehot2chord(y_true, mapping)
        chord_pred = onehot2chord(y_pred, mapping)
        return distance_tonnetz(chord_true, chord_pred)
    return tonnetz