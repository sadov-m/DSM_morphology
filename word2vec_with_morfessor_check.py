import gensim
import morfessor
import pymystem3
import numpy
import time
from scipy import spatial

io = morfessor.MorfessorIO()
model = gensim.models.Word2Vec.load('word2vec_morpho')
analyzer = pymystem3.Mystem()
start_time = time.time()
model_types = io.read_binary_model_file('morfessor/types')

# for manual input
#word_for_analysis = input('type in a word: ')
#word_to_compare = input('type in another word: ')


def vec_for_word(word, return_sum=True):
    word_for_test = word #analyzer.lemmatize(word)[0]
    compounds = []

    try:
        compounds.extend(model_types.segment(word_for_test))
    except KeyError:
        compounds.extend(model_types.viterbi_segment(word_for_test)[0])

    vecs = []
    #print('the compounds are:', compounds)

    # getting ready vecs for our target word
    for compound in compounds:

        try:
            vecs.append(model[compound])

        except KeyError:
            vecs.append(numpy.zeros(300, dtype='float32'))

    total_sum = numpy.zeros(300, dtype='float32')

    for ind, vec in enumerate(vecs):
        total_sum += vec
        # numpy.add(total_sum, vec)

    total_average = total_sum/float(len(compounds))

    if return_sum:
        return total_sum
    else:
        return total_average


def estimations_retrieval():

    with open('morfessor/golden_standard_final.txt', encoding='utf-8') as opener:
        words_pairs = opener.read().split('\n')

    with open('morfessor/morpho_w2v_estimations.txt', 'w', encoding='utf-8') as writer:

        for pair in words_pairs:

            word_1, word_2, value = pair.split('\t')
            dataSetI = vec_for_word(word_1)
            dataSetII = vec_for_word(word_2)
            result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
            writer.write(word_1+'\t'+word_2+'\t'+str(result)+'\n')

    print("Elapsed time for estimation: {:.3f} sec".format(time.time() - start_time))
