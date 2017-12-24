# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:29 2017

@author: teo
"""

from encoding import *
from model_test import *
from training import *
from generation import *
from reduction import *
import os.path
import pickle
import pdb
from chord_distance_octave import *

def mainN():

    ''' User interface to launch training, or generation using a trained model'''
    #c1 = input('Train or generate? [t/g] ')
    c1 = 't'
    if c1 == 't':
        name = 'training_N'
        filename = 'Inputs\chord_sentences.txt'
        inputs, alphabet, mapping = ParseInput(filename)
        preredutype = 'N'
        if preredutype != 'N':
            inputs, alphabet, mapping = ReduSeq(inputs, preredutype)
        tf_mapping = load_tonnetz_matrix(preredutype)
        ### Tonnetz distance matrix
        #tonnetz_matrix = 
        ###
        sentence_len = int(16)
        step = int(5)
        sentences, next_chars = GetSentences(inputs, sentence_len, step)
        x, y = Encode(sentences, mapping, next_chars)
        #%%
        batch_size = int(512)
        nb_epoch = int(60)
        model = GetModel(batch_size, sentence_len, len(alphabet),tf_mapping)
        history = RefinedTrain(model, x, y, batch_size, nb_epoch)
        pickle.dump(history, open('%s_history.p' %name, "wb"))
        SaveModel(model, name,'./Models/')
    return 0

def main3():
    ''' User interface to launch training, or generation using a trained model'''
    #c1 = input('Train or generate? [t/g] ')
    c1 = 't'
    if c1 == 't':
        name = 'training_a3'
        filename = 'Inputs\chord_sentences.txt'
        inputs, alphabet, mapping = ParseInput(filename)
        preredutype = 'a3'
        if preredutype != 'a3':
            inputs, alphabet, mapping = ReduSeq(inputs, preredutype)
        tf_mapping = load_tonnetz_matrix(preredutype)
        ### Tonnetz distance matrix
        #tonnetz_matrix = 
        ###
        sentence_len = int(16)
        step = int(5)
        sentences, next_chars = GetSentences(inputs, sentence_len, step)
        x, y = Encode(sentences, mapping, next_chars)
        #%%
        batch_size = int(512)
        nb_epoch = int(60)
        model = GetModel(batch_size, sentence_len, len(alphabet),tf_mapping)
        history = RefinedTrain(model, x, y, batch_size, nb_epoch)
        pickle.dump(history, open('%s_history.p' %name, "wb"))
        SaveModel(model, name,'./Models/')
    return 0

    
    


