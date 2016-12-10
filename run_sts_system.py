import sys
import glob
import os
import gensim
from AveragingWord2Vec import AverageVectors


# Reads a newline separated, tab pair-wise separated txt file into a list of 2-element lists of sentence pairs.
def parse_sentences_from_data(file_name):
    return [line.split('\t') for line in open(file_name)]


# Flattens a list by one level.
def flatten(l):
    return [j for i in l for j in i]


# Reads a newline separated txt file of similarity scores into a list.
def parse_labels_from_data(file_name):
    return [float(line) for line in open(file_name)]


# Break sentence pairs in a training set into word lists for each pair.
def break_sentence_pairs_into_words(data):
    result = []                     # Holds our final result.

    # Go through every sentence pair...
    for pair in data:
        word_list = []              # Holds the list of words for each sentence in pair.

        # Go through both of the sentences in pair...
        for sentence in pair:
            # Split sentence into words and append them to word list.
            word_list.append(sentence.split())

        result.append(word_list)    # Append the word lists to result.

    return result


# Save scores to a given file.
def save_results(file_name, scores):
    result_file = open(file_name, 'w')

    for item in scores:
        print>> result_file, item


# Obtain all gold standard scores in a directory.
def get_gold_standard(directory_name):
    # The labels to return.
    labels = []

    # Save current working directory and switch to the one with data.
    cwd = os.getcwd()
    os.chdir("train/" + directory_name)

    # Append every label file to training labels.
    for filename in glob.glob('STS.gs.*.txt'):
        labels.append(parse_labels_from_data(filename))

    # Go back to the current working directory.
    os.chdir(cwd)

    return labels


# Obtain all sentence pairs in a directory for data.
def get_input_sentences(directory_name):
    # The sentences to return.
    sentences = []

    # Save the current working directory and go to the one with data.
    cwd = os.getcwd()
    os.chdir("train/" + directory_name)

    # Append every label file to training labels.
    for filename in glob.glob('STS.input.*.txt'):
        sentences.append(parse_sentences_from_data(filename))

    # Go back to the current working directory.
    os.chdir(cwd)

    return sentences


# Sets up the google model for word2vec/
def set_up_google_word2vec():
    # Load saved model (GoogleWord2VecModel), or read and generate/save this model from the bin file.
    if os.path.exists(os.getcwd() + '/GoogleWord2VecModel'):
        google_model = gensim.models.Word2Vec.load(os.getcwd() + '\\GoogleWord2VecModel', mmap='r')
    elif os.path.exists(os.getcwd() + '/GoogleNews-vectors-negative300.bin'):
        google_model = gensim.models.Word2Vec.load_word2vec_format(os.getcwd() + '\\GoogleNews-vectors-negative300.bin',
                                                                   binary=True)
        google_model.init_sims(replace=True)
        google_model.save('GoogleWord2VecModel')
    else:
        print "Error: Did not detect Google word2vec data in project directory, please download!"
        return False

    return google_model


# Get the string of the algorithm to use and series of strings for the training set directories to use.
algorithm = sys.argv[1]
training_dirs = sys.argv[2:]

# Stores the training and test sentence pairs and gold standard scores.
training_set = []
training_labels = []
test_set = []
test_labels = []

# For every training directory...
for directory in training_dirs:
    training_set.append(get_input_sentences(directory))
    training_labels.append(get_gold_standard(directory))

# Flatten training set and labels for every directory into a single list of lists.
training_set = flatten(flatten(training_set))
training_labels = flatten(flatten(training_labels))

# Get test data.
test_set.append(get_input_sentences('STS2012-en-train'))
test_labels.append(get_gold_standard('STS2012-en-train'))

# Flatten training set and labels for every directory into a single list of lists.
test_set = flatten(flatten(test_set))
test_labels = flatten(flatten(test_labels))

# Choose which algorithm to use. Add more elseifs to use more algorithms.
if algorithm == 'Averaging':
    model = set_up_google_word2vec()

    if not model:
        print "Run Failed!"
        sys.exit()

    # Break sentences into words to prep for AveragingWord2Vec.
    test_words = break_sentence_pairs_into_words(test_set)

    # Instantiate instance of AverageVectors and compute similarity scores.
    ave = AverageVectors(test_words, model)
    ave.generate_average_vectors()
    ave.compute_similarity_scores()

    # Save these results.
    save_results('results_average.txt', ave.get_similarities())
elif algorithm == 'Blah':
    print "Add another algorithm."


# Save the gold standard scores.
save_results('gold_standard.txt', test_labels)

print "Done"
