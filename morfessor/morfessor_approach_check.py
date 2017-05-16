import morfessor
import time
import os
import re
import urllib
import requests
from lxml import html

"""import pymystem3

analyzer = pymystem3.Mystem()"""
segmentation_check = False
start_time = time.time()
io = morfessor.MorfessorIO()
reg_exp = re.compile('[а-яёА-ЯЁ]+')

#model_log_tok = io.read_binary_model_file('log_tokens')
model_types = io.read_binary_model_file('types')


#a bit of testing
def morfessor_check(flag):
    if segmentation_check:
        words = ['классный', 'молочник', 'поприветствовать', 'образованный', 'нет', 'дегидратация', 'обуславливаемый', 'недопетый', 'полигидрокарбонат', 'тяп-ляп']

        # for words the model knows
        print(model_types.segment('украинский'))

        # for words the model doesn't know
        for word in words:
            #print(model_log_tok.viterbi_nbest(word,1))
            print(model_types.viterbi_nbest(word,1))

morfessor_check(segmentation_check)


def simple_lex_sort():
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
                    if len(candidate) > 4 and len(token) > 10:
                        words_for_gold_std.append(''.join(candidate))
                if ind % 10000 == 0:
                    print(ind, '/', len(tokens_set))
            #print(words_for_gold_std, len(words_for_gold_std))
            print("Elapsed time for a file: {:.3f} sec".format(time.time() - start_time))
            with open('gold_standard/%d.txt' % text_num, 'w', encoding='utf-8') as writer:
                writer.write(' '.join(words_for_gold_std))
            words_for_gold_std = []


def sort_by_freq():
    link = "http: // search2.ruscorpora.ru / search.xml?env = alpha & mycorp = & mysent = & mysize = & mysentsize = &" \
           " mydocsize = & spd = & text = lexgramm & mode = main & sort = gr_tagging & lang = ru & nodia = 1 &" \
           " parent1 = 0 & level1 = 0 & gramm1 = & sem1 = & sem - mod1 = sem & sem - mod1 = sem2 & flags1 = &" \
           " m1 = & parent2 = 0 & level2 = 0 & min2 = 1 & max2 = 1 & lex2 = & gramm2 = & sem2 = & sem - mod2 = sem &" \
           " sem - mod2 = sem2 & flags2 = & m2 = &"
    space_remover = re.compile('\S+')
    digit_finder = re.compile('\d+')
    clean_link = ''.join(space_remover.findall(link))
    path_for_gold_std = 'C:/Users/Ольга/PycharmProjects/DSM_morphology/morfessor/gold_standard'
    container_gold = []

    for i in os.walk(path_for_gold_std):
        container_gold.append(i)

    with open('golden_standard_final.txt', 'w', encoding='utf-8') as writer:
        for text_num, filename in enumerate(container_gold[0][2]):

            with open(container_gold[0][0] + '/' + filename, encoding='utf-8') as opener:
                text = opener.read()
                tokens = text.split(' ')
                tokens_set = set(tokens)

                for token in tokens_set:
                    params = {'lex1': token.encode(encoding='windows-1251')}
                    page = requests.get(clean_link + urllib.parse.urlencode(params))
                    # in case of crash to see whether the page returns what was stated in Chrome
                    """with open('html.txt', 'w', encoding='utf-8') as f:
                f.write(page.text)"""
                    tree = html.fromstring(page.content)
                    freq_xpath = "/html/body/div[@class='content']/p[3]/span[3]"

                    if freq_xpath == [] or token == "заподозривать":
                        pass
                    else:
                        freq = 1001
                        try:
                            freq = ''.join(digit_finder.findall(tree.xpath(freq_xpath)[0].text_content()))
                        except:
                            print(token)


                        try:
                            freq = int(freq)
                        except TypeError:
                            print(token, freq)

                        if freq < 1000:
                            writer.write(token+' '+str(freq)+'\n')
            print("Elapsed time for a {} file: {:.3f} sec".format(text_num, time.time() - start_time))
