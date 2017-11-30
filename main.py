# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:29 2017

@author: teo
"""
#from tkinter import filedialog
#from tkinter import *
 
from tkinter import Tk
from tkinter import filedialog
import time
from encoding import *
from model import *
from training import *
from generation import *

def ParseInput():
    """ Parse the input text file into a python array and build the alphabet
    """
    print('Choose an text input file')
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = filedialog.askopenfilename(filetypes = (("Template files", "*.txt"), ("All files", "*"))) # show an "Open" dialog box and return the path to the selected file
    print('Database : ' + filename)
    print('Parsing input file...')
    fd = open(filename).read()
    print('Corpus length:', len(fd))
    chord_seq = fd.split(' ')
    chars = set(chord_seq)
    char_indices = dict((c, i) for i, c in enumerate(chars))    #Mapping : une numéro par mot
    indices_char = dict((i, c) for i, c in enumerate(chars))
    alphabet_len = len(char_indices)
    print('Alphabet size : ', alphabet_len)
    return chord_seq, chars, (char_indices, indices_char)
  
def SaveModel(model, name, pathmodel='./Models/'):
    from keras.models import load_model
    date = time.ctime()
    date = date.replace(' ', '_')
    print('Save model as ' + name + date + '.h5' + '...')
    model.save(pathmodel + name + '_' + date + '.h5')
    
def LoadModel():
    Tk().withdraw()
    filename = filedialog.askopenfilename(filetypes = (("Template files", "*.h5"), ("All files", "*")))
    model = load_model(filename)
    return model



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
        SimpleTrain(model, x, y, batch_size, nb_epoch)
        SaveModel(model, name, pathmodel=('./Models/'))
    elif c1 == 'G':
        model = LoadModel()
        