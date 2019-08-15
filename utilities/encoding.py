#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This module contains functions to read chords from files and encode them
before passing them to our keras model.

Example
-------
Examples of these functions can be found in the examples.py file at the root
of the project
'''

import numpy as np
from tkinter import Tk
from tkinter import filedialog


#%%
def ParseInput():
    '''
    Parse an input text file into a python list and build the alphabet and the
    mapping corresponding.

    Parameters
    ----------
    None: the file is retrieved via a GUI inside the function.

    Returns
    -------
    chord_seq: list of string
        A list containing all the chords in the chosen file.
        Chords must be separated by a space.
    chars: set of strings
        A set containing all the different chords (alphabet) in the chosen file.
    (char_indices, indices_char): tuple of dictionnaries of strings
        Two dictionnaries giving an ID number to each different chord in our
        output chord list.
        The first dictionnary uses chords as key and ID numbers as values.
        The first dictionnary uses ID numbers as key and chords as values.
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
    #read the file
    fd = open(filename).read()
    chord_seq = fd.split(' ')
    print('Corpus length:', len(chord_seq))
    #build the alphabet and dictionnaries
    chars = set(chord_seq)
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))
    alphabet_len = len(char_indices)
    print('Alphabet size : ', alphabet_len)
    return chord_seq, chars, (char_indices, indices_char)

#%%
def GetSentences(inputs,
                 sentence_len,
                 step):
    '''
    Split the input list into size defined sentences with a given step

    Parameters
    ----------
    inputs: list of strings
        A list of chords.
    sentence_len: int
        The size of the output sentences.
    step: int
        The step used to go from one sentence to another

    Returns
    -------
    sentences: list of lists of strings
        A list of the sentences created from the input
    next_chars: list of strings
        A list of the chords coming just after the corresponding sentences
        (used to train our keras model)
    '''
    sentences = []
    next_chars = []
    for i in range(0, len(inputs) - sentence_len, step):
        sentences.append(inputs[i:i + sentence_len])
        next_chars.append(inputs[i + sentence_len])
    print('number of sequences :', len(sentences))
    return sentences, next_chars

#%%
def Encode(sentences,
           mapping,
           next_chars = None):
    '''
    Encode the sentences through time into a 3-dimentionnal boolean array. 
    For each sentence, the array will contains activation vectors corresponding 
    to the given alphabet
    
    Parameters
    ----------
    sentences: list of lists of strings
        The sentences of chords to encode
    mapping: tuple of dictionnaries of strings
        Two dictionnaries giving an ID number to each different chord in our
        output chord list.
        The first dictionnary uses chords as key and ID numbers as values.
        The first dictionnary uses ID numbers as key and chords as values.
    next_chars: list of strings
        A list of chords coming right after the corresponding sentence
        (used to train our model)
    
    Returns
    -------
    x: 3D array of booleans 
    (shape: 
    number of sentences, 
    number of chords in the alphabet, 
    number of chords in a sentence)
        Activation array, representing the activation of chords for each 
        sentence
    y: 2D array of booleans (optionnal)
    (shape:
    number of sentences,
    number of chords in the alphabet)
        Activation array, representing the next chord for each sentence.
        
    '''
    #Code two arrays if next_chars is given
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
    #Only code x otherwise
    else :
        nb_sentence = 1
        alphabet_len = len(mapping[0])
        sentence_len = len(sentences)
        x = np.zeros((nb_sentence, sentence_len, alphabet_len), dtype=np.bool)
        for i, char in enumerate(sentences):
            x[0][i, mapping[0][char]] = 1
        return x
