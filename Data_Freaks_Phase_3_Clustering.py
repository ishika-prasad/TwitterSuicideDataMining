import re
import copy
import math
import pandas as pd
import random


regex_str = [
    r'<[^>]+>',
    r'(?:@[\w_]+)',
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
    r"(?:[a-z][a-z'\-_]+[a-z])",
    r'(?:[\w_]+)',
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token.lower() for token in tokens]
    return tokens


# defining the Jaccard distance
def jaccard(a,b):
    inter = list(set(a) & set(b))
    I = len(inter)
    union = list(set(a) | set(b))
    U = len(union)
    return round(1-(float(I)/U), 4)


# k-means implementation
def kmeans(id, centroids, terms_all, l, k):
    count = 0
    for h in range(10):
        count = count + 1
        indices = [id.index(item) for item in centroids]
        cen_txt = [terms_all[x] for x in indices]
        cluster = []
        for i in range(l):
            d = [jaccard(terms_all[i], cen_txt[j]) for j in range(k)]
            ans = d.index(min(d))
            cluster.append(ans)
        # print cluster

        centroids1 = up_date(id, cluster, terms_all, l, k)
        sum = 0
        for i in range(k):
            if centroids1[i] == centroids[i]:
                sum = sum + 1
        if sum == k:
            break
        centroids = copy.deepcopy(centroids1)

    output(cluster, k, id)
    sse(cluster, centroids, terms_all, k, l)
    f.close()


def output(cluster, k, id):
    final = []
    for i in range(k):
        final.append([j for j, u in enumerate(cluster) if u == i])
        t = [x for x in final[i]]
        print(i+1, [id[x] for x in t])


def sse(cluster, centroids, terms_all, k, l):
    indices1 = []
    indices = [id_list.index(item) for item in centroids]
    cen_txt = [terms_all[x] for x in indices]
    sum_error = 0
    for i in range(k):
        indices1.append([j for j, u in enumerate(cluster) if u == i])
        t = [terms_all[x] for x in indices1[i]]
        for j in range(len(indices1[i])):
            sum_error = sum_error + math.pow(jaccard(t[j], cen_txt[i]), 2)


# updatin gthe centroids at every iteration
def up_date(id, cluster, terms_all, l, k):
    indices = []
    new_centxt_index = []
    new_centroid = []
    for i in range(k):
        indices.append([j for j, u in enumerate(cluster) if u == i])
        m = indices[i]
        # print m
        # m gives the indices if the elements of every cluster k

        if len(m) != 0:
            txt = [terms_all[p] for p in m]
            sim = [[jaccard(txt[i], txt[j]) for j in range(len(m))] for i in range(len(m))]
            f1 = [sum(i) for i in sim]
        new_centxt_index.append(m[(f1.index(min([sum(i) for i in sim])))])
    new_centroid = [id[x] for x in new_centxt_index]
    return new_centroid


terms_all = []

dfs = pd.read_excel('sentiment212.xlsx')
new_df = dfs.dropna()

text_list = new_df['text'].tolist()
id_list = new_df['id'].tolist()


for line in text_list:
    tokens = preprocess(line)
    terms_all.append([term for term in tokens])


l = len(terms_all)

random.seed(10)
initial_centroids = random.sample(id_list, 10)

with open('Intial_centroids.txt', 'w') as filehandle:
    for centroids in initial_centroids:
        filehandle.write('%s\n' % centroids)
cent = []
text_file = open('Intial_centroids.txt', "r")
centroids = text_file.read().split('\n')

for x in centroids:
    if x != '':
        cent.append(int(x))

k = 6
f = open("output.txt", 'w')
kmeans(id_list, cent, terms_all,l,k)


