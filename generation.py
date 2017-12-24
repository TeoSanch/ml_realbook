#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 01:14:26 2017

@author: teo
"""

import random
from encoding import *
import pdb
from reduction import *

def GenerateSentence(model, inputs, seed, nb_iteration, temperature, sentence_len, mapping, determinism = True, redu = 'N'):
    '''Generate a number of word starting from a seed and a trained model
    Inputs : 
        model : the trained model
        inputs : the word-input list
        seed : a word-sequence starting point
        nb_iteration : number of word generated
        temperature : alpha coefficient, resamble the probability of the predicted word (temperature>1 --> diversity)
        sentence_len : length of the sentences
        mapping : mapping indices to chords and chords to indices
        determinist : Boolean value deciding if the seed is determinist or not
        '''
    generated = []
    seed_sentence = GetSeed(seed, inputs, sentence_len, determinism)
    generated = seed_sentence
    sentence = seed_sentence
    for i in range(nb_iteration):
        prediction = GenerateWord(sentence, model, temperature, mapping, redu = redu)
        sentence.append(prediction)
        sentence = sentence[1:]
        generated.append(prediction)
    return generated

def GenerateWord(sentence, model, temperature, mapping, redu = 'N'):
    ''' Generate a single word'''
    x = Encode(sentence, mapping)
    prediction = model.predict(x, verbose=0)[0]
    next_index = Sample(prediction, temperature)
    next_char = mapping[1][next_index]
    if redu != 'N':
        next_char = ReduChord(next_char, redu)
        print(next_char)
        return next_char
    else:
        print(next_char)
        return next_char

        
def GetSeed(seed, inputs, sentence_len, determinism = True):
    ''' Starting from a sequence of chords, detect if the sequence is in the inputs and take a sequence adapted to the sentence length defined before
    determinist : if True, it takes the first sequence found, otherwise, it takes randomly one of the occurrence in the inputs'''
    seed = seed.split(' ')
    if len(seed) < sentence_len:
        indexes = []
        for i in range(len(inputs)):
            if inputs[i:i+len(seed)] == seed:
                indexes.append((i, i+len(seed)))
        if len(indexes) == 0:
            print('Invalide Seed')
        if determinism == True:
            index = indexes[0]
        else :
            index = random.choice(indexes)
        seed_out = inputs[index[0]:index[0]+sentence_len]
        return seed_out
    else: 
        return seed

def Sample(predicted_probas, temperature=1.0):
    '''Resample the probabilities of the next generated chord
    If temperature > 1, increase the diversity'''
    tmp = np.log(predicted_probas) / temperature
    tmp = np.exp(tmp)/np.sum(np.exp(tmp))
    choices = range(len(tmp))
    return np.random.choice(choices, p=tmp)

    
    
