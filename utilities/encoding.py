#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Sun Nov 26 00:20:51 2017

@author: teo
'''
import numpy as np
from tkinter import Tk
from tkinter import filedialog


def ParseInput():
    ''' 
    Parse the input text file ( in the ./Inputs directory) into a python 
    list and build the alphabet and the mapping (indices to chords and chords 
    to indices)
    '''
    
    #User interface to select the file
    
    print('Choose an text input file')
    Tk().withdraw() 
    filename = filedialog.askopenfilename(
            initialdir = './Inputs/',
            filetypes = (('Template files', '*.txt'), ('All files', '*'))
            )
    print('Database : ' + filename)
    print('Parsing input file...')
    fd = open(filename).read()
    chord_seq = fd.split(' ')
    print('Corpus length:', len(chord_seq))
    chars = set(chord_seq)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    alphabet_len = len(char_indices)
    print('Alphabet size : ', alphabet_len)
    return chord_seq, chars, (char_indices, indices_char)


def GetSentences(inputs, sentence_len, step):
    '''Split the input list into size defined sentences. A step can be defined.'''
    sentences = []
    next_chars = []
    for i in range(0, len(inputs) - sentence_len, step):
        sentences.append(inputs[i:i + sentence_len])
        next_chars.append(inputs[i + sentence_len])
    print('number of sequences :', len(sentences))
    return sentences, next_chars

def Encode(sentences, mapping, next_chars = None):
    '''Encode the sentences through time into a 3-dimentionnal boolean array'''
    if next_chars != None:
        nb_sentences = len(sentences)
        alphabet_len = len(mapping[0])
        sentence_len = len(sentences[0])
        x = np.zeros((nb_sentences, sentence_len, alphabet_len), dtype=np.bool)
        y = np.zeros((nb_sentences, alphabet_len), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence[:]):
                x[i, t, mapping[0][char]] = 1
            y[i, mapping[0][next_chars[i]]] = 1
        return x, y
    else :
        nb_sentence = 1
        alphabet_len = len(mapping[0])
        sentence_len = len(sentences)
        x = np.zeros((nb_sentence, sentence_len, alphabet_len), dtype=np.bool)
        for i, char in enumerate(sentences):
            x[0][i, mapping[0][char]] = 1
        return x





     