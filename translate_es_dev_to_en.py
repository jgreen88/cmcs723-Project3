import mtranslate.mtranslate.core as mtr
import os.path

translated_file = 'xling_dev/STS.input.crosslingual-trial-english.txt'

if not os.path.isfile(translated_file):
    input_file = 'xling_dev/STS.input.crosslingual-trial.txt'
    sentences = [line.rstrip('\n').split('\t') for line in open(input_file)]

    english_sentences = []

    for pair in sentences:
        english_pair = []

        for sentence in pair:
            english_pair.append(mtr.translate(sentence, 'en', 'es').encode('utf-8'))

        english_sentences.append(english_pair)

    output_file = open(translated_file, 'w')

    for pair in english_sentences:
        print>> output_file, '\t'.join(pair)
