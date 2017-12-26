#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This module mainly developped by Tristan Carsault contains functions useful to
reduce a chord to a simplified version of itself, or to a chord that shares the
same harmonic function. This allow us to reduce the size of our chord alphabet,
and to process some calculations over simplified chords.

Attributes
----------
QUALITIES : dict of list of int
        This dictionnary links the type of a chord to a binary activation vector
        representing the notes activated for this chord. The first element of the
        activation list represents the root of the chord, second one is one
        semitone higher etc...
a0 : dict of str
        This dictionnary links the type of a chord to a simplified type. The chords
        will be simplified to major, minor or no type chords (a0 reduction)
a1: dict of str
        This dictionnary links the type of a chord to a simplified type. The chords
        will be simplified to major, minor, diminished or no type chords
        (a1 reduction)
a2: dict of str
        This dictionnary links the type of a chord to a simplified type. The chords
        will be simplified to major, minor, diminished, 7, major 7, minor 7 or
        no type chords (a2 reduction)
a3: dict of str
        This dictionnary links the type of a chord to a simplified type. The chords
        will be simplified to major, minor, diminished, 7, major 7, minor 7,
        augmented, sus4 or no type chords (a1 reduction)
gamme: dict of str
        This dictionnary links chords roots to normalized version of themselves
        to avoid dealing with several representations of the same root.
'''

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

#%%
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
    'n':       'N',
    'N':       'N',
    '':        'N'}
#%%
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
    '6':       'maj',
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
#%%
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
    '6':       'maj',
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
#%%
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
    '6':       'maj',
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
#%%
gamme = {
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
    }
#%%%
def reduChord(initChord,
              alpha= 'a1'):
    '''
    Change the input chord to a simplified version of itself through the
    reduction dictionnaries (see reduction dictionnaries above).

    Parameters
    ----------
    initChord: str
        The input chord.
        The chord must be written as follow: 'root:type'.
        The input chord can also be a string containing start or end, as they
        are boundary words in the Choi RealBook dataset.
    alpha: str
        The type of reduction desired. Must be N, a0, a1, a2 or a3

    Returns
    -------
    finalChord: str
        The chord after reduction (shaped like: 'root:type' in lower case).
        If the input chord contains one of the boundary words, it will return
        the same word.

    Notes
    -----
    It is possible to pass 'N' as reduction parameter. In that case, the
    function will only normalize the root and remove additionnal type
    information, separated of the real type by a '/'
    '''
    #Handle key words
    if 'START' in initChord.upper():
        return 'Start'
    elif 'END' in initChord.upper():
        return 'End'
    #Separate additionnal information from the chord if needed
    initChord, bass = (initChord.split('/') if '/' in initChord
                       else (initChord, ''))
    #Separate root from type
    root, qual = initChord.split(':') if ':' in initChord else (initChord, '')
    #Separate additionnal information from root
    root, noChord = root.split('(') if '(' in root else (root, '')
    #Separate additionnal information from type
    qual, bass = qual.split('(') if '(' in qual else (qual, '')
    #Normalize the root
    root = root.lower()
    qual = qual.lower()
    root = gamme[root]
    #If there is no type, assume that type is major
    if qual == '':
        if root == 'N' or noChord != '':
            finalChord = 'N'
        else:
            finalChord = root + ':maj'
    #If there is no root, returns no chord
    elif root == 'N':
        finalChord = 'N'
    #Perform reduction
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
                print('wrong alphabet value')
        if qual == 'N' or qual == 'n':
            finalChord = root + 'N'
        else:
            finalChord = root + ':' + qual

    return finalChord

def ReduSeq(inputs,
            alpha = 'a1'):
    '''
    Performs a reduction over a sequence of chords, using the reduChord function

    Parameters
    ----------
    inputs: list of str
        The chords sequence.
        The chords must be written as follow: 'root:type'.
        The input chords can also be strings containing start or end, as they
        are boundary words in the Choi RealBook dataset.
    alpha: str
        The type of reduction desired. Must be N, a0, a1, a2 or a3

    Returns
    -------
    new_inputs: list of str
        The chord sequence after reduction
        (shaped like: 'root:type' in lower case).
    new_chars: set of str
        A set of all the different chords that can be found in the sequence.
    (char_indices, indices_char): tuple of dict of string
        Two dictionnaries giving an ID number to each different chord in our
        output chord sequence.
        The first dictionnary uses chords as key and ID numbers as values.
        The first dictionnary uses ID numbers as key and chords as values.
    '''
    print('Process reduction ' + alpha + ' ...')
    #Apply the reduChord function to our sequence
    new_inputs = list(map(lambda x: reduChord(x, alpha), inputs))
    new_chars = set(new_inputs)
    #Give ID number to each chord
    char_indices = dict((c, i) for i, c in enumerate(new_chars))
    indices_char = dict((i, c) for i, c in enumerate(new_chars))
    alphabet_len = len(new_chars)
    print('New alphabet size : ', alphabet_len)
    return new_inputs, new_chars, (char_indices, indices_char)
