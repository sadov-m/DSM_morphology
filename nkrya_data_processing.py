import json
import time

#making data for word2vec
start_time = time.time()
lemmas = []

with open('data.txt', 'w', encoding='utf-8') as writer: # output file

    with open('ruscorpora_lemmatized.json', encoding='utf-8') as json_opener: #input json file

        for linea in json_opener:
            line = json.loads(linea)
            lemma = []

            for dict in line:
                if dict['analysis']:
                    lemma.append(dict['analysis'][0]['lex'])
                else:
                    lemma.append(dict['text'])

            if len(lemma) < 3:  # skip all the sentences that have less than 3 words
                pass
            else:
                lemmas.append(lemma)

            if len(lemmas) == 100000:
                writer.write('\n'.join([' '.join(sent).lower() for sent in lemmas]))
                print("Elapsed time for 100 thousand sents: {:.3f} sec".format(time.time() - start_time))
                lemmas = []
