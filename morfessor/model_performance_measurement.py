from scipy.stats import spearmanr

golden_standard_path = 'golden_standard_final.txt'
fasttext_model_eval_path = '../fasttext/fasttext_w2v_estimations.txt'
united_w2v_model_eval_path = '../united_w2v_model_estimations.txt'

with open('oov_words.txt', encoding='utf-8') as oov_opener:
    oov_words = oov_opener.read().split('\n')[:18]

with open(golden_standard_path, encoding='utf-8') as gs_opener:
    gs_pairs = gs_opener.read().split('\n')
    gs_normalized_estim = []

    for pair in gs_pairs:
        word_1, word_2, estim = pair.split('\t')
        if word_1 in oov_words or word_2 in oov_words:
            gs_normalized_estim.append(float(estim)/10)


def morph__model_estimation():
    with open(united_w2v_model_eval_path, encoding='utf-8') as morph_model_estim_opener:
        morph_model_estim_pairs = [float(line.split('\t')[-1]) for line in morph_model_estim_opener.read().split('\n')
                                   if line.split('\t')[-3] in oov_words or line.split('\t')[-2] in oov_words]

    print('corr with golden standard for moprh w2v is', spearmanr(morph_model_estim_pairs, gs_normalized_estim))

morph__model_estimation()


def fasttext_estimation():
    with open(fasttext_model_eval_path, encoding='utf-8') as fasttext_model_estim_opener:
        fasttext_model_estim_pairs = [float(line.split('\t')[-1]) for line in fasttext_model_estim_opener.read().split('\n')
                                    if line.split('\t')[-3] in oov_words or line.split('\t')[-2] in oov_words]

    print('corr with golden standard for fasttext w2v is', spearmanr(fasttext_model_estim_pairs, gs_normalized_estim))

fasttext_estimation()
