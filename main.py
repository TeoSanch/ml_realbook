# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:29 2017

@author: teo
"""

from encoding import *
from model_test import *
from training import *
from generation import *
from reduction import *
import os.path
import pickle
import pdb
from chord_distance_octave import *
from distance_tonnetz_alexis import * 

#def main():
if True:
    ''' User interface to launch training, or generation using a trained model'''
    c1 = input('Train or generate? [t/g] ')
    if c1 == 't':
        name = input('Name of the training : ')
        inputs, alphabet, mapping = ParseInput()
        preredutype = input('Type of pre-reduction [N/a0/a1/a2/a3]')
        if preredutype != 'N':
            inputs, alphabet, mapping = ReduSeq(inputs, preredutype)
        ### Tonnetz distance matrix
        #tonnetz_matrix = 
        ###
        #%%
        sentence_len = int(input('Sentence length = '))
        step = int(input('Step = '))
        sentences, next_chars = GetSentences(inputs, sentence_len, step)
        x, y = Encode(sentences, mapping, next_chars)
        #%%
        batch_size = int(input('Batch size = '))
        nb_epoch = int(input('Number of epochs = '))
        loss_number = int(input('Loss function:\n categorical crossentropy: 1\n euclidian: 2\n tonnetz: 3\n'))
        if loss_number == 1:
            loss = 'categorical_crossentropy'
            tf_mapping = 0
        elif loss_number == 2:
            loss = 'euclidian'
            tf_mapping = load_euclid_matrix(preredutype)
        elif loss_number == 3:
            loss = 'tonnetz'
            tf_mapping = load_tonnetz_matrix(preredutype)
            
        model = GetModel(batch_size, sentence_len, len(alphabet),tf_mapping,loss)
        history = RefinedTrain(model, x, y, batch_size, nb_epoch)
        pickle.dump(history, open('%s_history.p' %name, "wb"))
        SaveModel(model, name,'./Models/')
    elif c1 == 'g':
        inputs, alphabet, mapping = ParseInput()
        preredutype = input('Pre-reduction? [a1/a2/a3/N]')
        if preredutype != 'N':
            inputs, alphabet, mapping = ReduSeq(inputs, preredutype)
        tf_mapping = load_tonnetz_matrix(preredutype)
        model = LoadModel(tf_mapping)
        sentence_len = model.get_config()[0]['config']['batch_input_shape'][1]
        loop = True
        while loop:
            name = input('Name of the generated file : ')
            nb_iteration = int(input('Number of generated chords = '))
            seed = input('Seed chords : ')
            determinist = input('Deterministic generation ? [y, n]')
            if determinist == 'y':
                d = True
            elif determinist == 'n':
                d = False
            postredutype = input('Type of post-reduction [N/a0/a1/a2/a3]')
            temperature = float(input('Temperature = '))
            print(seed)
            generation = GenerateSentence(model, inputs, seed, nb_iteration, temperature, sentence_len, mapping, d, redu = postredutype)
            c2 = input('Save output/Generate again/Quit? [s/g/q] ')
            if c2 == 's':
                print('Writing outputs...')
                subdirectory = os.getcwd() + '\\Outputs'
                fd = open(os.path.join(subdirectory, name + '.out'), 'a')
                for item in generation:
                    if 'END' in item.upper():
                        fd.writelines("%s\n" % 'End')
                    if 'START' in item.upper():
                        fd.writelines("%s " % 'Start')
                    else:
                        fd.writelines("%s " % item)
                fd.close()
                print('Written')
            elif c2 == 'g':
                loop = True
            else :
                loop = False

