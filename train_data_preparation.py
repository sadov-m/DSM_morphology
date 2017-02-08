import codecs
import re
from bs4 import BeautifulSoup
import pymorphy2
import time

start_time = time.time()
morph = pymorphy2.MorphAnalyzer()

with codecs.open('some_news_tar', "r", encoding='utf-8', errors='ignore') as news:
    strings = news.readlines()

texts_only = []
length = len(strings)
container = ''

reg_exp = re.compile('[а-яё]+')
def tokenize_n_lemmatize(text_string):
    text_string = text_string.lower().replace('ё', 'е')
    tokens = reg_exp.findall(text_string)
    lemmas = []
    for token in tokens:
        lemmas.append(morph.parse(token)[0].normal_form)
    return lemmas

for line in strings:
    flag_end = re.findall('</TEXT>', line)
    if flag_end:
        beaux_text = BeautifulSoup(container, "lxml")
        n_text = beaux_text.get_text()
        texts_only.append(n_text)
        #texts_only.append(' '.join(tokenize_n_lemmatize(container)))
        #texts_only.append(container)
        container = ''
        print("Elapsed time for one text: {:.3f} sec".format(time.time() - start_time))
    else:
        flag_p = re.findall('<p>', line)
        if flag_p:
            container += line.strip()

print(texts_only[0])

with open('train_data.txt', 'w', encoding='utf-8') as writer:
    writer.write('\n'.join(texts_only[::2]))