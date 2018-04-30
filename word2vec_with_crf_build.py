import gensim
import time

start_time = time.time()
path = 'trial_data.txt'


class MySentences(object):
    def __init__(self, dirname):
        self.path_name = path

    def __iter__(self):

        for line in open(self.path_name, encoding='utf-8', errors='ignore'):

            output = []

            for word in line.split():

                output.append(word)

            yield output


corpus = MySentences(path)  # a memory-friendly iterator from Rehurek's post"""
#with open(path, encoding='utf-8') as input_file:
#    corpus = [line.strip().split(' ') for line in input_file.readlines()]

model = gensim.models.Word2Vec(corpus, sg=1, size=300, window=5, min_count=3, workers=-1, negative=15)

model.save('word2vec_crf')
del corpus
print("Elapsed time for learning: {:.3f} sec".format(time.time() - start_time))
