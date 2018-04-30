import gensim
import numpy
from scipy import spatial

model = gensim.models.Word2Vec.load('w2v_models/word2vec_standart')
morph_model = gensim.models.Word2Vec.load('w2v_models/word2vec_crf')

oov_words = []

with open('crf-based/golden_standard_crf_processed.txt', encoding='utf-8') as opener:
    pairs = [line.split('\t') for line in opener.read().split('\n')]


def vec_for_word(word, return_sum=True):
    word_for_test = word
    compounds = word_for_test.split(' ')

    vecs = []

    # getting ready vecs for our target word
    for compound in compounds:

        try:
            vecs.append(morph_model[compound])

        except KeyError:
            vecs.append(numpy.zeros(300, dtype='float32'))

    total_sum = numpy.zeros(300, dtype='float32')

    for ind, vec in enumerate(vecs):
        total_sum += vec

    if return_sum:
        return total_sum
    else:
        total_average = total_sum / float(len(compounds))
        return total_average


with open('w2v_model_estimations_crf.txt', 'w', encoding='utf-8') as writer:

    for i in range(1, len(pairs), 2):

        word_norm_1, word_morphed_1 = pairs[i][0], pairs[i][1]
        word_norm_2, word_morphed_2 = pairs[i-1][0], pairs[i-1][1]
        words = [word_norm_1, word_morphed_1, word_norm_2, word_morphed_2]

        vecs_for_words = []

        for j in range(0, len(words), 2):

            try:
                vecs_for_words.append(model[words[j]])
            except KeyError:
                vecs_for_words.append(vec_for_word(words[j+1]))
                oov_words.append(words[j])

        result = 1 - spatial.distance.cosine(vecs_for_words[0], vecs_for_words[1])

        if result < 0:
            result = 0.0
        elif word_norm_1 == 'кефир' or word_norm_2 == 'кефир':
            result = 0.0

        writer.write(word_norm_1+'\t'+word_norm_2+'\t'+str(result)+'\n')

#print(oov_words)
