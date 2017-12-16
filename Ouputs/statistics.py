# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 18:10:31 2017

@author: teo
"""

import pickle
import pdb
import numpy as np
import matplotlib.pyplot as plt

true_proba =pickle.load(open('../Inputs/proba_C.p', "rb"))
name = 'C_2048x128_4periodic_scaled.out'

def GetGenerationProba(length_sentence = 32, filepath='../'):
    """ Parse a text file into a python list and build the alphabet and the mapping (indices to chords and chords to indices)"""
    print('Choose an text output file')
    import pdb
    pdb.set_trace()
    if filepath != '../':
        filename = filepath
    else:
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = filedialog.askopenfilename(initialdir = filepath ,filetypes = ( ("All files", "*"), ("Output files", "*.out"), ("Input files", "*.txt")))
    print('Database : ' + filename)
    print('Parsing output file...')
    fd = open(filename).read()
    if length_sentence>0:
        chord_seq = fd.split('\n')
    else:
        chord_seq = fd.split(' ')
    print('Corpus length:', len(chord_seq))
    chord_seq = list(filter(lambda a: a != '', chord_seq))
    chars = set(chord_seq)
    char_indices = dict((c, i) for i, c in enumerate(chars))    #Mapping : une numéro par mot
    indices_char = dict((i, c) for i, c in enumerate(chars))
    alphabet_len = len(char_indices)
    print('Alphabet size : ', alphabet_len)
    proba = {}
    for field in chars:
        proba[field] = chord_seq[length_sentence:].count(field)/(len(chord_seq)-length_sentence)
    if length_sentence==0:
        proba['End'] = proba.pop('End\n')
    return proba
    
proba_in = GetGenerationProba(0, '../Inputs/C_248x128_2Periodic.txt')
proba_out = GetGenerationProba(32, '../Outputs/C_2048x128_2periodic_random_full.out')

#%% Plotting
N = len(proba_in)
ind = np.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars
plt.figure()
fig, ax = plt.subplots()
rects1 = ax.bar(ind, proba_in.values(), width, color='b')
rects2 = ax.bar(ind + width, proba_out.values(), width, color='orange')

# add some text for labels, title and axes ticks
ax.set_ylabel('Occurence Probability')
ax.set_xticks(ind + width / 2)
keys = list(proba_in.keys())
for i, key in enumerate(proba_in.keys()):
    if ':min' in key:
        keys[i] = key.replace(':min', 'm')
    elif ':maj' in key:
        keys[i] = key.replace(':maj', '')
        
ax.set_xticklabels(keys)

ax.legend((rects1[0], rects2[0]), ('Built inputs', 'Generated outputs'))


#def autolabel(rects):
#    """
#    Attach a text label above each bar displaying its height
#    """
#    for rect in rects:
#        height = rect.get_height()
#        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
#                '%d' % int(height),
#                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)
plt.savefig('proba_results.png', format='png')
plt.show()


