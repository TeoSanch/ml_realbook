# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:29 2017

@author: teo
"""

from encoding import *
from model import *
from training import *
from generation import *
import os.path

def main():
    c1 = input('Train or generate? [t/g] ')
    if c1 == 't':
        name = input('Name of the training : ')
        inputs, alphabet, mapping = ParseInput()
        sentence_len = int(input('Sentence length = '))
        step = int(input('Step = '))
        sentences, next_chars = GetSentences(inputs, sentence_len, step)
        x, y = Encode(sentences, next_chars, mapping)
        batch_size = int(input('Batch size = '))
        nb_epoch = int(input('Number of epochs = '))
        model = GetModel(batch_size, sentence_len, len(alphabet))
        history = RefinedTrain(model, x, y, batch_size, nb_epoch)
        SaveModel(model, name,'./Models/')
    elif c1 == 'g':
        name = input('Name of the generated file : ')
        model = LoadModel()
        sentence_len = model.get_config()[0]['config']['batch_input_shape'][1]
        inputs, alphabet, mapping = ParseInput()
        loop = True
        while loop:
            nb_iteration = int(input('Number of generated chords = '))
            seed = input('Seed chords : ')
            determinist = input('Deterministic generation ? [y, n]')
            if determinist == 'y':
                d = True
            elif determinist == 'n':
                d = False
            temperature = float(input('Temperature = '))
            generation = GenerateSentence(model, inputs, seed, nb_iteration, temperature, sentence_len, mapping, d)
            print(generation)
            c2 = input('Save output/Generate again/Quit? [s/g/q] ')
            if c2 == 's':
                print('Writing outputs...')
                subdirectory = os.getcwd() + '\\Outputs'
                fd = open(os.path.join(subdirectory, name + '.out'), 'a')
                fd.writelines(["%s\n" % item  for item in generation])
                fd.close()
                print('Written')
            elif c2 == 'g':
                loop = True
            else :
                loop = False

