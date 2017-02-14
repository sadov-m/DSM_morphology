# coding: utf-8
import fasttext
import sys

corpus = sys.argv[1]


model = fasttext.cbow(sys.argv[1], 'model') #learning
print(model.words) # list of words in dictionary

#model = fasttext.load_model('model.bin')
#print(model.words) #trying to list the words the model knows, though no result
#print(model['что'])
#"""