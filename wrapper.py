# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:10:03 2017

@author: teo
"""
from distance_tonnetz_alexis import *
from Distances import *
import numpy as np
import tensorflow as tf
import pdb
import keras.backend as K

    
    


def wrap_tonnetz(tf_mapping):  
    def tonnetz(y_true, y_pred):

        mat1 = K.dot(y_pred, tf_mapping)
        vect = K.transpose(y_true)
        loss = K.dot(mat1,vect)
        
        return loss

    return tonnetz