from scipy.stats import spearmanr

golden_standard_path = 'golden_standard_final.txt'
morph_model_eval_path = 'morpho_w2v_estimations.txt'

with open(golden_standard_path, encoding='utf-8') as gs_opener:
    gs_pairs = gs_opener.read().split('\n')
    gs_normalized_estim = []

    for pair in gs_pairs:
        word_1, word_2, estim = pair.split('\t')
        gs_normalized_estim.append(float(estim)/10)

with open(morph_model_eval_path, encoding='utf-8') as model_estim_opener:
    model_estim_pairs = [float(line.split('\t')[-1]) for line in model_estim_opener.read().split('\n')]

print(spearmanr(model_estim_pairs, gs_normalized_estim))
