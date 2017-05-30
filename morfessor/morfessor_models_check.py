import morfessor
import time
import re

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
