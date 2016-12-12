import numpy as np
import pyrenn
from sklearn.metrics.pairwise import cosine_similarity


class RNN(object):

    def __init__(self, training_sentences, training_labels):
        self._EMBED_EXCLUDE = ["the", "be", "to", "of", "and", "a", "in"]
        self._UNKNOWN_KEY = 'UUUNKKK'
        self._training_sentences = training_sentences
        self._training_labels = training_labels
        self._paragram_embeddings = self.load_paragram_embeddings()
        self._rnn = 0

    def test_rnn(self, test_sentences):
        test = self.assemble_input(test_sentences)

        return pyrenn.NNOut(test, self._rnn)

    def train_rnn(self):
        train = self.assemble_input(self._training_sentences)
        self._rnn = pyrenn.CreateNN([1, 2, 1], dIn=[0], dIntern=[1], dOut=[1, 2])
        self._rnn = pyrenn.train_LM(train, np.array(self._training_labels).reshape(1, -1), self._rnn, k_max=50, E_stop=5e-3)

        #shape = train.shape

        #self._rnn = pyrenn.CreateNN([shape[0], 50, 1], dIn=[0], dIntern=[1], dOut=[1, 2])
        #self._rnn = pyrenn.train_LM(train, np.array(self._training_labels), self._rnn, k_max=100, E_stop=1e-3)

    @staticmethod
    def load_paragram_embeddings():
        # load paragram phrase embeddings
        embeddings = {}

        # we create a dictionary: word => [embedding as numpy array]
        with open("paragram-phrase-XXL.txt", "r") as ins:
            for line in ins:
                spl = line.split(" ")

                word = spl[0]
                embed = np.array([float(i) for i in spl[1:]])
                embeddings[word] = embed

        return embeddings

    def generate_sentence_embedding(self, snt, word_embeds):
        # process period, apostrophe, comma tokens
        #     (leads to some improvement, especially on MSRvid)
        p_snt = snt.lower()
        p_snt = p_snt.replace(".", " . ")
        p_snt = p_snt.replace(",", "")
        p_snt = p_snt.replace("'", " '")

        tokens = p_snt.split(" ")

        embed = None

        # compute average embedding over all tokens
        for tk in tokens:
            # exclude common words
            if tk in self._EMBED_EXCLUDE:
                continue

            if tk in word_embeds:
                w_embed = np.copy(word_embeds[tk])
            else:
                w_embed = np.copy(word_embeds[self._UNKNOWN_KEY])

            if embed is None:
                embed = np.copy(w_embed)
            else:
                embed += w_embed

        embed /= float(len(tokens))

        return embed

    def assemble_input(self, sentences):

        samples = len(sentences)
        #features = self.generate_sentence_embedding(sentences[0][0], self._paragram_embeddings).reshape(1, -1).shape[1]
        #input_data = np.zeros((features, samples))

        calculated_similarity = []

        for i in xrange(0, samples):
            sentence = sentences[i]

            embed_s1 = self.generate_sentence_embedding(sentence[0], self._paragram_embeddings)
            embed_s1 = embed_s1.reshape(1, -1)

            embed_s2 = self.generate_sentence_embedding(sentence[1], self._paragram_embeddings)
            embed_s2 = embed_s2.reshape(1, -1)

            #input_data[:, i] = np.abs(embed_s1-embed_s2)
            calculated_similarity.append(cosine_similarity(embed_s1, embed_s2))

        calculated_similarity = np.array(calculated_similarity)
        calculated_similarity = calculated_similarity.flatten()

        return calculated_similarity

        #return input_data
