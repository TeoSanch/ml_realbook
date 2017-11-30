#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 00:20:51 2017

@author: teo
"""
import numpy as np


def GetSentences(inputs, sentence_len, step):
    sentences = []
    next_chars = []
    for i in range(0, len(inputs) - sentence_len, step):
        sentences.append(inputs[i: i + sentence_len])
        next_chars.append(inputs[i + sentence_len])
    print('number of sequences :', len(sentences))
    return sentences, next_chars

def Encode(sentences, next_chars, mapping):
    alphabet_len = len(mapping[0])
    sentence_len = len(sentences[0])
    print('Vectorization...')
    x = np.zeros((len(sentences), sentence_len, alphabet_len), dtype=np.bool)
    y = np.zeros((len(sentences), alphabet_len), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, mapping[0][char]] = 1
        y[i, mapping[0][next_chars[i]]] = 1
    return x, y
    
#def Decode()





     