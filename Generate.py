#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 01:14:26 2017

@author: teo
"""
import misc
from keras.callbacks import ModelCheckpoint

def Generate(model, x, y, itemax):
    
    for i in range (1, itemax):
        print()
        print(i, ' : ')
        with open(('result_iter_%02d.txt' % i), 'w') as f_write:
            
            model.fit(x, y , batch_size = 512, nb_epoch=1)
            start_index = random.randint
        
        
def SimpleTrain(model, x, y, batch, nb_epochs):
    from keras.models import load_model
    import time
    filepath = './checkpoints/'
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    model.fit(x, y, batch_size = batch, epochs = nb_epochs, verbose = 1, callbacks = [checkpoint])
    date = time.ctime()
    date = date.replace(' ', '_')
    model.save('model_' + date + '.h5')