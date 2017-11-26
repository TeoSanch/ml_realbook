#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:10:19 2017

@author: teo
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.utils.data_utils import get_file
from keras.callbacks import ModelCheckpoint
import numpy as np
import random
import misc as m
import Generate as g

def get_model(statelen, sentence_len, numchars):
    print('Build model...')
    model = Sequential()
    model.add(LSTM(statelen, return_sequences = True, input_shape = (sentence_len, numchars)))
    model.add(Dropout(0.2))
    model.add(LSTM(statelen, return_sequences = False))
    model.add(Dropout(0.2))
    model.add(Dense(numchars))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

def main():
    inputs , alphabet, mapping = m.ParseInput()
    sentence_len = 100;
    step = 50;
    sentences, next_chars = m.GetSentences(inputs, sentence_size, step)
    x, y = m.Vectorize(sentences, next_chars, mapping)
    batch_size = 512
    nb_epochs = 60
    model = get_model(batch_size, sentence_size, len(alphabet))
    g.SimpleTrain(model, x, y, batch_size, nb_epochs)
    return model

#%%
model = main()
