import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr
import nltk
import sys

PARAGRAM_PHRASE_FNAME = "paragram-phrase-XXL.txt"
PARAGRAM_SL999_FNAME = "paragram_300_sl999.txt"

def load_embeddings(fname):
    embeddings = {}
    
    file = open(fname)
    
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            spl = line.split(" ")
            
            word = spl[0]
            embed = np.array([float(i) for i in spl[1:]])
            embeddings[word] = embed
    
    file.close()
    
    return embeddings
   
    
    
phrase_embed = load_embeddings(PARAGRAM_PHRASE_FNAME)
#print "Phrase embeddings loaded."
sl999_embed = load_embeddings(PARAGRAM_SL999_FNAME)
#print "SL999 embeddings loaded."
embedding_set = [phrase_embed, sl999_embed]

# key for unknown tokens (in Paragram Phrase XXL)
UNKNOWN_KEY = 'UUUNKKK'
UNKNOWN_EMBED = phrase_embed[UNKNOWN_KEY]



def generate_sentence_embedding(snt, embeddings):
    # replace period, apostrophe, comma tokens
    p_snt = snt.lower()
    tokens = nltk.wordpunct_tokenize(p_snt)
    
    embed = None
    
    for tk in tokens:
        w_embed = None
        for e in embeddings:
            if (tk in e):
                w_embed = np.copy(e[tk])
                break
        if (w_embed is None):
            w_embed = np.copy(UNKNOWN_EMBED)
        
        if (embed is None):
            embed = np.copy(w_embed)
        else:
            embed += w_embed
    
    embed /= float(len(tokens))
    
    return embed



def compute_scores(inp_fname, out_fname):
    inp_file = open(inp_fname)
    inp_content = inp_file.readlines()
    inp_file.close()

    calculated_similarity = []
    for i in xrange(0, len(inp_content)):
        snts = inp_content[i].split("\t")

        embed_s1 = generate_sentence_embedding(snts[0], embedding_set)
        embed_s1 = embed_s1.reshape(1, -1)

        embed_s2 = generate_sentence_embedding(snts[1], embedding_set)
        embed_s2 = embed_s2.reshape(1, -1)

        calculated_similarity.append(cosine_similarity(embed_s1, embed_s2))

    calculated_similarity = np.array(calculated_similarity)
    calculated_similarity = calculated_similarity.flatten()

    np.savetxt(out_fname, calculated_similarity)







if (len(sys.argv) != 3):
    print "Wrong number of arguments!"
    exit()

inp_fname = sys.argv[1]
out_fname = sys.argv[2]

inp_file = open(inp_fname)
inp_content = inp_file.readlines()
inp_file.close()

calculated_similarity = []
for i in xrange(0, len(inp_content)):
    snts = inp_content[i].split("\t")
    
    embed_s1 = generate_sentence_embedding(snts[0], embedding_set)
    embed_s1 = embed_s1.reshape(1, -1)
    
    embed_s2 = generate_sentence_embedding(snts[1], embedding_set)
    embed_s2 = embed_s2.reshape(1, -1)
    
    calculated_similarity.append(cosine_similarity(embed_s1, embed_s2))

calculated_similarity = np.array(calculated_similarity)
calculated_similarity = calculated_similarity.flatten()

np.savetxt(out_fname, calculated_similarity)








