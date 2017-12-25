#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:10:19 2017

@author: teo
"""

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
import keras.backend as K

def GetModel(statelen,
             sentence_len,
             numchars,
             tf_mapping,
             loss = 'categorical_crossentropy'):
    ''' Generate the LSTM Keras Model described in the K. Choi work'''
    print('Build model...')
    model = Sequential()
    model.add(LSTM(statelen,
                   return_sequences = True,
                   input_shape = (sentence_len, numchars)))
    model.add(Dropout(0.2))
    model.add(LSTM(statelen, return_sequences = False))
    model.add(Dropout(0.2))
    model.add(Dense(numchars))
    model.add(Activation('softmax'))

    if loss == 'categorical_crossentropy':
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', 
                      metrics = ['accuracy'])
    elif loss == 'tonnetz':
        model.compile(loss=[wrap_loss_function(tf_mapping = tf_mapping)],
                      optimizer='adam',
                      metrics = ['accuracy', 'categorical_crossentropy'])
    elif loss == 'euclidian':
        model.compile(loss=[wrap_loss_function(tf_mapping = tf_mapping)],
                      optimizer='adam',
                      metrics = ['accuracy', 'categorical_crossentropy'])
    else:
        raise ValueError('Cost function named '+loss+' not defined')

    return model

def wrap_loss_function(tf_mapping):
    def loss_function(y_true, y_pred):

        mat1 = K.dot(y_pred, tf_mapping)
        vect = K.transpose(y_true)
        loss = K.dot(mat1,vect)
        
        return loss

    return loss_function