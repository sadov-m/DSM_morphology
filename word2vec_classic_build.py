import gensim
import os
import time

start_time = time.time()
pdir = 'C:/Users/Ольга/Downloads/lemmas_only'
contdir = []

for i in os.walk(pdir):
    contdir.append(i)

# trying to iteratively learn the model updating it
"""index = 0
corpus = []
model = ''
    for filename in contdir[0][2]:
    with open(contdir[0][0]+'/'+filename, encoding='utf-8') as opener:
        for ind, line in enumerate(opener):
            text_string = line.split(' ')
            corpus.append(text_string)
        if index == 0:
            model = gensim.models.Word2Vec(corpus, sg=1, size=300, window=5, min_count=3, workers=4, negative=15)
            index += 1
            corpus = []
        else:
            model.train(corpus, total_words = sum([len(sent) for sent in corpus]))
        print("Elapsed time for reading: {:.3f} sec".format(time.time() - start_time))"""


# for loading the model sentence by sentence
class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname), encoding='utf-8', errors='ignore'):
                yield line.split()


corpus = MySentences('C:/Users/Ольга/Downloads/lemmas_only')  # a memory-friendly iterator
#model = gensim.models.Word2Vec(sentences)
model = gensim.models.Word2Vec(corpus, sg=1, size=300, window=5, min_count=3, workers=4, negative=15)
print("Elapsed time for training: {:.3f} sec".format(time.time() - start_time))

model.save('word2vec_standart')
