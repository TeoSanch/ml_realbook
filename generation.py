#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 01:14:26 2017

@author: teo
"""


def Generate(modelpath, inputs, sentences, mapping, char, seed, nb_prediction = 48):
    model = load_model(modelpath)
    seed = seed.split(' ')
    start_index = map(mapping[0], seed)
    

    maxlen = len(sentences[0])
    num_chars = len(mapping[0])
    for i in range(nb_prediction):
        x = np.zeros((1, maxlen, num_chars))
        for t, char in enumerate(mapping[0][char]):
            preds = model.predict(x, verbose = 0)[0]
        
def ChangeTemperature(vector, temperature=1.0):
    tmp = np.log(vector) / temperature
    out_vector = np.exp(tmp) / sum(np.exp(tmp))
    return np.argmax(np.random.multinomial(1, out_vector, 1))   #???


    
    
