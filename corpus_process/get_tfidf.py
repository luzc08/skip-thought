# run tf-idf on preprocessed data

import os.path
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import *
from nltk.corpus import stopwords
import re
import string
from collections import Counter
# from pre_process_para import stem_tokens,sent_tokenize_text
import cPickle as pickle
from sklearn.feature_extraction.text import TfidfVectorizer

data_path = '/data2/luzhc/raw_text/'

target_path = '/data2/luzhc/tfidf/'

token_dict = {}

all_tokens = []

p = re.compile(ur'\[[\,\-\s\d]*\]')

stemmer = PorterStemmer()

# cnt = 0

def stem_tokens(tokens, stemmer):
   stemmed = []
   for item in tokens:
       stemmed.append(stemmer.stem(item))
   return stemmed


def sent_tokenize_text(line):
    #sentences = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    #for t in line:
        #sents = sent_detector.tokenize(t)
    sentences = sent_detector.tokenize(line)
    return sentences

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems

def collect_text(filename):
    f_name = os.path.join(data_path, filename)
    print 'processing', f_name
    # tokens = []
    if not os.path.isfile(f_name):
        return []

    with open(f_name, 'r') as text_file:
        text = text_file.read()
        lowers = text.lower()
        lowers1 = re.sub(p, '', lowers)
            # remove the punctuation using the character deletion step of translate
        no_punctuation = lowers1.translate(None, string.punctuation)
        # tokens = nltk.word_tokenize(no_punctuation)
        return no_punctuation
    # for line in open(f_name):
    #     print line
    #     sentences = sent_tokenize_text(line)
    #     for t_sent in sentences:
    #         # cnt += 1
    #         sent = re.sub(p, '', t_sent)
    #         tokens = word_tokenize(sent)
    #         tokens = [i.lower() for i in tokens if i not in string.punctuation]
    #         stems = stem_tokens(tokens, stemmer)
            # if cnt%10 == 0:
            #     print stems

    # tokens = tokens + stems
    # return tokens
            # all_tokens = all_tokens + stems
            # new_line = ' '.join(stems)
            # new_line = ' '.join(tokens)
            # f.write(new_line + '\n')
    # f = open(target_path + conf_name + '.txt', "a+")
folders = os.listdir(data_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

t_folders = os.listdir(target_path)

for filename in folders:
    token_dict[filename] = collect_text(filename)
    if filename=="CHI2015":
        print token_dict[filename]
    # tmp = collect_text(filename)
    # if tmp:
    #     all_tokens = all_tokens + tmp

print "all tokens got!"
tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
tfs = tfidf.fit_transform(token_dict.values())

pickle.dump( token_dict, open( target_path+"token_dict.p", "wb" ) )
pickle.dump( tfs, open( target_path+"tfidf.p", "wb" ) )

feature_names = tfidf.get_feature_names()
print feature_names
# count = Counter(all_tokens)
# print count.most_common(100)