# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:02 2017

@author: teo
"""
from tkinter import Tk
from tkinter import filedialog
import time

def SaveModel(model, name, pathmodel='./Models/'):
    date = time.ctime()
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    print('Save model as ' + name + '_' + date + '.h5' + '...')
    filepath = pathmodel + name + '_' + date + '.h5'
    model.save(filepath)
    return model
    
def LoadModel():
    Tk().withdraw()
    filename = filedialog.askopenfilename(filetypes = (("Template files", "*.h5"), ("All files", "*")))
    model = load_model(filename)
    return model
    
def SimpleTrain(model, x, y, batch, nb_epochs):
    filepath = './checkpoints/'
    #checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    model.fit(x, y, batch_size = batch, epochs = nb_epochs, verbose = 1)  #callbacks = [checkpoint])
