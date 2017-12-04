# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:29 2017

@author: teo
"""

from encoding import *
from model import *
from training import *
from generation import *


def main():
    c1 = input('Train or generate? [T/G] ')
    if c1 == 'T':
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
    elif c1 == 'G':
        model = LoadModel()
        sentence_len = model.get_config()[0]['config']['batch_input_shape'][1]
        name = input('Name of the generated sequence : ')
        inputs, alphabet, mapping = ParseInput()
        seed = input('Seed chords : ')
        nb_iteration = int(input('Number of generated chords = '))
        temperature = float(input('Temperature = '))
        generation = GenerateSentence(model, inputs, seed, nb_iteration, temperature, sentence_len, mapping)
        print(generation)
        