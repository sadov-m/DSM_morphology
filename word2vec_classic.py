import gensim
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

with open('lemmatized_data.txt', encoding='utf-8') as opener:
    mini_texts = opener.readlines()
mini_texts = [mini_text.split(' ') for mini_text in mini_texts]

"""model = gensim.models.Word2Vec(mini_texts, size=100, window=5, min_count=2, workers=4, negative=10)
model.save('word2vec_standart')"""
model = gensim.models.Word2Vec.load('word2vec_standart')
#print(model.most_similar(positive=morph.parse('россия')[0].normal_form))
print(model['компьютер'])