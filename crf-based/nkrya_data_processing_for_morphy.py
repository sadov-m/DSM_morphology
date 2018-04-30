import time

#making data for crf supervised morpho-segmentation model
start_time = time.time()

with open('data_for_morph.txt', 'w', encoding='utf-8') as writer: # output file

    resulting_string = ''
    with open('data.txt', encoding='utf-8') as reader:  # input json file

        i = 0
        for linea in reader:
            words = linea.split(' ')

            resulting_string += '\n'.join(words) + '\n' + '//'
            i += 1

            if i%100000 == 0:
                writer.write(resulting_string)
                print("Elapsed time for 100 thousand sents: {:.3f} sec".format(time.time() - start_time))
                resulting_string = ''
