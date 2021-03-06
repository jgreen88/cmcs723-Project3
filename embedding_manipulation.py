import numpy as np
import nltk
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords, wordnet


class EmbeddingManipulation(object):

    def __init__(self, sentences):
        #self._EMBED_EXCLUDE = ["the", "be", "to", "of", "and", "a", "in"]
        self._EMBED_EXCLUDE = stopwords.words('english')
        self._UNKNOWN_KEY = 'UUUNKKK'
        self._sentences = sentences

    def load_paragram_embeddings(self):
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

    def generate_sentence_embedding(self, snt, word_embeds, stop_list=True):
        # process period, apostrophe, comma tokens
        #     (leads to some improvement, especially on MSRvid)
        p_snt = snt.lower()
        p_snt = p_snt.replace(".", " . ")
        p_snt = p_snt.replace(",", "")
        p_snt = p_snt.replace("'", " '")
        p_snt = p_snt.replace(":", "")
        p_snt = p_snt.replace(";", "")
        p_snt = p_snt.replace("?", " QUESTION_TOKEN")
        p_snt = p_snt.replace("&", " and ")
        #p_snt = p_snt.replace("(", "")
        #p_snt = p_snt.replace(")", "")
        #p_snt = p_snt.replace("$", "dollars ")

        tokens = p_snt.split(" ")

        pos_tags_raw = nltk.pos_tag(nltk.tokenize.word_tokenize(p_snt.decode("utf-8")))
        pos_tags = []

        for tag in pos_tags_raw:
            pos_tags.append((tag[0], self.get_wordnet_pos(tag[1])))

        embed = None

        # compute average embedding over all tokens
        for tk in tokens:
            tk = tk.lower()

            #try:
            #    tk = self.num2words(int(tk))
            #except ValueError:
            #    pass

            # exclude common words
            if (stop_list and tk in self._EMBED_EXCLUDE): continue

            if (tk in word_embeds):
                w_embed = np.copy(word_embeds[tk])
            elif tk.isalpha() and wordnet.synsets(tk, pos=self.get_pos(tk, pos_tags), lang='eng'):
                w_embed = self.find_synonyms(wordnet.synsets(tk, pos=self.get_pos(tk, pos_tags), lang='eng'),
                                             word_embeds)
            else:
                w_embed = np.copy(word_embeds[self._UNKNOWN_KEY])

            if (embed is None):
                embed = np.copy(w_embed)
            else:
                embed += w_embed

        if embed == None:
            embed = self.generate_sentence_embedding(snt, word_embeds, stop_list=False)
        else:
            embed /= float(len(tokens))

        return embed

    def perform_scoring(self):

        paragram_embeddings = self.load_paragram_embeddings()

        calculated_similarity = []
        for i in xrange(0, len(self._sentences)):
            snts = self._sentences[i]

            embed_s1 = self.generate_sentence_embedding(snts[0], paragram_embeddings)
            embed_s1 = embed_s1.reshape(1, -1)

            embed_s2 = self.generate_sentence_embedding(snts[1], paragram_embeddings)
            embed_s2 = embed_s2.reshape(1, -1)

            calculated_similarity.append(cosine_similarity(embed_s1, embed_s2))

        calculated_similarity = np.array(calculated_similarity)
        calculated_similarity = calculated_similarity.flatten()

        return calculated_similarity

    def find_synonyms(self, synonyms_set, word_embeds):
        for synset in synonyms_set:
            for lemma in synset.lemmas():
                if lemma.name() in word_embeds:
                    return np.copy(word_embeds[lemma.name()])

        return np.copy(word_embeds[self._UNKNOWN_KEY])

    def get_wordnet_pos(self, treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def get_pos(self, tk, pos_tags):
        for tag in pos_tags:
            if tag[0] == tk:
                return tag[1]

    @staticmethod
    def num2words(num, join=True):
        '''words = {} convert an integer number into words'''
        units = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        teens = ['', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', \
                 'seventeen', 'eighteen', 'nineteen']
        tens = ['', 'ten', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', \
                'eighty', 'ninety']
        thousands = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', \
                     'quintillion', 'sextillion', 'septillion', 'octillion', \
                     'nonillion', 'decillion', 'undecillion', 'duodecillion', \
                     'tredecillion', 'quattuordecillion', 'sexdecillion', \
                     'septendecillion', 'octodecillion', 'novemdecillion', \
                     'vigintillion']
        words = []
        if num == 0:
            words.append('zero')
        else:
            numStr = '%d' % num
            numStrLen = len(numStr)
            groups = (numStrLen + 2) / 3
            numStr = numStr.zfill(groups * 3)
            for i in range(0, groups * 3, 3):
                h, t, u = int(numStr[i]), int(numStr[i + 1]), int(numStr[i + 2])
                g = groups - (i / 3 + 1)
                if h >= 1:
                    words.append(units[h])
                    words.append('hundred')
                if t > 1:
                    words.append(tens[t])
                    if u >= 1: words.append(units[u])
                elif t == 1:
                    if u >= 1:
                        words.append(teens[u])
                    else:
                        words.append(tens[t])
                else:
                    if u >= 1: words.append(units[u])
                if (g >= 1) and ((h + t + u) > 0): words.append(thousands[g] + ',')
        if join: return ' '.join(words)
        return words
