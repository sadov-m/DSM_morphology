import gensim
import pymorphy2
import morfessor
import time

start_time = time.time()
io = morfessor.MorfessorIO()
morph = pymorphy2.MorphAnalyzer()

model_types = io.read_binary_model_file('morfessor/types')

with open('lemmatized_data.txt', encoding='utf-8') as opener:
    mini_texts = opener.read().split('\n')
mini_texts = [mini_text.split(' ') for mini_text in mini_texts]
morph_texts = []
for text in mini_texts:
    morph_texts.append([])
    for lemma in text:
        try:
            morph_texts[-1].extend(model_types.segment(lemma))
        except KeyError:
            morph_texts[-1].extend(model_types.viterbi_segment(lemma))

model = gensim.models.Word2Vec(morph_texts, sg=1, size=300, window=5, min_count=3, workers=4, negative=15)
model.save('word2vec_morpho')
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))
