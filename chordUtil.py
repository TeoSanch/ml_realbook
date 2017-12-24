#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 12:38:02 2017

@author: tristan
"""

"""----------------------------------------------------------------------
-- Tristan Metadata and conv
----------------------------------------------------------------------"""
#%%

def convMetaLBC(audioSet,transformOptions):
    #convInput = []
    listBeatChord = [];
    hopSizeS = (transformOptions["hopSize"] / transformOptions["resampleTo"]);
    hopSizeMs = hopSizeS * 1000;
    nbData = 0;
    curData = 0;
    nbBands = len(audioSet.data[1])
    audioSet.metadata['listBeatChord'] = {};
#Count the number of frames
    for k in range(len(audioSet.data)):
        nbData = nbData + len(audioSet.data[k][0]) - transformOptions["contextWindows"] + 1
#Pre-allocate the windowed dataset
        #local finalData = options.modelType == 'ladder' and torch.Tensor(nbData, nbBands * options.contextWindows) or torch.Tensor(nbData, nbBands, options.contextWindows);
        #finalData = np.array(nbData, nbBands, options.contextWindows)
    finalData = {}
    #finalLabels = {};
#-- Parse the whole set of windows
    for k in range(len(audioSet.data)):
        #print(k)
        maxFrame = len(audioSet.data[k][0])
        for numFrame in range(maxFrame - transformOptions["contextWindows"]  + 1):
            nbrAcc = 0
            while numFrame + (transformOptions["contextWindows"]  / 2) + 0.5 > (audioSet.metadata['chord'][k][0]['timeEnd'][nbrAcc] / hopSizeS) and nbrAcc+1 < len(audioSet.metadata['chord'][k][0]['timeStart']):
                nbrAcc = nbrAcc+1;
            curData = curData + 1;
            #finalLabels[curData] = list(audioSet.metadata['chord'][k][0]['labels'][nbrAcc]);
            finalData[curData] = audioSet.data[k][:, range(numFrame, numFrame + transformOptions["contextWindows"])];
            finalData[curData] = (finalData[curData] - finalData[curData].mean()) / finalData[curData].max();
            listBeatChord.append(audioSet.metadata['chord'][k][0]['labels'][nbrAcc]);
#audioSet.data[k] = convInputTens;
        audioSet.metadata['listBeatChord'][k] = listBeatChord;
        listBeatChord = []
    audioSet.data = finalData;
    #audioSet.metadata['listBeatChord'] = finalLabels
    return audioSet

QUALITIES = {
    #           1     2     3     4  5     6     7
    'maj':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    'min':     [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    'aug':     [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    'dim':     [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'sus4':    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
    'sus2':    [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    '7':       [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'maj7':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min7':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    'minmaj7': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    'maj6':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
    'min6':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    'dim7':    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    'hdim7':   [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    'maj9':    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min9':    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '9':       [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'b9':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '#9':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'min11':   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '11':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '#11':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'maj13':   [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    'min13':   [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
    '13':      [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    'b13':     [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    '1':       [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    '5':       [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    '': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}


a0 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'N',
    'dim':     'N',
    'sus4':    'N',
    'sus2':    'N',
    'sus':     'N',
    '7':       'maj',
    'maj7':    'maj',
    'min7':    'min',
    'minmaj7': 'min',
    'maj6':    'maj',
    '6':       'maj',
    'min6':    'min',
    'dim7':    'N',
    'hdim7':   'N',
    'hdim':    'N',
    'maj9':    'maj',
    'min9':    'min',
    '9':       'maj',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'maj',
    '1':       'N',
    '5':       'N',
    '': 'N'}

a1 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'N',
    'dim':     'dim',
    'sus4':    'N',
    'sus2':    'N',
    '7':       'maj',
    'maj7':    'maj',
    'min7':    'min',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj',
    'min9':    'min',
    '9':       'maj',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'maj',
    '1':       'N',
    '5':       'N',
    '': 'N'}

a2 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'N',
    'dim':     'dim',
    'sus4':    'N',
    'sus2':    'N',
    '7':       '7',
    'maj7':    'maj7',
    'min7':    'min7',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim7',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj7',
    'min9':    'min7',
    '9':       '7',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'maj',
    '1':       'N',
    '5':       'N',
    '': 'N'}

a3 = {
    'maj':     'maj',
    'min':     'min',
    'aug':     'aug',
    'dim':     'dim',
    'sus4':    'sus4',
    'sus2':    'sus4',
    '7':       '7',
    'maj7':    'maj7',
    'min7':    'min7',
    'minmaj7': 'min',
    'maj6':    'maj',
    'min6':    'min',
    'dim7':    'dim7',
    'hdim7':   'dim',
    'hdim':    'dim',
    'maj9':    'maj7',
    'min9':    'min7',
    '9':       '7',
    'b9':      'maj',
    '#9':      'maj',
    'min11':   'min',
    '11':      'maj',
    '#11':     'maj',
    'maj13':   'maj',
    'min13':   'min',
    '13':      'maj',
    'b13':     'maj',
    '1':       'N',
    '5':       'N',
    '': 'N'}

gamme = {
### modifié par Octave
    'ab':   'g#',
    'a':    'a',
    'a#':   'a#',
    'bb':   'a#',
    'b':    'b',
    'cb':   'b',
    'c':    'c',
    'c#':   'c#',
    'db':   'd#',
    'd':    'd',
    'd#':   'd#',
    'eb':   'd#',
    'e':    'e',
    'e#':   'e#',
    'fb':   'e#',
    'f':    'f',
    'f#':   'f#',
    'gb':   'f#',
    'g':    'g',
    'g#':   'g#',
    'n' :   'n',
    '' :    'n'
###
    }

def reduChord(initChord, alpha= 'a1'):

    #if initChord == "":
        #print("buuug")
    initChord, bass = initChord.split("/") if "/" in initChord else (initChord, "")
    root, qual = initChord.split(":") if ":" in initChord else (initChord, "")
    root, noChord = root.split("(") if "(" in root else (root, "")
    qual, bass = qual.split("(") if "(" in qual else (qual, "")
    if "(" in qual:
        qual = ""

#### modifié par Octave
    root = root.lower()
###

    root = gamme[root]

    if qual == "":
        if root == "N" or noChord != "":
            finalChord = "N"
        else:
            finalChord = root + ':maj'

    elif root == "N":
        finalChord = "N"

    else:
        if alpha == 'a1':
                qual = a1[qual]
        elif alpha == 'a0':
                qual = a0[qual]
        elif alpha == 'a2':
                qual = a2[qual]
        elif alpha == 'a3':
                qual = a3[qual]
        elif alpha == 'N':
            qual = qual
        else:
                print("wrong alphabet value")
        if qual == "N":
            finalChord = "N"
        else:
            finalChord = root + ':' + qual

    return finalChord
