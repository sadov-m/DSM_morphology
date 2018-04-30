
with open(r'crf_processed_data/supervised_train_data', encoding='utf-8') as file:
    with open(r'trial_data.txt', 'w', encoding='utf-8') as output:
        i = 0
        sents = []
        sent = []

        for line in file:

            target_form = line.strip().split('\t')[1]
            if target_form == '//':
                if sent:
                    sents.append(' <s> '.join(sent))
                    sent = []
            else:
                sent.append(target_form)

            if len(sents) > 500:
                output.write('\n'.join(sents))
                sents = []
