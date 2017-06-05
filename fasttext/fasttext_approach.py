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
    print u'что' in model
    print(model[u'что'])

    print u'сепулька' in model
    print(model[u'сепулька'])
