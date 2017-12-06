# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:02 2017

@author: teo
"""
from tkinter import Tk
from tkinter import filedialog
import time
from keras.models import load_model
import matplotlib.pyplot as plt


def SaveModel(model, name, pathmodel='./Models/'):
    print('Save model to ...')
    date = time.ctime()
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    print('Save model as ' + name + '_' + date + '.h5' + '...')
    filepath = pathmodel + name + '_' + date + '.h5'
    model.save(filepath)
    print('Model savec in '+ filepath)
    return model
    
def LoadModel():
    print('Load model...')
    Tk().withdraw()
    filename = filedialog.askopenfilename(initialdir = './Models/', filetypes = (("Template files", "*.h5"), ("All files", "*")))
    model = load_model(filename)
    print(filename + ' loaded')
    return model
    
def SimpleTrain(model, x, y, batch, nb_epochs):
    model.fit(x, y, batch_size = batch, epochs = nb_epochs, verbose = 1)


def RefinedTrain(model, x, y, batch, nb_epochs):
    history = model.fit(x, y , batch_size = batch, epochs = nb_epochs, verbose = 1, validation_split = 0.2).history
    Evaluate(history)
    return history

def Evaluate(history):
    plt.plot(history['acc'])
    plt.plot(history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left');
    
