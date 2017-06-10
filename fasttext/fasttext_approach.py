# coding: utf-8
import fasttext
import time
from scipy import spatial

path = 'data.txt'
start_time = time.time()


def training_the_model():
    # first training: '/home/ubuntu/PycharmProjects//DSM_morphology/data.txt'
    fasttext.skipgram(path, 'fasttext_model', dim=300, min_count=5, neg=15, minn=4, maxn=5)


#training_the_model()
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))


def checking_the_model(word_pairs_to_check, manual_input=False):
    model = fasttext.load_model('/media/ubuntu/14_0/fasttext_model.bin')#'model.bin')

    if manual_input:
        print u'sorry, this function is currently unfinished'
        word_to_analyze = raw_input('type in a word to check: ')
        word_to_compare = raw_input('type in the second word: ')

    else:

        with open('fasttext_w2v_estimations.txt', 'w') as writer:

            for pair in word_pairs_to_check:

                word_to_analyze, word_to_compare, value = pair.split('\t')

                dataSetI = model[word_to_analyze]
                dataSetII = model[word_to_compare]
                result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
                writer.write(word_to_analyze + '\t' + word_to_compare + '\t' + str(result) + '\n')
                #print(word_to_analyze, word_to_compare,result)
            print("Elapsed time for estimation: {:.3f} sec".format(time.time() - start_time))

#strings = [u'кумовство потакание', u'ребенок\tбаловаться', u'жизнь\nсуществование']
#checking_the_model(strings)

with open('/home/ubuntu/PycharmProjects/DSM_morphology/morfessor/'
          'golden_standard_final.txt') as opener:
    words_pairs = opener.read().split('\n')

checking_the_model(words_pairs)
