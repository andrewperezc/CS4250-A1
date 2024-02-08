#-------------------------------------------------------------------------
# AUTHOR: Andrew Perez
# FILENAME: indexing.py
# SPECIFICATION: 
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/
#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays
#Importing some Python libraries
import csv
from os import remove
import math

#documents = ["I love cats and cats", "She loves her dog", "They love their dogs and cat"]
documents = []

#Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0: # skipping the header
            documents.append (row[0])
#Conducting stopword removal. Hint: use a set to define your stopwords.
stopWords = {'for', 'or', 'and', 'nor', 'but', 'yet','so', 
             'i', 'her', 'his', 'she', 'he', 'they', 'their',
             'hers', 'his', 'theirs'}
count = 0
for document in documents:
    sentence = document.lower().split() #split document sentences by word
    sentenceRemoveStopWords = [word for word in sentence if word not in stopWords] #if a word is in stopWord, remove from sentence
    documents.remove(document)
    documents.insert(count, sentenceRemoveStopWords) # replace the document with the new split and filtered 
    count += 1


#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
stemming = {
    "loves" : "love",
    "cats" : "cat",
    "dogs" : "dog"
}

for document in documents:
    count = -1
    for word in document:
        count += 1
        if word in stemming:
            document.remove(word)
            document.insert(count, stemming.get(word))


#Identifying the index terms.
terms = []
for document in documents:
    for term in document:
        if term not in terms:
            terms.append(term)

# keep track of count of word per document
d1 = {}
d2 = {}
d3 = {}

def currentDoc(x): # switch between d1, d2, d3
    match x:
        case 1:
            return d1
        case 2:
            return d2
        case 3:
            return d3 

# count the occurrences of a term in a document
documentNum = 0
for document in documents:
    documentNum += 1
    for term in document:
        if term not in currentDoc(documentNum):
            currentDoc(documentNum).update({term : 1})
        else:
            currentDoc(documentNum)[term] += 1

#Building the document-term matrix by using the tf-idf weights.
# initialize docTermMatrix
docTermMatrix = [ [0]*(len(terms)+1) for i in range(len(documents)+1)]
for x in range(len(terms)):
    docTermMatrix[x+1][0] = terms[x]
    docTermMatrix[0][x+1] = "d"+ str(x+1)

#perform tf calculations
def tf(term, docNum):
    if term in currentDoc(docNum+1):
        return currentDoc(docNum+1)[term] / len(documents[docNum])
    else:
        return 0

#perform idf calculations
def idf(term):
    numOfDocsIn = 0
    length = len(documents)
    for docNum in range(length):
        if term in currentDoc(docNum+1):
            numOfDocsIn += 1
    return math.log10(length/numOfDocsIn)

# populate the rest of docTermMatrix
for col in range(len(documents)):
    for row in range(len(terms)):
        if terms[col] not in currentDoc(col+1): #if a term is not found in a document, 0
            docTermMatrix[row+1][col+1] = 0
        else: # calculate td-idf = tf(term, d) * idf(term, D)
            docTermMatrix[row+1][col+1] = tf(terms[row], col) * idf(terms[row])

#Printing the document-term matrix.
#--> add your Python code here
for x in range(len(docTermMatrix)):
    print(docTermMatrix[x],"\n")
