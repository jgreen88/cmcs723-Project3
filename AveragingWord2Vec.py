import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict


class AverageVectors(object):

    def __init__(self, words, model):
        self._words = words
        self._model = model
        self._average_vectors_generated = False
        self._average_vectors = []
        self._cosine_similarity = []
        self._similarity = []

    def get_similarities(self):
        return self._cosine_similarity

    def compute_similarity_scores(self):
        if not self._average_vectors_generated:
            self.generate_average_vectors()

        for pair in self._average_vectors:
            self._cosine_similarity.append(5*cosine_similarity(pair[0].reshape(1, -1), pair[1].reshape(1, -1))[0][0])

    def generate_average_vectors(self):
        model = self._model
        words = self._words
        length = len(model['hello'])

        for pair in words:
            average_pair = []

            for word_list in pair:
                average = np.zeros(length)

                for word in word_list:
                    if word in model.vocab:
                        average += model[word]

                average_pair.append(average/len(word_list))

            self._average_vectors.append(average_pair)

        self._average_vectors_generated = True
