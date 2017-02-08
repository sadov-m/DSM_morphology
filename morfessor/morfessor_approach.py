import morfessor
import math

io = morfessor.MorfessorIO()

#training (all the steps)
"""train_data = list(io.read_corpus_file('C:/Users/Ольга/PycharmProjects/coursepaper_dsm/lemmatized_data.txt'))

model_types = morfessor.BaselineModel()
model_logtokens = morfessor.BaselineModel()

#loading data and defining the count modifiers
model_types.load_data(train_data, count_modifier=lambda x: 1)
def log_func(x):
    return int(round(math.log(x + 1, 2)))
model_logtokens.load_data(train_data, count_modifier=log_func)

models = [model_types, model_logtokens]
#training
for model in models:
    model.train_batch()

io.write_binary_model_file('types', model_types)
io.write_binary_model_file('log_tokens', model_logtokens)
"""
model_log_tok = io.read_binary_model_file('log_tokens')
model_types = io.read_binary_model_file('types')

#a bit of testing
words = ['классный', 'молочник', 'поприветствовать', 'образованный', 'нет', 'дегидратация', 'обуславливаемый', 'недопетый', 'полигидрокарбонат', 'тяп-ляп']

#for words the model knows
print(model_types.segment('украинский'))

#for words the model doesn't know
for word in words:
    print(model_log_tok.viterbi_nbest(word,1))
    print(model_types.viterbi_nbest(word,1))
    print('\n')