#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:10:19 2017

@author: teo
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from wrapper import *
import tensorflow as tf

def GetModel(statelen, sentence_len, numchars, tf_mapping):
    ''' Generate the LSTM Keras Model described in the K. Choi work'''
    print('Build model...')
    model = Sequential()
    model.add(LSTM(statelen, return_sequences = True, input_shape = (sentence_len, numchars)))
    model.add(Dropout(0.2))
    model.add(LSTM(statelen, return_sequences = False))
    model.add(Dropout(0.2))
    model.add(Dense(numchars))
    model.add(Activation('softmax'))
    
    #model.compile(loss=caca, optimizer='adam', metrics = ['accuracy', 'categorical_crossentropy'])
    model.compile(loss=[wrap_tonnetz(tf_mapping = tf_mapping)], optimizer='adam', metrics = ['accuracy', 'categorical_crossentropy'])

    return model
