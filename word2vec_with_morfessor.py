import gensim
import pymorphy2
import morfessor
import time
import numpy

start_time = time.time()
io = morfessor.MorfessorIO()
morph = pymorphy2.MorphAnalyzer()

model_types = io.read_binary_model_file('morfessor/types')

"""with open('lemmatized_data.txt', encoding='utf-8') as opener:
    mini_texts = opener.read().split('\n')
mini_texts = [mini_text.split(' ') for mini_text in mini_texts]
morph_texts = []
for text in mini_texts:
    morph_texts.append([])
    for lemma in text:
        try:
            morph_texts[-1].extend(model_types.segment(lemma))
        except KeyError:
            pass

model = gensim.models.Word2Vec(morph_texts, size=100, window=5, min_count=2, workers=4, negative=10)
model.save('word2vec_morpho')
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))"""
model = gensim.models.Word2Vec.load('word2vec_morpho')

word_for_test = morph.parse('украинский')[0].normal_form
compounds = []
try:
    compounds.extend(model_types.segment(word_for_test))
except KeyError:
    compounds.extend(model_types.viterbi_segment(word_for_test)[0])

vecs = []
print(compounds)
for compound in compounds:
    try:
        vecs.append(model[compound])
    except KeyError:
        vecs.append(numpy.array([0.0 for i in range(100)]))
total = 0
for ind, vec in enumerate(vecs):
    if ind == 0:
        total = vec
    else:
        total = numpy.add(total, vec)

print(model.similar_by_vector(total))