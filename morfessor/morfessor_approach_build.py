import morfessor
import math
import os
import time

start_time = time.time()
io = morfessor.MorfessorIO()

pdir = 'C:/Users/Ольга/Downloads/lemmas_only'
contdir = []

for i in os.walk(pdir):
    contdir.append(i)
print(type(contdir[0][0]), contdir[0][0])
# training (all the steps)

train_data = list(io.read_corpus_files([contdir[0][0]+'/'+contdir[0][2][i] for i in range(len(contdir))]))
print("Elapsed time for reading: {:.3f} sec".format(time.time() - start_time))

model_types = morfessor.BaselineModel()
#model_logtokens = morfessor.BaselineModel()

# loading data and defining the count modifiers
model_types.load_data(train_data, count_modifier=lambda x: 1)
print("Elapsed time for loading: {:.3f} sec".format(time.time() - start_time))


# for logtokens model
def log_func(x):
    return int(round(math.log(x + 1, 2)))
#model_logtokens.load_data(train_data, count_modifier=log_func)

models = [model_types]#, model_logtokens]

# training
for model in models:
    model.train_batch()
print("Elapsed time for training: {:.3f} sec".format(time.time() - start_time))

io.write_binary_model_file('types', model_types)
print("Elapsed time for saving: {:.3f} sec".format(time.time() - start_time))
#io.write_binary_model_file('log_tokens', model_logtokens)
