#Opis:
#Algorytm z Sklearn, do testów

from sklearn.datasets import load_iris
from sklearn import tree
iris = load_iris()
X, y = iris.data, iris.target

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, y_train)
tfl = clf.predict(X_test)

tree.plot_tree(clf)

print(tfl)
print(y_test)
x = 0
correct = 0
guesses = 0

for element in tfl:
    guesses = guesses + 1
    if y_test[x] == element:
        correct = correct + 1
    x = x + 1

score = correct / guesses * 100
print("Score =", int(score), "%")

dictionary = {}
for element in y_test:
    if element in dictionary:
        dictionary[element] = dictionary[element] + 1
    else:
        dictionary[element] = 1

sorted_dict = dict(sorted(dictionary.items()))
for key in dictionary:
    print(key," = ", dictionary[key])
