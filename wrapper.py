# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 00:10:03 2017

@author: teo
"""
from distance_tonnetz_alexis import *
from chord_distance_octave import *
import numpy as np
import tensorflow as tf

def tensor2chord(y, tf_mapping):
    sess = tf.Session()
    dim = tf.constant(1, tf.int64)
    index = tf.argmax(y, dim)
    #octave*
    #index = tf.reduce_max(tf.argmax(y,dim))
    #
#     = tf.contrib.lookup.index_to_string_table_from_tensor(tf_mapping, default_value="N")
    value = tf_mapping.lookup(index)
    tf.tables_initializer().run(session = sess)
    try:
        chord = value.eval(session = sess)
    except:
        chord = "C:min"
    return chord

    
#def wrap_euclidian(mapping):
#    def euclidian(y_true, y_pred):
#        chord_true = onehot2chord(y_true, mapping)
#        chord_pred = onehot2chord(y_pred, mapping)
#        return distance(chord_true, chord_pred, 1)
#    return euclidian  

def wrap_tonnetz(tf_mapping):  
    def tonnetz(y_true, y_pred):
        import pdb
        #db.set_trace()
        chord_pred = tensor2chord(y_pred, tf_mapping)
        chord_true = tensor2chord(y_true, tf_mapping)
        
        return tf.constant(distance_tonnetz(chord_true, chord_pred), tf.float32)
    return tonnetz