# DSM_morphology
Course paper project dedicated to a research of usage of morphology in distributional semantics models (DSM). All the scripts except the one that is situated in the folder called "fasttext" were written using python 3.6 on Windows 7 OS. The code in the folder "fasttext" was written for python 2.7 version on Ubuntu 14.04 OS.

## Code

### Processing
nkrya_data_processing.py - a script to extract sentences from Russian National Corpora (RNC) processed by Mystem in json format

### Building models (DSMs and Morfessor)
word2vec_classic_build.py - creation of a DSM using the SkipGram algorithm where target elements of a model are words by means of gensim

word2vec_classic_check.py - retrieval of estimations for word pairs from a golden standard

word2vec_with_morfessor_build.py and word2vec_with_morfessor_check.py serve the same purposes as two previous scripts accordingly but using parts of words and spaces as target elements of a model

fasttext/fasttext_approach.py - creation of a DSM using the SkipGram algorithm by means of fasttext and estimations retrieval take place in the same script

morfessor/morfessor_models_build.py - creation of a Morfessor model for words segmentation; the output received from the model was then used to obtain words segmentations for creating the DSM in word2vec_with_morfessor_build.py

morfessor/morfessor_models_check.py - a script used only for testing the Morfessor model

### Golden standard creation
golden_standard_creation.py - a script to retrieve rare and multi-morphemic words from RNC for creation of the golden standard

### Evaluation
krippendorff_alpha.py - a script to measure inter-annotator agreement in terms of Krippendorff's alpha; borrowed from Thomas Grill https://github.com/grrrr/krippendorff-alpha

model_performance_measurement.py - a script for estimating the performance of all the DSMs built in terms of two different metrics: Krippendorff's alpha and rho-value (Spearman's correlation)

## Files

### Models
morfessor/log_tokens and morfessor/types - two different Morfessor models for words segmentation

DSM created in word2vec_classic_build.py - https://drive.google.com/file/d/0B60o6LzcMfuBeDVnaFZLVHJzVTQ/view?usp=sharing

DSM created in morfessor/morfessor_models_build.py - https://drive.google.com/file/d/0B60o6LzcMfuBMVQxRDNRR0UxZXM/view?usp=sharing

DSM created in fasttext/fasttext_approach.py - http://ltr.uio.no/~andreku/data/trained_model.tgz

### Golden standard (for measuring DSMs performance)
morfesssor/golden_standard.csv - the file that holds manually annotated golden standard, all the estimations for all word pairs

morfessor/golden_standard_final.txt - the file that holds manually annotated golden standard, only the average estimation for all word pairs

morfessor/pre_golden_standard - the file that holds not annotated golden standard

morfessor/words_paired_annotated_by_me.txt - the golden standard manually annotated by me, the author

morfessor/Инструкция для разметки.docx - instruction for annotators of the golden standard

### Golden standard estimations
morfessor/words_estimated_by_ruwikiruscorpora - estimations for a golden standard retrieved from DSM available at (http://rusvectores.org/ru/)

morfessor/morpho_w2v_estimations.txt - estimations for a golden standard retrieved from DSM created in morfessor/morfessor_models_build.py

fasttext/fasttext_w2v_estimations.txt - estimations for a golden standard retrieved from DSM created in fasttext/fasttext_approach.py

classic_w2v_estimations.txt - estimations for a golden standard retrieved from DSM created in word2vec_classic_build.py

## Comments and details
available upon request - I am available at mikeabyrvalg5@gmail.com
