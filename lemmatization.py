import codecs
import re
import pymorphy2
import time

start_time = time.time()
#I've chosen pymorphy for lemmatization because the performance of MyStem in terms of stability leaves much to be desired
morph = pymorphy2.MorphAnalyzer()

with codecs.open('corpus.txt', "r", encoding='utf-8', errors='ignore') as news:
    text_lines = news.readlines()

#been thinking about to load sentences in DSM, but then decided to load the whole paragraph instead
#sents = re.split('(?<!\w\.\w.)(?<![А-Я][а-я]\.)(?<=\.|\?)\s', text_lines[0])

reg_exp = re.compile('[а-яё]+')
def tokenize_n_lemmatize(text_string):
    text_string = text_string.lower().replace('ё', 'е')
    tokens = reg_exp.findall(text_string)
    lemmas = [morph.parse(token)[0].normal_form for token in tokens]
    return lemmas

#it takes time, but for now it's bearable
lemmatized_paragraphs = [tokenize_n_lemmatize(text_line) for text_line in text_lines]
print("Elapsed time for tokenization + lemmatization: {:.3f} sec".format(time.time() - start_time))

with open('lemmatized_data.txt', 'w') as writer:
    for paragraph in lemmatized_paragraphs:
        writer.write(' '.join(paragraph)+'\n')