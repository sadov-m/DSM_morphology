import gensim
import morfessor
import pymystem3
import numpy
# from scipy import spatial
import time

io = morfessor.MorfessorIO()
model = gensim.models.Word2Vec.load('word2vec_morpho')
classic_model = gensim.models.Word2Vec.load('word2vec_standart')
analyzer = pymystem3.Mystem()
start_time = time.time()
word_for_analysis = input('type in a word: ')
model_types = io.read_binary_model_file('morfessor/types')

word_for_test = analyzer.lemmatize(word_for_analysis)[0]
compounds = []

try:
    compounds.extend(model_types.segment(word_for_test))
except KeyError:
    compounds.extend(model_types.viterbi_segment(word_for_test)[0])

vecs = []
print('the compounds are:', compounds)

# getting ready vecs for our target word
for compound in compounds:

    try:
        vecs.append(model.wv[compound])
        values_type = set()
        for digit in model.wv[compound]:
            values_type.add(type(digit))
        print(values_type)
        # print('similar by compound:', model.wv.most_similar(positive=[compound]))
    except KeyError:
        vecs.append(numpy.array([0.0 for i in range(300)], dtype='float32'))

total_sum = numpy.array([0.0 for j in range(300)], dtype='float32')
values_type = set()
for digit in total_sum:
    values_type.add(type(digit))
print(values_type)

for ind, vec in enumerate(vecs):
    total_sum += vec
    # numpy.add(total_sum, vec)

values_type = set()
for digit in total_sum:
    values_type.add(type(digit))
print(values_type)
total_average = total_sum/float(len(compounds))

print('similar by sum_vector are:', classic_model.wv.similar_by_vector(total_sum))
print('similar by average_vector are:', classic_model.wv.similar_by_vector(total_average))
print('similar by classic model are:', classic_model.wv.most_similar(positive=[word_for_test]))
print("Elapsed time for this word: {:.3f} sec".format(time.time() - start_time))
