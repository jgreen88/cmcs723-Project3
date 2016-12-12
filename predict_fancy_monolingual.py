import sys
from embedding_manipulation import EmbeddingManipulation


# Get input file name and output file name from arguments.
input_file = sys.argv[1]
output_file = sys.argv[2]

# Parse the input sentences into a list of pairs of sentences.
input_sentences = [line.rstrip('\n').split('\t') for line in open(input_file)]

# ------------------------------------------------------------
# ------------------------------------------------------------
# Change this code to give different output into 'results'.

# Run the EmbeddingManipulation algorithm on our input sentences and score to get results.
model = EmbeddingManipulation(input_sentences)
results = model.perform_scoring()
# ------------------------------------------------------------
# ------------------------------------------------------------

# Create / open output file for writing to.
result_file = open(output_file, 'w')

# Print our scores into result_file.
for item in results:
    print>> result_file, item
