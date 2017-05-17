import gensim
import pymystem3

word = input("введите слово для анализа: ")
analyzer = pymystem3.Mystem()
model = gensim.models.Word2Vec.load('word2vec_standart')
print(model.most_similar(positive=analyzer.lemmatize(word)[0]))
#print(model[word])
