# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 17:01:02 2017

@author: teo
"""
    
def SimpleTrain(model, x, y, batch, nb_epochs):
    filepath = './checkpoints/'
    #checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    model.fit(x, y, batch_size = batch, epochs = nb_epochs, verbose = 1)  #callbacks = [checkpoint])
