#krok 1 - wczytanie danych iris
#krok 2 - zmiana danych na krotki

import numpy as np

from sklearn.datasets import load_iris
iris = load_iris()
data = iris.data
target = iris.target

from sklearn.model_selection import train_test_split
data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.3, random_state=42)

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
def learn_tuple_maker(dataset, testset):
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

node_base = learn_tuple_maker(data_train, target_train)

def test_tuple_maker(dataset):
    node_info = []
    for line in dataset:
        if type(line) == np.ndarray:
            krotka = tuple(line)
            node_info = node_info + [krotka]
        else:
            print("failure")

    return node_info

node_test = test_tuple_maker(data_test)
print(node_test)

#---------------------------------------------------------
#Obliczanie zysku informacji

#Gini index
#im wyższa homogeniczność węzła, tym wyższy wskaźniki Gini
#Funkcja obliczania Gini rozbita na 2 funkcje, dla uprostrzenia i zwiększenia czytelnosci
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
#Im większy "zysk informacji" (skuteczność podziału), tym lepszy podział
#IG_Caulculator będzie wykorzystane do wybrania najlepszego podziału
def IG_Calculator(list_parent, list_node_1, list_node_2):

    score_p = G_calculator(list_parent)
    score1 = G_calculator(list_node_1)
    w1 = len(list_node_1)/len(list_parent)
    score2 = G_calculator(list_node_2)
    w2 = len(list_node_2)/len(list_parent)

    #print("w1",w1,"w2",w2,"score1",score1,"score2",score2)

    child = score1 * w1 + score2 * w2
    score = score_p - child

    return score

#---------------------------------------------------
#Szukanie najlepszego podziału

def Treshhold_Generator(lista):
    #this function, provided with a list of objects, divides it into all possible splits - and picks the best one
    #Similar in function to "Attribute selection method" from "Series in Data Management"

    dimension = 0
    max_dimension = 0 #po ilu wymiarach, i w którym, udało się znaleść najbardziej optymalny treshhold
    max_depth = 0 #po ilu obiektach, i w którym, udało się znaleść najbardziej optymalny treshhold
    #max_depth was used in testing, however its not useful outside of it, unlike max_dimention
    the_bear = 0
    the_bull = 0

    object_len = len(lista[1])-1
    depth = 1
    maks = 0
    threshold = 0

    while dimension < object_len:

        unique_list = []
        new_number = 0

        for krotka in lista:

            depth = depth + 1
            new_value = krotka[dimension]
            #we don't check for every single number, but every value. To reduce repetition, we ignore numbers repeats

            #if new_value not in unique_list and len(unique_list) == 0:
                #unique_list = unique_list + [new_value] - LEGACY CODE

            if new_value not in unique_list: #If we find a new value, we test its usefulness as a divider / threshold
                unique_list = unique_list + [new_value]

                lista_1 = []
                lista_2 = []
                for krotka_2 in lista:
                    if krotka_2[dimension] > new_value:
                        lista_1 = lista_1 + [krotka_2]
                    else:
                        lista_2 = lista_2 + [krotka_2]

                new_number = (IG_Calculator(lista, lista_1, lista_2))*(-1)

            else:
                continue

            if new_number > maks: #testing if information gain from the new divider is bigger then previous max
                threshold = new_value
                maks = new_number
                max_dimension = dimension
                max_depth = depth #additional information, used in the past for testing

                the_bear = lista_2
                the_bull = lista_1
                #print("new max number is", new_number)
            else:
                continue

        depth = 0
        dimension = dimension + 1
        #print("dimension =", dimension)

    #print("MAX = ", maks) #LEGACY CODE - testing
    #print("max dimension =", max_dimension)
    #print("max depth =", max_depth)
    #print(len(the_bear)) #nawiązanie do gry Fallout New Vegas
    #print(len(the_bull))
    #print("")
    return threshold, max_dimension, the_bear, the_bull

def Flower_Generator(lista,x):
    #This tests the node and assigns a type
    #If all objects are from the same class - its a leaf
    #If not all objects are from the same class, but we reached the max depth - its a ground leaf
    #If neither conditions are met, its a "node", meaning it can and will be divided further

    status = 0
    engels = [] #unqiue_values

    for element in lista:

        if element[-1] in engels:
            continue
        else:
            engels = engels + [element[-1]]

    if len(engels) == 1:
        status = engels[0]
        return "leaf", status
    elif len(engels) != 1  and x == 8:
        status = engels[0] #ROZWIĄZANIE TYMCZASOWE
        return "ground leaf", status
    else:
        return "node", status

def tree_making(lista_matka,x): #PODZIAŁ NA DANYCH UCZĄCYCH - tworzy algorytm dla danych testowych
    #funckja rekurencyjna, która dzieli węzeł na dwie, po czym stosuje siebie samą, jeżeli węzły-dzieci nie są liścmi
    #funckja zapisuje rezultaty na 2 sposoby
    #1 - pisemną reprezentację drzewa (node1, node2)
    #2 - instrukcję jak potwórzyc podział, tym razem na danych testowych, nie uczących się (bez informacji odn. klas)

    treshhold, dimention, node1, node2 = Treshhold_Generator(lista_matka)
    x = x + 1

    # We check if child 1 and child 2 are nodes or leafes / ground leafes
    n1_status, n1_class = Flower_Generator(node1, x)
    n2_status, n2_class = Flower_Generator(node2, x)
    #print("Node1, (", n1_status ,")")
    #print("Node2, (", n2_status ,")")
    #print(" ")

    save = x

    if n1_status == "node" and x != 8:
        # if left child note can be subdivided earlier, we do, and we receive information how it will happen - procedure
        procedura, new_node_11, new_node_12 = tree_making(node1,x)
        node1 = [new_node_11] + [new_node_12]
        node1_info = procedura

    else: #if left child node is a leaf or ground leaf, we pass it on upwards with information about itself
        node1_info = (n1_status, int(n1_class), len(node1))

    if n2_status == "node" and x != 8:
        #if right child note can be subdivided earlier, we do, and we receive information how it will happen - procedure
        procedura, new_node_21, new_node_22 = tree_making(node2,x)
        node2 = [new_node_21] + [new_node_22]
        node2_info = procedura

    else: #if right child node is a leaf or ground leaf, we pass it on upwards with information about itself
        node2_info = (n2_status, int(n2_class), len(node2))

    procedura = ("node", (float(treshhold), dimention), node1_info, node2_info)
    #making of "procedure" is self-referential, allowing for easier readability both for the user and algorithm

    return procedura, node1, node2

procedura, node1, node2 = tree_making(node_base,0)
results = [node1] + [node2]

#a = node1[1]
#print(a)
#a = a[0]
#print(a)

print(procedura)

def treshhold_user(lista, value, wymiar):
    #based on treshhold calculator - but reverse
    #Instead of looking for the best split, it uses value and dimention provided to divide the list provided

    lista_1 = []
    lista_2 = []

    for krotka in lista:
        if krotka[wymiar] > value:
            lista_1 = lista_1 + [krotka]
        else:
            lista_2 = lista_2 + [krotka]

    #print("lista_1 = ", len(lista_1))
    #print("lista_2 = ", len(lista_2)) # - LEGACY CODE - used for testing

    return lista_2, lista_1

def check(dictionary): #function used for printing the state of dictionary - what keys there are and their assigned values
    print("dict check")
    for key in dictionary:
        print(key, " = ", dictionary[key])
    print("")

def reading_procedure(procedure, data, x): #UŻYWA ALGORYTMU BY KLASYFIKOWAĆ DANE TESTOWE

    dictionary = {}
    lista_1 = []
    lista_2 = []

    if procedure[0] == 'node':
        threshold = procedure[1]
        value = threshold[0]
        wymiar = threshold[1]
        lista_1, lista_2 = treshhold_user(data, value, wymiar)

        node_left = procedure[2]
        node_right = procedure[3]

        if node_left[0] == 'node':
            x = x + 1
            new_dictionary = reading_procedure(node_left, lista_1, x)
            for key in new_dictionary:
                dictionary[key] = new_dictionary[key]
        else:
            klasa = node_left[1]
            #print("klasa:", klasa, "-", len(lista_1))
            dictionary[klasa] = len(lista_1)

        if node_right[0] == 'node':
            x = x + 1
            new_dictionary = reading_procedure(node_right, lista_2, x)
            for key in new_dictionary:
                if key in dictionary:
                    dictionary[key] = dictionary[key] + new_dictionary[key]
                else:
                    dictionary[key] = new_dictionary[key]
        else:
            klasa = node_right[1]
            #print(klasa, "-", len(lista_2))
            if klasa in dictionary:
                dictionary[klasa] = dictionary[klasa] + len(lista_2)
            else:
                dictionary[klasa] = len(lista_2)

    check(dictionary)
    return dictionary


print("testing \n")
procedura, node1, node2 = tree_making(node_base,0)
dictionary = reading_procedure(procedura, node_test, 0)
print("\ndictionary:")
for key in dictionary:
    print(key, " : ", dictionary[key])

