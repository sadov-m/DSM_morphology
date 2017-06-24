from scipy.stats import spearmanr

golden_standard_path = 'golden_standard_final.txt'
morph_model_eval_path = 'morpho_w2v_estimations.txt'
fasttext_model_eval_path = 'C:/Users/Ольга/PycharmProjects/DSM_morphology/fasttext/fasttext_w2v_estimations.txt'
regular_w2v_model_eval_path = 'C:/Users/Ольга/PycharmProjects/DSM_morphology/classic_w2v_estimations.txt'

with open(golden_standard_path, encoding='utf-8') as gs_opener:
    gs_pairs = gs_opener.read().split('\n')
    gs_normalized_estim = []

    for pair in gs_pairs:
        word_1, word_2, estim = pair.split('\t')
        gs_normalized_estim.append(float(estim)/10)


def morph__model_estimation():
    with open(morph_model_eval_path, encoding='utf-8') as morph_model_estim_opener:
        morph_model_estim_pairs = [float(line.split('\t')[-1]) for line in morph_model_estim_opener.read().split('\n')]

    print('corr with golden standard for moprh w2v is', spearmanr(morph_model_estim_pairs, gs_normalized_estim))

morph__model_estimation()


def fasttext_estimation():
    with open(fasttext_model_eval_path, encoding='utf-8') as fasttext_model_estim_opener:
        fasttext_model_estim_pairs = [float(line.split('\t')[-1]) for line in fasttext_model_estim_opener.read().split('\n')]

    print('corr with golden standard for fasttext w2v is', spearmanr(fasttext_model_estim_pairs, gs_normalized_estim))

fasttext_estimation()


def regular_model_estimation():
    with open(regular_w2v_model_eval_path, encoding='utf-8') as regular_w2v_model_estim_opener:
        lines = regular_w2v_model_estim_opener.read().split('\n')
        regular_w2v_model_estim_pairs = []

        for line in lines:

            try:
                regular_w2v_model_estim_pairs.append(float(line.split('\t')[-1]))

            except ValueError:
                regular_w2v_model_estim_pairs.append('na')

    print('corr with golden standard for regular w2v is', spearmanr(regular_w2v_model_estim_pairs, gs_normalized_estim, nan_policy='omit'))

regular_model_estimation()
