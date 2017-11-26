#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:20:51 2017

@author: teo
"""
import numpy as np

def ParseInput(filepath = 'chord_input.txt'):
    """ Parse the input text file into a python array and build the alphabet
    """
    fd = open(filepath).read()
    print('corpus length:', len(fd))
    chord_seq = fd.split(' ')
    chars = set(chord_seq)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    num_chars = len(char_indices)
    print('total chars:', num_chars)
    return chord_seq, chars, (char_indices, indices_char)

def GetSentences(inputs, maxlen, step):
    sentences = []
    next_chars = []
    for i in range(0, len(inputs) - maxlen, step):
        sentences.append(inputs[i: i + maxlen])
        next_chars.append(inputs[i + maxlen])
    print('number of sequences :', len(sentences))
    return sentences, next_chars

def Vectorize(sentences, next_chars, mapping):
    num_chars = len(mapping[0])
    maxlen = len(sentences[0])
    print('Vectorization...')
    x = np.zeros((len(sentences), maxlen, num_chars), dtype=np.bool)
    y = np.zeros((len(sentences), num_chars), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, mapping[0][char]] = 1
        y[i, mapping[0][next_chars[i]]] = 1
    return x, y
    

def ChangeTemperature(vector, temperature=1.0):
    tmp = np.log(vector) / temperature
    out_vector = np.exp(tmp) / sum(np.exp(tmp))
    return np.argmax(np.random.multinomial(1, out_vector, 1))   #???

def LoadCheckpoint(actual_model, pathnewmodel):
    from keras.models import load_model
    import time
    date = time.ctime()
    date = date.replace(' ', '_')
    model.save('model_' + date + '.h5')
    del model
    model = load_model(pathnewmodel)


     