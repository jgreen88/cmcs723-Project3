import sys
import mtranslate.mtranslate.core as mtr
from embedding_manipulation import EmbeddingManipulation


# Get input file name and output file name from arguments.
input_file = sys.argv[1]
output_file = sys.argv[2]

# If the input file is for the multisource or news categories, use pre-translated files. Else translate the given file.
if 'multisource' in input_file:
    input_file = 'xling_test/STS.input.multisource-english.txt'
    english_sentences = [line.rstrip('\n').split('\t') for line in open(input_file)]
elif 'news' in input_file:
    input_file = 'xling_test/STS.input.news-english.txt'
    english_sentences = [line.rstrip('\n').split('\t') for line in open(input_file)]
else:
    # Obtain sentences in input file.
    sentences = [line.rstrip('\n').split('\t') for line in open(input_file)]

    # Will contain translated English sentences from Spanish.
    english_sentences = []

    # For every pair of sentences...
    for pair in sentences:
        english_pair = []   # Will contain a pair of translated English sentences.

        # For every sentence in pair...
        for sentence in pair:
            # Translate it from Spanish to English using mtranslate.
            english_pair.append(mtr.translate(sentence, 'en', 'es').encode('utf-8'))

        # Append the results.
        english_sentences.append(english_pair)

# ------------------------------------------------------------
# ------------------------------------------------------------
# Change this code to give different output into 'results'.

# Run the EmbeddingManipulation algorithm on our input sentences and score to get results.
model = EmbeddingManipulation(english_sentences)
results = model.perform_scoring()
# ------------------------------------------------------------
# ------------------------------------------------------------

# Create / open output file for writing to.
result_file = open(output_file, 'w')

# Print our scores into result_file.
for item in results:
    print>> result_file, item
