#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:10:19 2017

@author: teo
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM


def GetModel(statelen, sentence_len, numchars):
    ''' Generate the LSTM Keras Model described in the K. Choi work'''
    print('Build model...')
    model = Sequential()
    model.add(LSTM(statelen, return_sequences = True, input_shape = (sentence_len, numchars)))
    model.add(Dropout(0.2))
    model.add(LSTM(statelen, return_sequences = False))
    model.add(Dropout(0.2))
    model.add(Dense(numchars))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
    return model
