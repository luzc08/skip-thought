from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model1 = word2vec.Word2Vec.load_word2vec_format('/data2/luzhc/GoogleNews-vectors-negative300.bin', binary=True)
model2 = word2vec.Word2Vec.load('/data2/luzhc/w2v_data/test.model')
model3 = word2vec.Word2Vec.load('/data2/luzhc/w2v_data/mixed.model')

#model.accuracy('word2vec_model/q_w.txt')
#model.accuracy('word2vec_model/q_p.txt')

print model1.most_similar(['tangible', 'interaction'], ['hardware'], topn=10)
print model2.most_similar(['tangible', 'interaction'], ['hardware'], topn=10)
print model3.most_similar(['tangible', 'interaction'], ['hardware'], topn=10)

#print model.doesnt_match("breakfast cereal dinner lunch".split())