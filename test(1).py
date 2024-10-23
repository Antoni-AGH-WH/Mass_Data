#krok 1 - wczytanie danych iris
#krok 2 - zmiana danych na krotki

import numpy as np
import random
import pandas as pd

from sklearn.datasets import load_iris
iris = load_iris()

data = iris.data
target = iris.target

#---------------------------------------------------------
#Podstawowy kod

def unique_numbers(list): #https://www.geeksforgeeks.org/python-get-unique-values-list/ - źródło

    class_dictionary = {}
    total = 0

    for x in list:
        key = int(x)
        if x in class_dictionary:
            class_dictionary[key] = class_dictionary[key]+1
            total = total + 1
        else:
            class_dictionary[key] = 1
            total = total + 1

    return class_dictionary, total

#---------------------------------------------------------
#Stworzenie danych testowych
def tuple_maker(dataset, testset):
    node_info = []
    x = -1
    for line in dataset:

        x = x + 1
        if type(line) == np.ndarray:
            class_number = testset[x]
            krotka = tuple(line) + (class_number,)
            node_info = node_info + [krotka]
        else:
            print("failure")

    return node_info

node_base = tuple_maker(data, target)


#---------------------------------------------------------
#Obliczanie zysku informacji

#Gini index
def G_calculator(list_of_elements):

    list_of_classes = []
    G_score = 0

    for element in list_of_elements:
        list_of_classes = list_of_classes + [element[-1]]

    class_data, total = unique_numbers(list_of_classes)

    for element in class_data:
        perchance = pow((class_data[element]/total),2)
        G_score = G_score + perchance

    return G_score

#Information Gain Calculator
def IG_Calculator(list_parent, list_node_1, list_node_2):

    score_p = G_calculator(list_parent)
    score1 = G_calculator(list_node_1)
    w1 = len(list_node_1)/len(list_parent)
    score2 = G_calculator(list_node_2)
    w2 = len(list_node_2)/len(list_parent)

    #print("w1",w1,"w2",w2,"score1",score1,"score2",score2)

    child = score1 * w1 + score2 *w2
    score = score_p - child

    return score

#---------------------------------------------------
#Szukanie najlepszego podziału

def Treshhold_Generator(lista):
    #this function, provided with a list of objects, divides it into all possible splits - and picks the best one

    dimension = 0
    max_dimension = 0
    max_depth = 0
    the_bear = 0
    the_bull = 0

    object_len = len(lista[1])-1
    depth = 1
    maks = 0

    while dimension < object_len:

        unique_list = []
        new_number = 0
        for krotka in lista:

            depth = depth + 1
            new_value = krotka[dimension]
            if new_value not in unique_list and len(unique_list) == 0:
                unique_list = unique_list + [new_value]

            elif new_value not in unique_list and len(unique_list) > 0:
                unique_list = unique_list + [new_value]

                lista_1 = []
                lista_2 = []
                for krotka_2 in lista:
                    if krotka_2[dimension] > new_value:
                        lista_1 = lista_1 + [krotka_2]
                    else:
                        lista_2 = lista_2 + [krotka_2]

                new_number = (IG_Calculator(lista, lista_1, lista_2))*(-1)
                #print("new_number",new_number)
            else:
                continue

            if new_number > maks:
                maks = new_number
                max_dimension = dimension
                max_depth = depth

                the_bear = lista_2
                the_bull = lista_1
                print("new max number is", new_number)
            else:
                continue

        depth = 0
        dimension = dimension + 1
        print("dimension =", dimension)

    print("MAX = ", maks)
    print("max dimension =", max_dimension)
    print("max depth =", max_depth)
    return the_bear, the_bull


#def Node_Divider_Generator():



node1, node2 = Treshhold_Generator(node_base)

