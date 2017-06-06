# coding: utf-8
import fasttext
import time
from scipy import spatial

path = 'data.txt'
start_time = time.time()


def training_the_model():
    # first training: '/home/ubuntu/PycharmProjects//DSM_morphology/data.txt'
    fasttext.skipgram(path, 'fasttext_model', dim=300, min_count=5, neg=15, minn=2, maxn=4)

training_the_model()
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))


# word_pairs should be loaded as a list in which every pair is a string
# string should cointain two words separated by space or escape sequence (\t,\n)
def checking_the_model(word_pairs_to_check, manual_input=False):
    model = fasttext.load_model('model.bin')

    if manual_input:
        word_to_analyze = raw_input('type in a word to check: ')
        word_to_compare = raw_input('type in the second word: ')

    else:

        for pair in word_pairs_to_check:

            word_1, word_2 = pair.split()

            dataSetI = model[word_1]
            dataSetII = model[word_2]
            result = 1 - spatial.distance.cosine(dataSetI, dataSetII)

            print(word_1, word_2,result)
            print("Elapsed time for this word: {:.3f} sec".format(time.time() - start_time))

#strings = [u'кумовство потакание', u'ребенок\tбаловаться', u'жизнь\nсуществование']
#checking_the_model(strings)
