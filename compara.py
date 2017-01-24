import re

__author__ = 'dnul'


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.preprocessing import normalize
import numpy as np


import glob

def representation(indices,dictionary,vector):
    for i in range(len(indices)):
        print(dictionary[indices[i]],vector[0,indices[i]])


def close_documents(distance_vector,corpus):
    closest = np.array(distance_vector).argsort()
    for value in closest[0:5]:
        print(corpus[value])


def max_n(row_data, row_indices, n):
        i = row_data.argsort()[-n:]
        # i = row_data.argpartition(-n)[-n:]
        top_values = row_data[i]
        top_indices = row_indices[i]  # do the sparse indices matter?
        return top_values, top_indices, i

def parse_double_utf8(txt):
    def parse(m):
        try:
            return m.group(0).encode('latin1').decode('utf8')
        except UnicodeDecodeError:
            return m.group(0)
    return re.sub(u'[\xc2-\xf4][\x80-\xbf]+', parse, txt)


corpus=[]
onlyfiles = glob.glob('./noticias/*.txt')
stopwords = parse_double_utf8(open('stopwords.txt','r').read()).splitlines()

for file in onlyfiles:
    content = open(file,'r').read()
    print(file)
    corpus=corpus+[content]

vectorizer = TfidfVectorizer(min_df=1,max_features=200,stop_words=stopwords)
X = vectorizer.fit_transform(corpus)
idf = vectorizer.idf_
#print(dict(zip(vectorizer.get_feature_names(), idf)))
#print(len(vectorizer.get_feature_names()))

print(idf)

#print(X[0])
#print(cosine_similarity(X[0],X[1]))
#print(euclidean_distances(X[0],X[1]))
#print(euclidean_distances(X[1],X[1]))
#print(cosine_similarity(X[1],X[1]))
distances = pairwise_distances(X,metric='cosine')
for i,row in enumerate(distances):
    print('-------\n')
    indices = np.array(X[i])
    print(i,corpus[i])
    arr_ll=X[i].tolil()
    top_values,top_indices,wtf = max_n(np.array(arr_ll.data[0]),np.array(arr_ll.rows[0]),10)
    #print('top values',top_values,'top indices',top_indices)
    representation(top_indices,vectorizer.get_feature_names(),X[i])
    close_documents(row,corpus)
    print('-------\n')
    #print(X[i])
    #print(row)
    #row[i]=0
    #print(max(row))
    #print(min(row))

#closest = pairwise_distances_argmin(X[5],X[6,:],metric='cosine')
