import gensim
from scipy import spatial
import morfessor
import numpy

model = gensim.models.Word2Vec.load('word2vec_standart')
morph_model = gensim.models.Word2Vec.load('word2vec_morpho')
io = morfessor.MorfessorIO()
model_types = io.read_binary_model_file('morfessor/types')
oov_words = []


def vec_for_word(word, return_sum=True):
    word_for_test = word
    compounds = []

    # try:
    #    compounds.extend(model_types.segment(word_for_test))
    # except KeyError:
    compounds.extend(model_types.viterbi_segment(word_for_test)[0])

    vecs = []

    # getting ready vecs for our target word
    for compound in compounds:

        try:
            vecs.append(model[compound])

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


def w2v_classic_estimations_retrieval():

    with open('morfessor/golden_standard_final.txt', encoding='utf-8') as opener:
        words_pairs = opener.read().split('\n')

    with open('united_w2v_model_estimations.txt', 'w', encoding='utf-8') as writer:

        for pair in words_pairs:

            word_1, word_2, value = pair.split('\t')
            vecs_for_words = []

            for word in [word_1, word_2]:
                try:
                    vecs_for_words.append(model[word])
                except KeyError:
                    vecs_for_words.append(vec_for_word(word))
                    oov_words.append(word)

            result = 1 - spatial.distance.cosine(vecs_for_words[0], vecs_for_words[1])

            writer.write(word_1+'\t'+word_2+'\t'+str(result)+'\n')


w2v_classic_estimations_retrieval()

with open('oov_words.txt', 'w', encoding='utf-8') as oov_file:
    oov_file.write('\n'.join(oov_words))
