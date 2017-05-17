import gensim
import morfessor
import pymorphy2
import numpy
from sklearn.externals import joblib

io = morfessor.MorfessorIO()
model = gensim.models.Word2Vec.load('word2vec_morpho')
morph = pymorphy2.MorphAnalyzer()
word_for_analysis = input("введите слово для анализа: ")

model_types = io.read_binary_model_file('morfessor/types')


def dictionary_creation():
    final_dict = {}

    with open('lemmatized_data.txt', encoding='utf-8') as opener:
        mini_texts = opener.read().split('\n')
    mini_texts = [mini_text.split(' ') for mini_text in mini_texts]
    for text in mini_texts:

        for lemma in text:
            try:
                segments = model_types.segment(lemma)
            except KeyError:
                segments = model_types.viterbi_segment(lemma)

            for segment in segments:
                if segment in final_dict:
                    final_dict[segment].add(lemma)
                else:
                    final_dict[segment] = set()
                    final_dict[segment].add(lemma)

    joblib.dump(final_dict, 'dict_of_compounds')

dictionary = joblib.load('dict_of_compounds')

word_for_test = morph.parse(word_for_analysis)[0].normal_form
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

# seraching for candidates for our analyzed word
candidates = set()
for compound in compounds:
    try:
        candidates.update(dictionary[compound])
    except KeyError:
        pass


#print(model.similar_by_vector(total))
