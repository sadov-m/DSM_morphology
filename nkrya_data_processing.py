import json
import time

#making data for word2vec
start_time = time.time()
lemmas = []
index = 0
with open('C:/Users/Ольга/Downloads/ruscorpora_lemmatized.json', encoding='utf-8') as json_opener:
    for linea in json_opener:
        line = json.loads(linea)
        lemma = []

        for dict in line:
            if dict['analysis']:
                lemma.append(dict['analysis'][0]['lex'])
            else:
                lemma.append(dict['text'])

        if len(lemma) < 3: # skip all the sentences that have less than 3 words
            pass
        else:
            lemmas.append(lemma)
        if len(lemmas) == 100000:
            with open('C:/Users/Ольга/Downloads/lemmas_only/text_%d.txt' % index, 'w', encoding='utf-8') as writer:
                writer.write('\n'.join([' '.join(sent).lower() for sent in lemmas]))
            print("Elapsed time for 100 thousand sents: {:.3f} sec".format(time.time() - start_time))
            lemmas = []
            index += 1
