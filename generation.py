#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 01:14:26 2017

@author: teo
"""

import random
from encoding import *

def GenerateSentence(model, inputs, seed, nb_iteration, temperature, sentence_len, mapping, determinism = True):
    generated = []
    seed_sentence = GetSeed(seed, inputs, sentence_len, determinism)
    generated = seed_sentence
    sentence = seed_sentence
    for i in range(nb_iteration):
        prediction = GenerateWord(sentence, model, temperature, mapping)
        sentence.append(prediction)
        sentence = sentence[1:]
        generated.append(prediction)
    return generated

def GenerateWord(sentence, model, temperature, mapping):
    x = Encode(sentence, mapping)
    prediction = model.predict(x, verbose=0)[0]
    next_index = Sample(prediction, temperature)
    next_char = mapping[1][next_index]
    return next_char
        
def GetSeed(seed, inputs, sentence_len, determinism = True):
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
    tmp = np.log(predicted_probas) / temperature
    tmp = np.exp(tmp)/np.sum(np.exp(tmp))
    choices = range(len(tmp))
    return np.random.choice(choices, p=tmp)

    
    
