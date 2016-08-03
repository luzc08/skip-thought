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

data_path = '/data2/luzhc/raw_text/'

target_path = '/data2/luzhc/tfidf/'

all_tokens = []

p = re.compile(ur'\[[\,\-\s\d]*\]')

stemmer = PorterStemmer()

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

# cnt = 0

def collect_text(filename):
    f_name = os.path.join(data_path, filename)
    print f_name + ' ? '
    # print 'processing', f_name
    # all_tokens = []
    if not os.path.isfile(f_name):
        return []

    with open(f_name, 'r') as text_file:
        text = text_file.read()
        lowers = text.lower()
        lowers1 = re.sub(p, '', lowers)
        # remove the punctuation using the character deletion step of translate
        no_punctuation = lowers1.translate(None, string.punctuation)
        tokens = nltk.word_tokenize(no_punctuation)
        return tokens
    # for line in open(f_name):
    #     #print line
    #     sentences = sent_tokenize_text(line)
    #     for t_sent in sentences:
    #         # cnt += 1
    #         sent = re.sub(p, '', t_sent)
    #         tokens = word_tokenize(sent)
    #         tokens = [i.lower() for i in tokens if i not in string.punctuation]
    #         stems = stem_tokens(tokens, stemmer)
    #         # if cnt%10 == 0:
    #         #     print stems
    #         all_tokens = all_tokens + stems


    # return all_tokens
            # all_tokens = all_tokens + stems
            # new_line = ' '.join(stems)
            # new_line = ' '.join(tokens)
            # f.write(new_line + '\n')
    # f = open(target_path + conf_name + '.txt', "a+")
# folders = os.listdir(data_path)

# if not os.path.exists(target_path):
#     os.makedirs(target_path)

# t_folders = os.listdir(target_path)
all_tokens = collect_text('CHI2015.txt')

# print all_tokens
# for filename in folders:
#     tmp = collect_text(filename)
#     if tmp:
#         all_tokens = all_tokens + tmp

pickle.dump( all_tokens, open( target_path+"tokens.p", "wb" ) )
count = Counter(all_tokens)
print count.most_common(100)