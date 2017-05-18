import gensim
import morfessor
import pymystem3
import numpy
from sklearn.externals import joblib
from scipy import spatial
import time

io = morfessor.MorfessorIO()
model = gensim.models.Word2Vec.load('word2vec_morpho')
analyzer = pymystem3.Mystem()
word_for_analysis = input("введите слово для анализа: ")
top_n = int(input("сколько топ-кандидатов показывать? введите целое число: "))
start_time = time.time()
modifier = 0.5

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
                segments = model_types.viterbi_segment(lemma)[0]

            for segment in segments:
                # some debugging due to a different output mode for known and unknown words for our morfessor model
                try:
                    if segment in final_dict:
                        final_dict[segment].add(lemma)
                    else:
                        final_dict[segment] = set()
                        final_dict[segment].add(lemma)
                except TypeError:
                    print(segment, segments, lemma)
                    exit(1)
    print("Elapsed time for a file: {:.3f} sec".format(time.time() - start_time))

    joblib.dump(final_dict, 'dict_of_compounds')

dictionary = joblib.load('dict_of_compounds')

word_for_test = analyzer.lemmatize(word_for_analysis)[0]
compounds = []

try:
    compounds.extend(model_types.segment(word_for_test))
except KeyError:
    compounds.extend(model_types.viterbi_segment(word_for_test)[0])

vecs = []
print(compounds)

candidates = set()
# getting ready vecs for our target word + searching for candidates for it
for compound in compounds:
    try:
        vecs.append(model[compound])
    except KeyError:
        vecs.append(numpy.array([0.0 for i in range(300)]))
    try:
        candidates.update(dictionary[compound])
    except KeyError:
        pass

total = 0
for ind, vec in enumerate(vecs):
    length = len(vecs)
    if ind == 0:
        total = vec * modifier
    elif ind == length - 1:
        total = numpy.add(total, vec * modifier)
    else:
        total = numpy.add(total, vec)

print(len(candidates))

vecs_for_candidates = []
candidates = list(candidates)

for candidate in candidates:

    candidate_compounds = []
    try:
        candidate_compounds.extend(model_types.segment(candidate))
    except KeyError:
        candidate_compounds.extend(model_types.viterbi_segment(candidate)[0])

    candidate_vecs = []
    for candidate_compound in candidate_compounds:
        try:
            candidate_vecs.append(model[candidate_compound])
        except KeyError:
            candidate_vecs.append(numpy.array([0.0 for i in range(300)]))

    final = 0
    for ind, vec in enumerate(candidate_vecs):
        length = len(candidate_vecs)
        if ind == 0:
            final = vec * modifier
        elif ind == length - 1:
           final = numpy.add(final, vec * modifier)
        else:
            final = numpy.add(final, vec)

    vecs_for_candidates.append(final)

results = []
for vector in vecs_for_candidates:
    results.append(1 - spatial.distance.cosine(total, vector))

top_n_indexes = sorted(range(len(results)), key=lambda i: results[i])[-top_n:]

for index in top_n_indexes:
    print(word_for_analysis, "the best candidate is:", candidates[index], ", distance:", results[index])

print("Elapsed time for this word: {:.3f} sec".format(time.time() - start_time))
#print(model.similar_by_vector(total))
