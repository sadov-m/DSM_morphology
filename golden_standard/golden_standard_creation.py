import morfessor
import time
import os
import re
import urllib
import requests
from lxml import html
import random
from time import sleep
import csv
#from scipy.stats import spearmanr
import numpy
from krippendorff_alpha import krippendorff_alpha, interval_metric

start_time = time.time()
io = morfessor.MorfessorIO()
reg_exp = re.compile('[а-яёА-ЯЁ]+')
model_types = io.read_binary_model_file('types')



def sort_by_morfessor_segmentation():
    path = 'C:/Users/Ольга/Downloads/lemmas_only'
    container = []
    words_for_gold_std = []

    for i in os.walk(path):
        container.append(i)

    for text_num, filename in enumerate(container[0][2]):
        with open(container[0][0]+'/'+filename, encoding='utf-8') as opener:
            text = opener.read()
            tokens = text.split(' ')
            tokens_set = set(tokens)

            for ind, token in enumerate(tokens_set):

                if reg_exp.search(token):

                    try:
                        candidate = model_types.segment(token)

                    except:
                        candidate = model_types.viterbi_segment(token)

                    if len(candidate) > 4:
                        words_for_gold_std.append(''.join(candidate))

                if ind % 10000 == 0:
                    print(ind, '/', len(tokens_set))
            #print(words_for_gold_std, len(words_for_gold_std))
            print("Elapsed time for a file: {:.3f} sec".format(time.time() - start_time))

            with open('gold_standard/%d.txt' % text_num, 'w', encoding='utf-8') as writer:
                writer.write(' '.join(words_for_gold_std))

            words_for_gold_std = []


def sort_by_freq_in_rnc():
    link = "http: // search2.ruscorpora.ru / search.xml?env = alpha & mycorp = & mysent = & mysize = & mysentsize = &" \
           " mydocsize = & spd = & text = lexgramm & mode = main & sort = gr_tagging & lang = ru & nodia = 1 &" \
           " parent1 = 0 & level1 = 0 & gramm1 = & sem1 = & sem - mod1 = sem & sem - mod1 = sem2 & flags1 = &" \
           " m1 = & parent2 = 0 & level2 = 0 & min2 = 1 & max2 = 1 & lex2 = & gramm2 = & sem2 = & sem - mod2 = sem &" \
           " sem - mod2 = sem2 & flags2 = & m2 = &"
    space_remover = re.compile('\S+')
    clean_link = ''.join(space_remover.findall(link))
    path_for_gold_std = 'C:/Users/Ольга/PycharmProjects/DSM_morphology/morfessor/multimorph_words'
    container_gold = []
    digit_finder = re.compile('\d+')

    for i in os.walk(path_for_gold_std):
        container_gold.append(i)

    with open('words_for_golden_standard.txt', 'w', encoding='utf-8') as writer:

        total_tokens_set = set()
        not_found_tokens = set()

        for text_num, filename in enumerate(container_gold[0][2]):

            with open(container_gold[0][0] + '/' + filename, encoding='utf-8') as opener:
                text = opener.read()
                tokens = text.split(' ')
                tokens_set = set(tokens)

                for token in tokens_set:

                    if token in total_tokens_set:
                        pass

                    else:
                        params = {'lex1': token.encode(encoding='windows-1251')}
                        page = requests.get(clean_link + urllib.parse.urlencode(params))
                        # in case of crash to see whether the page returns what was stated in Chrome
                        """with open('html.txt', 'w', encoding='utf-8') as f:
                          f.write(page.text)"""
                        tree = html.fromstring(page.content)
                        freq_xpath = "/html/body/div[@class='content']/p[3]/span[3]"

                        if freq_xpath:

                            freq = 0

                            try:
                                freq = ''.join(digit_finder.findall(tree.xpath(freq_xpath)[0].text_content()))

                            # if token not found in corpora
                            except IndexError:

                                if token in not_found_tokens:
                                    pass

                                else:
                                    print(token)
                                    not_found_tokens.add(token)

                            try:
                                freq = int(freq)

                            #if token is not digit
                            except TypeError:
                                print(token, freq)

                            if freq > 0 and freq < 1000:
                                writer.write(token + ' ' + str(freq) + '\n')
                                total_tokens_set.add(token)

                        sleep(0.3)  # so as not to be banned
                print("Elapsed time for a {} file: {:.3f} sec".format(text_num, time.time() - start_time))


def sort_by_rutez():
    path_to_a_rutez = 'C:/Users/Ольга/Desktop/rt.csv'

    with open(path_to_a_rutez, encoding='utf-8') as rutez_opener:
        strings = rutez_opener.read().split('\n')[1:]

    rutez_dictionary_related = {}

    for string in strings:
        string_unpacked = string.split(',') if string else ('', '', -1)
        target, value, estimation = string_unpacked[0], string_unpacked[1], int(string_unpacked[2])

        # to avoid unrelated words labeled as zero
        # and broken strings labeled -1 (see else clause at the string number 142)
        if estimation > 0:

            if target in rutez_dictionary_related:
                rutez_dictionary_related[target].add(value)

            else:
                rutez_dictionary_related[target] = set()
                rutez_dictionary_related[target].add(value)

            if value in rutez_dictionary_related:
                rutez_dictionary_related[value].add(target)

            else:
                rutez_dictionary_related[value] = set()
                rutez_dictionary_related[value].add(target)

    print("Elapsed time for a dictionary: {:.3f} sec".format(time.time() - start_time))

    with open('golden_standard_final.txt', encoding='utf-8') as gold_std_opener:

        words_for_pairing = gold_std_opener.read().split('\n')
        words_for_pairing = [pair.split(' ')[0] for pair in words_for_pairing]

        with open('problematic_words.txt', encoding='utf-8') as problematic_std_opener:

            another_words_for_pairing = problematic_std_opener.read().split('\n')
            words_for_pairing = set(words_for_pairing + another_words_for_pairing)

    with open('words_paired.txt', 'w', encoding='utf-8') as pairing_writer:

        for word in words_for_pairing:

            if word in rutez_dictionary_related:
                string_to_write = random.choice(list(rutez_dictionary_related[word]))
                #print(word, string_to_write, '\n', rutez_dictionary_related[word], '\n')
                pairing_writer.write(word+' '+string_to_write+'\n')

        print("Elapsed time for all: {:.3f} sec".format(time.time() - start_time))


def sort_morph_rich_by_freq():
    with open("golden_standard_final.txt", encoding='utf-8') as std_opener:
        words_and_freq = std_opener.read().split('\n')

    rare = []
    moderate = []
    frequent = []

    for elem in words_and_freq:
        word, freq = elem.split(' ')
        freq = int(freq)

        if word in rare or word in moderate or word in frequent:
            pass
        else:
            if freq < 11:
                rare.append(word)
            elif freq > 10 and freq < 101:
                moderate.append(word)
            else:
                frequent.append(word)

    print(rare[:40])
    print(moderate[:40])
    print(frequent[:40])


# checking rusvectores model for out-of-vocab words
def oov_words_finding():
    with open('words_for_golden_standard.txt', encoding='utf-8') as open_words:
        words = open_words.read().split('\n')

    with open('words out of vocab.txt', 'w', encoding='utf-8') as words_writer:

        for word_freq in words:
            word, freq = word_freq.split(' ')

            try:
                request = 'http://rusvectores.org/ruwikiruscorpora/%s/api/json' % word
                requests.get(request).json()

            except:
                words_writer.write(word+'\t'+freq+'\n')

            sleep(0.1) # so as not to be banned


# to see if there any out-of-vocab words to add to golden standard
def comparison_with_golden_standard():
    with open('words_paired.txt', encoding='utf-8') as open_pairs:
        paired_words = [pair.split(' ')[0] for pair in open_pairs.read().split('\n') if ' ' in set(pair)]
        already_in = []

        with open('words out of vocab.txt', encoding='utf-8') as open_oov:
            oov_words = [pair.split('\t')[0] for pair in open_oov.read().split('\n')]

        for oov_word in oov_words:
            if oov_word in paired_words:
                already_in.append(oov_word)
            else:
                print(oov_word)

        print(already_in)


# retrieving rusvectores model estimations for our golden standard
def get_model_estimations():
    float_finder = re.compile('\d+.\d+')
    with open('words_ruwikiruscorpora_estimated.txt', 'w', encoding='utf-8') as estimation_writer:

        with open('words_paired.txt', encoding='utf-8') as dataset_open:
            paired_words = [pair for pair in dataset_open.read().split('\n') if ' ' in set(pair)]

            for couple in paired_words:

                try:
                    target_word, paired_word = couple.split(' ')

                except ValueError:
                    print(couple)
                    exit(1)

                request = 'http://rusvectores.org/ruwikiruscorpora/%s__%s/api/similarity' % (target_word, paired_word)
                response = requests.get(request).text

                if response == 'Unknown':
                    estimation = 'na'

                else:
                    estimation = float_finder.findall(response)[0]

                estimation_writer.write(target_word + ' ' + paired_word + ' ' + estimation + '\n')


# get estimations of inter-annotator agreement
def golden_standard_parsing(alpha=True):
    path = 'C:/Users/Ольга/Downloads/golden_standard.csv'
    extract_pairs = re.compile('\w+-\w+-?\w+|\w+')

    with open(path, 'r', encoding='utf-8') as ex:
        reader = csv.reader(ex, delimiter=",")
        header = next(reader)
        evaluations = [] # every elem of a list is an annotator
        word_pairs = []

        for line in reader:
            evaluations.append([int(elem) for elem in line[4:]])

        for string in header[4:]:
            word_pairs.append('\t'.join(extract_pairs.findall(string)[-2:]))

        with open('words_paired_average_10.txt', 'w', encoding='utf-8') as writer:

            for ind, pair in enumerate(word_pairs):

                values = []

                for ident, annotator in enumerate(evaluations):

                    if ident not in [5,11,12]:
                        values.append(annotator[ind])

                writer.write(pair+'\t'+str(numpy.average(values))+'\n')

        # 1st version of inter-annotator agreement metric
        """def counting_spearman():
            # counting Spearman correlation as inter-annotator agreement metric
            length = len(evaluations)
            correlation = []

            for ind, annotator in enumerate(evaluations):
                print('annotator number:', ind)
                #avg_per_annotator = []
                #less_agr_annos = [5, 11, 12]

                #if ind not in less_agr_annos:

                for i in range(0, length):

                        if i != ind:#+less_agr_annos:

                            print('their correlation with annotator number:', i, 'is', spearmanr(annotator, evaluations[i]))
                            correlation.append(spearmanr(annotator, evaluations[i])[0])
                            #avg_per_annotator.append(spearmanr(annotator, evaluations[i])[0])
                #print('avg corr per annotator number', ind, 'is', numpy.average(avg_per_annotator))

            print('avg correlation is:', numpy.average(correlation))"""

        def alpha_counting():
            print("interval metric: %.3f" % krippendorff_alpha(evaluations, interval_metric, missing_items=[]))

        if alpha:
            alpha_counting()

golden_standard_parsing()
