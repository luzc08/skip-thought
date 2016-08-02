import os.path
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import *
import re
import string

# preprocessed all the raw text

dir_path = '/data2/luzhc/raw_text/'
target_path = '/data2/luzhc/pre_processed_text/'

stemmer = PorterStemmer()
p = re.compile(ur'\[[\,\-\s\d]*\]')

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


def process_raw_text(filename):
    conf_name = filename.split('.')[-2]
    f_name = os.path.join(dir_path, filename)
    f = open(target_path+conf_name+'.txt', "a+")
    print 'processing', f_name
    if not os.path.isfile(f_name):
        return
    for line in open(f_name):
        sentences = sent_tokenize_text(line)
        for t_sent in sentences:
            sent = re.sub(p, '', t_sent)
            tokens = word_tokenize(sent)
            tokens = [i.lower() for i in tokens if i not in string.punctuation]
            stems = stem_tokens(tokens, stemmer)
            new_line = ' '.join(stems)
            # new_line = ' '.join(tokens)
            f.write(new_line+'\n')
            #return stems
    f.close()

folders = os.listdir(dir_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

t_folders = os.listdir(target_path)

for filename in folders:
    process_raw_text(filename)
