import gensim
import morfessor
import time
import os

start_time = time.time()
io = morfessor.MorfessorIO()
model_types = io.read_binary_model_file('morfessor/types')
path_dir = 'C:/Users/Ольга/Downloads/lemmas_only' # 'C:/Users/Ольга/Desktop/test'


class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):

            for line in open(os.path.join(self.dirname, fname), encoding='utf-8', errors='ignore'):

                output = []

                for word in line.split():

                    try:
                        output.extend(model_types.segment(word))
                    except KeyError:
                        output.extend(model_types.viterbi_segment(word)[0])
                    output.append(' ')

                yield output

corpus = MySentences(path_dir)  # a memory-friendly iterator from Rehurek's post
model = gensim.models.Word2Vec(corpus, sg=1, size=300, window=5, min_count=3, workers=4, negative=15)

model.save('word2vec_morpho')
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))
