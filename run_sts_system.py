import sys
import glob
import os
import string
import gensim
from averaging_word2vec import AverageVectors
from embedding_manipulation import EmbeddingManipulation
from rnn import RNN


# Reads a newline separated, tab pair-wise separated txt file into a list of 2-element lists of sentence pairs.
def parse_sentences_from_data(file_name):
    return [line.rstrip('\n').split('\t') for line in open(file_name)]


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
    result_file = open(modifier + file_name, 'w')

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
if len(sys.argv) > 1:
    algorithm = sys.argv[1]
else:
    # Default algorithm.
    algorithm = 'Averaging'

# If user specified directories as argument, use those, otherwise use whole training set.
if len(sys.argv) > 2:
    training_dirs = sys.argv[2:]
else:
    training_dirs = ['STS2012-en-test', 'STS2013-en-test', 'STS2014-en-test', 'STS2015-en-test']

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

# Modifies file names to designate Spanish versions (if needed).
modifier = 'spanish_'

# Check if we are using the Spanish translated test set or the normal English one...
if "Spanish" in algorithm:
    # Remove the Spanish portion from algorithm to handle if statements for algorithms.
    algorithm = string.replace(algorithm, 'Spanish', '')

    # Parse pre-translated sentences and scores for them.
    test_set = parse_sentences_from_data('xling_dev/STS.input.crosslingual-trial-english.txt')
    test_labels = parse_labels_from_data('xling_dev/STS.gs.crosslingual-trial.txt')
else:
    # Don't use Spanish modifier for save file.
    modifier = ''

    # Get test data.
    test_set.append(get_input_sentences('STS2012-en-train'))
    test_labels.append(get_gold_standard('STS2012-en-train'))

    # Flatten training set and labels for every directory into a single list of lists.
    test_set = flatten(flatten(test_set))
    test_labels = flatten(flatten(test_labels))

# Choose which algorithm to use. Add more elseifs to use more algorithms.
if algorithm == 'AveragingW2V':
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
elif algorithm == 'EmbeddingManipulation':
    model = EmbeddingManipulation(test_set)

    save_results('results_embeddings.txt', model.perform_scoring())
elif algorithm == 'RNN':
    model = RNN(training_set, training_labels)

    model.train_rnn()
    save_results('results_rnn.txt', model.test_rnn(test_set))


# Save the gold standard scores.
save_results('gold_standard.txt', test_labels)

# Below used only to get single file for all testing data under STS2012-en-train. Labels are in gold_standard.txt.
#for i, pair in enumerate(test_set):
#    test_set[i] = "\t".join(test_set[i])
#save_results('train/STS2012-en-train/all_test_data.txt', test_set)
