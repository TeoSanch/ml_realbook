# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:10:03 2017

@author: teo
"""
from distance_tonnetz_alexis import *
from chord_distance_octave import *
import numpy as np
import tensorflow as tf
import pdb
import keras.backend as K

def test_py(x1, x2):
    pdb.set_trace()
    y = 1
    return y

def tensor2chord(y, tf_mapping):
    sess = tf.Session()
    dim = tf.constant(1, tf.int64)
    index = tf.argmax(y, dim)
    
    #octave*
    #index = tf.reduce_max(tf.argmax(y,dim))
    #
#     = tf.contrib.lookup.index_to_string_table_from_tensor(tf_mapping, default_value="N")
    """
    value = tf_mapping.lookup(index)
    tf.tables_initializer().run(session = sess)
    try:
        chord = value.eval(session = sess)
    except:
        chord = "C:min"
    return chord
    """
    return index
    

    
#def wrap_euclidian(mapping):
#    def euclidian(y_true, y_pred):
#        chord_true = onehot2chord(y_true, mapping)
#        chord_pred = onehot2chord(y_pred, mapping)
#        return distance(chord_true, chord_pred, 1)
#    return euclidian  
'''
def caca(y_true,y_pred):
    return K.mean(K.square(y_true-y_pred), axis = -1)
'''
def wrap_tonnetz(tf_mapping):  
    def tonnetz(y_true, y_pred):
        import pdb
        #pdb.set_trace()
        mat1 = K.dot(y_pred, tf_mapping)
        vect = K.transpose(y_true)
        loss = K.dot(mat1,vect)
        '''
        diag =tf.ones([alpha_len],tf.float32)
        matrix = tf.diag(diag)
        mat1 = tf.matmul(y_pred,matrix)
        loss= tf.matmul(mat1,y_true, transpose_a = False, transpose_b=True)
        '''
        # loss = K.mean(K.square(y_true - y_pred), axis = -1)
        #sess = tf.Session()
        #y_true_len = K.sum(K.ones_like(y_true))
        #y_pred_len = K.sum(K.ones_like(y_pred))
        #db.set_trace()
        """
        chord_pred = tensor2chord(y_pred, tf_mapping)
        chord_true = tensor2chord(y_true, tf_mapping)
        
        return tf.mean(distance_tonnetz(chord_true, chord_pred), axis = -1)
        """
        #index_true = tensor2chord(y_true, tf_mapping)
        #index_pred = tensor2chord(y_pred, tf_mapping)
        
        #true = tf.placeholder(tf.float32)
        #pred = tf.placeholder(tf.float32)
        
        #loss1 = tf.py_func(test_py, [y_true,y_pred], tf.float32)
        #loss = sess.run(loss1)
        #loss = y_pred
        
        return loss

    return tonnetz