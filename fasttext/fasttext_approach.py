# coding: utf-8
import fasttext
import time

path = '/home/ubuntu/lemmas_only/text_0.txt'
start_time = time.time()


def training_the_model():
    # first training: '/home/ubuntu/PycharmProjects//DSM_morphology/data.txt'
    fasttext.skipgram(path, 'model', dim=300, min_count=3, neg=15, thread=3)

training_the_model()
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))


def checking_the_model():
    model = fasttext.load_model('model.bin')

    # toy model: '/home/ubuntu/PycharmProjects/DSM_morphology/fasttext/first_model_cbow/model.bin')
    #print u'что' in model
    #print(model[u'что'])

    #print u'сепулька' in model
    #print(model[u'сепулька'])

    classic_model = gensim.models.Word2Vec.load('/home/ubuntu/model_w2v/word2vec_standart')

    word_to_analyze = u'гнать' # input('type in a word to check: ')

    print('similar words by vector are:',
          classic_model.most_similar(positive=[numpy.array(model[word_to_analyze], dtype='float32')], topn = 5))

checking_the_model()
