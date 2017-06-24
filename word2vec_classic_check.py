import gensim
#import pymystem3
from scipy import spatial

#word = input("введите слово для анализа: ")
#analyzer = pymystem3.Mystem()
model = gensim.models.Word2Vec.load('word2vec_standart')
#print(model.most_similar(positive=analyzer.lemmatize(word)[0]))
#print(model[word])

def w2v_classic_estimations_retrieval():

    with open('morfessor/golden_standard_final.txt', encoding='utf-8') as opener:
        words_pairs = opener.read().split('\n')

    with open('classic_w2v_estimations.txt', 'w', encoding='utf-8') as writer:

        for pair in words_pairs:

            word_1, word_2, value = pair.split('\t')

            try:
                result = model.similarity(word_1, word_2)
                dataSetI = model[word_1]
                dataSetII = model[word_2]
                result_vec = 1 - spatial.distance.cosine(dataSetI, dataSetII)
                print(result, result_vec)

            except KeyError:
                result = 'na'
                print('not in vocab')

            writer.write(word_1+'\t'+word_2+'\t'+str(result)+'\n')

w2v_classic_estimations_retrieval()
