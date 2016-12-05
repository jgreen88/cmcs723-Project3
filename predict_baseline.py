import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats.stats import pearsonr
import sys

# exclude the top 10 most common English words from contributing
# to the embedding
#EMBED_EXCLUDE = ["the", "be", "to", "of", "and", "a", "in"]

# key for unknown tokens
UNKNOWN_KEY = 'UUUNKKK'



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



def generate_sentence_embedding(snt, word_embeds):
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
        #if (tk in EMBED_EXCLUDE): continue
            
        if (tk in word_embeds):
            w_embed = np.copy(word_embeds[tk])
        else:
            w_embed = np.copy(word_embeds[UNKNOWN_KEY])
        
        if (embed is None):
            embed = np.copy(w_embed)
        else:
            embed += w_embed
    
    embed /= float(len(tokens))
    
    return embed



if (len(sys.argv) != 3):
    print "Wrong number of arguments!"
    exit()

inp_fname = sys.argv[1]
out_fname = sys.argv[2]



paragram_embeddings = load_paragram_embeddings()

inp_file = open(inp_fname)
inp_content = inp_file.readlines()
inp_file.close()

calculated_similarity = []
for i in xrange(0, len(inp_content)):
    snts = inp_content[i].split("\t")
    
    embed_s1 = generate_sentence_embedding(snts[0], paragram_embeddings)
    embed_s1 = embed_s1.reshape(1, -1)
    
    embed_s2 = generate_sentence_embedding(snts[1], paragram_embeddings)
    embed_s2 = embed_s2.reshape(1, -1)
    
    calculated_similarity.append(cosine_similarity(embed_s1, embed_s2))

calculated_similarity = np.array(calculated_similarity)
calculated_similarity = calculated_similarity.flatten()

np.savetxt(out_fname, calculated_similarity)








