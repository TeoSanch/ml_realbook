# -*- coding: utf-8 -*-

'''
The distances package include functions to calculate distances between two
chords in various ways, save and load them. These distances will be used as loss
functions for our models.

Examples
--------
Examples of those functions can be found in the examples.py script
(project's root)

Notes
-----
These functions are not used when the main script is running. To gain
efficiency, we calculate the results and save them before running the main
script, calling the saved data directly.
'''



import utilities
import pickle
import keras.backend as K
import numpy as np

root_list = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'g#', 'a', 'bb', 'b']
'''list of str:
Used in each function as base for all chord root
'''
#%%
def distance_tonnetz(Chord1, Chord2):
    '''
    The function calculate the distance between two given chords by using
    Neo-Riemmanian Tonnetz transformations

    Parameters
    ----------
    Chord1: str
        The first chord to compare
    Chord2: str
        The second chord to compare

    Each chord must be written as follow: 'root:type'.
    Upper or lower case doesn't affect the code.
    Writing chords root with # or b doesn't affect the code (C# = Db).
    Since the function uses heavily the utilities package, any type not
    defined in chordUtil.py qualities will return an error.

    Returns
    -------
    cost: float
        Distance (cost) between Chord1 and Chord2

    Notes
    -----
    The distance rely on tonnetz transformations L, P and R. A cost is assigned
    to each transformation and the function iterates over the possibilities of
    tonnetz transformations to find suites of transforms that lead to two
    matching chords. The distance is calculaed based on the least expensive
    suite.
    However, since these transformations only apply to major and minor chords,
    it might be necessary to reduce the input chords to one of those two types.
    A cost is added if the reduction is necessary.

    '''
    #use Chords2Vec functions to get the chords roots and types
    root_1, type_1 = utilities.C2V.parse_mir_label(Chord1)
    root_2, type_2 = utilities.C2V.parse_mir_label(Chord2)
    #use Chords2Vec functions to normalize the chords roots
    #(matching the root_list above)
    root_1 = utilities.C2V.normalized_note(root_1)
    root_2 = utilities.C2V.normalized_note(root_2)
    #define the costs of each Tonnetz movement
    L_cost = 1
    R_cost = 1
    P_cost = 1
    #define the cost of a noneType chord (augmented, diminished etc) and a chord
    #with no root
    noneType_cost = 1
    noneRoot_cost = 1
    #define the cost of a reduction
    reduction_cost = 0.2
    suite = ['L']
    costs = []
    matching_suite = []

    #if the two chords are the same, the cost is zero
    if root_1 == root_2 and type_1 == type_2:
        costs.append(0)
    else:
        #Reduce chords to maj, min or noneType
        a,type_1 = utilities.C2V.parse_mir_label(
                utilities.utils.reduChord(Chord1, 'a0'))
        a,type_2 = utilities.C2V.parse_mir_label(
                utilities.utils.reduChord(Chord2, 'a0'))
        #test if the chords matches after reduction
        if root_2 == root_1 and type_2 == type_1:
            matching_suite.append('')
            costs.append(reduction_cost)
        elif (root_1==root_2
              and ((type_2 == 'n' or type_1 == 'n')
                  or (type_2=='' or type_1=='')
                  )
              ):
                matching_suite.append('')
                costs.append(reduction_cost + noneType_cost)
        elif root_1 in ['N', 'n', ' ', ''] or root_2 in ['N', 'n', ' ', '']:
            matching_suite.append('')
            costs.append(noneRoot_cost)

        #if at least one of the chord is a noneType, perform the
        #distance_tonnetz by replacing its type. The function will return the
        #smallest distance between a major or minor chord for the replacing
        #type, added to the noneType_cost
        elif ((type_1 == 'n' or type_1 == '')
        and (type_2 == 'n' or type_2 == '')):
            costs.append(
                    distance_tonnetz(root_1+':maj', root_2+':maj')
                    + noneType_cost
                         )
            costs.append(
                    distance_tonnetz(root_1+':maj', root_2+':min')
                    + noneType_cost
                         )
            costs.append(
                    distance_tonnetz(root_1+':min', root_2+':maj')
                    + noneType_cost
                         )
            costs.append(
                    distance_tonnetz(root_1+':min', root_2+':min')
                    + noneType_cost
                        )
        elif type_1 == 'n' or type_1 == 'n':
            costs.append(
                    distance_tonnetz(root_1+':maj', root_2+':'+type_2)
                    + noneType_cost
                        )
            costs.append(
                    distance_tonnetz(root_1+':min', root_2+':'+type_2)
                    + noneType_cost
                        )
        elif type_2 == 'n' or type_2 == '':
            costs.append(
                    distance_tonnetz(root_1+':'+type_1, root_2+':maj')
                    + noneType_cost
                        )
            costs.append(
                    distance_tonnetz(root_1+':'+type_1, root_2+':min')
                    + noneType_cost
                        )

        #perform the tonnetz_distance for major and minor chords
        else:
            #loop to test all combined suites of 5 tonnetz transformations
            #(5 is enough as it'll render all major and minor chords)
            while len(suite)<6:
                root_transform = root_2
                type_transform = type_2
                #for each element in the tranformation suite,
                #apply the transform
                for i in suite:
                    if i == 'L':
                        root_transform, type_transform = L_transform(
                                                            root_transform,
                                                            type_transform)
                    elif i=='R':
                        root_transform, type_transform = R_transform(
                                                            root_transform,
                                                            type_transform)
                    elif i=='P':
                        root_transform, type_transform = P_transform(
                                                            root_transform,
                                                            type_transform)
                #if the transformed chord matches the first chord,
                #store the suite and its cost
                if root_transform == root_1 and type_transform == type_1:
                    matching_suite.append(list(suite))
                    costs.append(
                            int(cost_count(suite, L_cost, R_cost, P_cost))
                            + reduction_cost
                                )
                #change the suite
                for i in range(len(suite)):
                    if suite[i] == 'L':
                        suite[i] = 'R'
                        break
                    elif suite[i] == 'R':
                        suite[i] = 'P'
                        break
                    elif suite[i] == 'P':
                        if i == len(suite) - 1:
                            suite.append('L')
                            suite[i] = 'L'
                            break
                        else:
                            suite[i] = 'L'
    #Search fo the minimal cost inside all possible suites
    cost = min(costs)

    return cost

#%%
def L_transform(chord_root, chord_type):
    '''
    The function transform the input chord by a L-transform in the Tonnetz
    space. A minor chord becomes a major chord a major third down and a major
    chord becomes a minor chord a major third up.

    Parameters
    ----------
    chord_root: str
        The chord's root (value must be from the root_list variable)
    chord_type: str
        The chord's type. If its value is not 'maj' or 'min', it will not be
        changed by the function.

    Returns
    -------
    chord_root: str
        The chord's root after the L-transform
        (value from the root_list variable)
    chord_type: str
        The chord's type after the L-transform
        ('min', 'maj', or the initial value of chord_type)
    '''
    if chord_type == 'maj':
        n = (root_list.index(chord_root)+4) % 12
        chord_root = root_list[n]
        chord_type = 'min'
    elif chord_type == 'min':
        n = (root_list.index(chord_root)-4) % 12
        chord_root = root_list[n]
        chord_type = 'maj'
    return chord_root, chord_type

#%%
def R_transform(chord_root, chord_type):
    '''
    The function transform the input chord by a R-transform in the Tonnetz
    space. A minor chord becomes a major chord a minor third up and a major
    chord becomes a minor chord a minor third down.

    Parameters
    ----------
    chord_root: str
        The chord's root (value must be from the root_list variable)
    chord_type: str
        The chord's type. If its value is not 'maj' or 'min', it will not be
        changed by the function.

    Returns
    -------
    chord_root: str
        The chord's root after the R-transform
        (value from the root_list variable)
    chord_type: str
        The chord's type after the R-transform
        ('min', 'maj', or the initial value of chord_type)
    '''
    if chord_type == 'maj':
        n = (root_list.index(chord_root)-3) % 12
        chord_root = root_list[n]
        chord_type = 'min'
    elif chord_type == 'min':
        n = (root_list.index(chord_root)+3) % 12
        chord_root = root_list[n]
        chord_type = 'maj'
    return chord_root, chord_type

#%%
def P_transform(chord_root, chord_type):
    '''
    The function transform the input chord by a P-transform in the Tonnetz
    space. A minor chord becomes a major chord and a major chord becomes a minor
    chord. The chord's root stay unchanged.

    Parameters
    ----------
    chord_root: str
        The chord's root.
    chord_type: str
        The chord's type. If its value is not 'maj' or 'min', it will not be
        changed by the function.

    Returns
    -------
    chord_root: str
        The chord's root after the P-transform (no changes).
    chord_type: str
        The chord's type after the P-transform
        ('min', 'maj', or the initial value of chord_type)
    '''
    if chord_type == 'maj':
        chord_type = 'min'
    elif chord_type == 'min':
        chord_type = 'maj'
    return chord_root, chord_type

#%%
def cost_count(suite, L_cost, R_cost, P_cost):
    '''
    The function calculates the cost of a given serie of Tonnetz transformations
    using a specific cost for each transformation by iterating through a list
    representing the serie.

    Parameters
    ----------
    suite: list of char
        The serie of Tonnetz transformation.
    L_cost: float
        Cost of an L-transformation.
    R_cost: float
        Cost of an R-transformation.
    P_cost: float
        Cost of a P-transformation.

    Returns
    -------
    cost: float
        The cost of the Tonnetz transformations serie.
    '''
    cost = 0
    for i in suite:
        if i == 'L':
            cost = cost + L_cost
        elif i=='R':
            cost = cost + R_cost
        elif i=='P':
            cost=cost + P_cost

    return cost

#%%
def tonnetz_matrix(mapping):
    '''
    The function ccalculates a matrix representing the costs of all possible
    pair of chords in a given chord alphabet.

    Parameters
    ----------
    mapping: tuple or list of dict
            (given by the enconding functions from utilities)
        A tuple or list containing on its second part a dictionnary associating
        a number (key) and a chord (value).

    The chords inside the mapping must be formatted like defined in the 
    distance_tonnetz function.

    Returns
    -------
    matrix: list of lists of floats
        A matrix containing for each item (row i, column j) the tonnetz distance
        of the two chords defined by keys i and j in the initial mapping.

    Notes
    -----
    In the Choi RealBook dataset which we are using, there is 'Start' and 'End'
    elements which bounds a given piece of music. Since we cannot calculate a
    tonnetz distance for these elements, we state that the cost between them and
    any other element will be given by the cost_start_end value.
    '''
    #Parse the dictionnary to chords and keys
    dict_alphabet = mapping[1]
    key, alphabet = zip(*dict_alphabet.items())
    key = list(key)
    alphabet = list(alphabet)
    #define the cost of start and end statements
    cost_start_end = 2
    matrix  = [[]]
    #loop over the elements in the dictionnary
    for i in key:
        matrix_line = []
        for j in key:
            if (alphabet[i] in ['_START_','_END_','Start','End']
            or alphabet[j] in ['_START_','_END_','Start','End']):
                if alphabet[i] == alphabet[j]:
                    matrix_line.append(0)
                else:
                    matrix_line.append(cost_start_end)
            else:
                cost = distance_tonnetz(alphabet[i], alphabet[j])
                matrix_line.append(cost)

        matrix.append(matrix_line)

    return matrix

#%%

def save_tonnetz_matrix():
    inputs, alphabet, mapping = utilities.encoding.ParseInput()
    inputs0, alphabet, mapping0 = utilities.utils.reduSeq(inputs, 'a0')
    matrix = tonnetz_matrix(mapping0)
    pickle.dump(matrix, open('Distances/matrix_tonnetz_0.p', 'wb'))

    inputs1, alphabet, mapping1 = utilities.utils.reduSeq(inputs, 'a1')
    matrix = tonnetz_matrix(mapping1)
    pickle.dump(matrix, open('Distances/matrix_tonnetz_1.p', 'wb'))

    inputs2, alphabet, mapping2 = utilities.utils.reduSeq(inputs, 'a2')
    matrix = tonnetz_matrix(mapping2)
    pickle.dump(matrix, open('Distances/matrix_tonnetz_2.p', 'wb'))


    inputs3, alphabet, mapping3 = utilities.utils.reduSeq(inputs, 'a3')
    matrix = tonnetz_matrix(mapping3)
    pickle.dump(matrix, open('Distancees/matrix_tonnetz_3.p', 'wb'))

    inputsN, alphabet, mappingN = utilities.utils.reduSeq(inputs, 'N')
    matrix = tonnetz_matrix(mappingN)
    pickle.dump(matrix, open('matrix_tonnetz_N.p', 'wb'))

def load_tonnetz_matrix(reduction_type):
    if reduction_type == 'N':
        matrix = pickle.load(open('Distances/matrix_tonnetz_N.p', 'rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a3':
        matrix = pickle.load(open('Distances/matrix_tonnetz_3.p', 'rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a2':
        matrix = pickle.load(open('Distances/matrix_tonnetz_2.p', 'rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a1':
        matrix = pickle.load(open('Distances/matrix_tonnetz_1.p', 'rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a0':
        matrix = pickle.load(open('Distances/matrix_tonnetz_0.p', 'rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    return tensor_matrix

#%%

#%%
#dist=0 pour une distance en terme de euclid en note, =1 pour une distance euclidean
# Necessite une réduction avant comparaison car ne peux lire uniquement les accord de type maj/min/dim/aug/maj7/min7/7/dim7/hdim7/minmaj7/maj6/min6/9/maj9/min9/sus2/sus4
def distance_euclid(A_1,
                    A_2):

    #initialisaition
    A_1_red = utilities.utils.reduChord(A_1, 'N')
    A_2_red = utilities.utils.reduChord(A_2, 'N')

    Accord_1_eucl = utilities.C2V.mir_label_to_semitones_vec(A_1_red)
    Accord_2_eucl = utilities.C2V.mir_label_to_semitones_vec(A_2_red)
    N_1 = len(Accord_1_eucl)
    N_2 = len(Accord_2_eucl)
    distance_all = np.zeros(N_1, N_2)
    distance_ligne = np.zeros(N_1)
    distance_eucl = 0

    #Dictionnaire regroupant les distances euclédienne pour des distances >=7 demis tons
    D= { 11 : 1,
        10 : 2,
        9 : 3 ,
        8 : 4,
        7 : 5}

    for k in range(0, N_1):
        for l in range(0, N_2):
            d = Accord_1_eucl[k] - Accord_2_eucl[l]

            #lorsque l'intervalle est inférieur à 6 demis tons
            if abs(d) <= 6:
                distance_all[k][l] = np.pow(d, 2)

            #lorsque l'intervalle est supérieur à 6 demis tons on se sert du dictionnaire D
            if abs(d) > 6:
                distance_all[k][l] = np.pow(D[abs(d)], 2)

        #on concerve uniquement les distances minimum pour la note k_eme de l'accord 1
        distance_ligne[k] = min(distance_all[k])

        #on somme toute les distances minimum
        distance_eucl += distance_ligne[k]


    distance_eucl = np.sqrt(distance_eucl)

    #on renvoi la distance normalisé pour le pire cas

    return distance_eucl / np.sqrt(4*11)


#%%

def euclid_matrix(mapping):
    dict_alphabet = mapping[1]
    key, alphabet = zip(*dict_alphabet.items())
    key = list(key)
    alphabet = list(alphabet)

    cost_start_end = 1

    matrix  = [[]]

    for i in key:
        print(i)
        matrix_line = []
        for j in key:
            if (alphabet[i] in ['_START_','_END_','Start','End']
            or alphabet[j] in ['_START_','_END_','Start','End']):
                if alphabet[i] == alphabet[j]:
                    matrix_line.append(0)
                else:
                    matrix_line.append(cost_start_end)
            else:
                cost = distance(alphabet[i], alphabet[j])
                matrix_line.append(cost)


        matrix.append(matrix_line)

    return matrix

#%%
def save_euclid_matrix():
    inputs, alphabet, mapping = utilities.encoding.ParseInput()
    inputs0, alphabet, mapping0 = utilities.utils.ReduSeq(inputs, 'a0')
    matrix = euclid_matrix(mapping0)
    pickle.dump(matrix, open('Distances/matrix_eucl_0.p','wb'))

    inputs1, alphabet, mapping1 = utilities.utils.ReduSeq(inputs, 'a1')
    matrix = euclid_matrix(mapping1)
    pickle.dump(matrix, open('Distances/matrix_eucl_1.p','wb'))

    inputs2, alphabet, mapping2 = utilities.utils.ReduSeq(inputs, 'a2')
    matrix = euclid_matrix(mapping2)
    pickle.dump(matrix, open('Distances/matrix_eucl_2.p','wb'))


    inputs3, alphabet, mapping3 = utilities.utils.ReduSeq(inputs, 'a3')
    matrix = euclid_matrix(mapping3)
    pickle.dump(matrix, open('Distances/matrix_eucl_3.p','wb'))

    matrix = euclid_matrix(mapping)
    pickle.dump(matrix, open('Distances/matrix_eucl_N.p','wb'))

def load_euclid_matrix(reduction_type):
    if reduction_type == 'N':
        matrix = pickle.load(open('Distances/matrix_eucl_N.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a3':
        matrix = pickle.load(open('Distances/matrix_eucl_3.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a2':
        matrix = pickle.load(open('Distances/matrix_eucl_2.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a1':
        matrix = pickle.load(open('Distances/matrix_eucl_1.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    elif reduction_type == 'a0':
        matrix = pickle.load(open('Distances/matrix_eucl_0.p','rb'))
        matrix.pop(0)
        tensor_matrix = K.constant(matrix)
    return tensor_matrix
