import os
import sys
import Stemmer
import json
import re
from math import log2, log10
import threading
from time import time, sleep

lock = threading.Lock()
result = {}
token_map = {}
flag_map = {'title': 128, 'infobox': 64, 'categories': 32, 'links': 16, 'references': 8, 'body': 4}
toks = []
w = [0.2, 0.17, 0.14, 0.11, 0.08, 0.05]
f_p = 0
s_p = False
tf = []
print('Loading Modules...\n')
for i in range(4):
    with open('./titles/real_result_{}'.format(i)+'.json') as o:
        tf.append(json.load(o))
print('Modules Loaded\n')
id_set = set()
title_id = []
locations = {}
vals = []
path_to_index = sys.argv[1]
file_path = sys.argv[2]
n_records = 15

stopwords= ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've",\
            "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', \
            'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their',\
            'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', \
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', \
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', \
            'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after',\
            'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',\
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',\
            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than', 'too', 'very', \
            's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', \
            've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn',\
            "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn',\
            "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", \
            'won', "won't", 'wouldn', "wouldn't", \
            'infobox', 'category', 'title', 'body', 'links', 'link', 'references', 'html', 'xml', 'url', 'https', 'http', 'www', \
            'web', 'com', 'co', 'org', 'cfm', 'edu', 'refbegin', 'reflist', 'refend', 'cite', 'bibliography', 'notes', 'gt', 'lt'\
            'ref', 'quote']

ps = Stemmer.Stemmer('english')

def decode_int(s):
    b = b''
    flag = ord(s[0])
    cat_lists = []
    b += (flag&3).to_bytes(1, 'big')
    for i in range(1, len(s)):
        b += ord(s[i]).to_bytes(1, 'big')
    for key in flag_map.keys():
        if flag_map[key]&flag == flag_map[key]:
            cat_lists.append(7 - int(log2(flag_map[key])))
    return int.from_bytes(b, 'big'), sorted(cat_lists, reverse=True)

def find_loc(i):
    l = [18000000, 35000000, 53000000, 70000000]
    for j in range(len(l)):
        if l[j] > i:
            return j

def lookup(ele):
    global id_set
    global f_p
    loc_s = {}
    di = ele[0]
    pos = 0
    r_s = set()
    with open(path_to_index+'/'+di+'/sec.txt','r',encoding='utf-8') as o:
        for line in o:
            if ele == line:
                with open(path_to_index+'/'+di+'/'+di+'_'+str(pos-1)+'.txt', 'r', encoding='utf-8') as o:
                    line = o.readline()
                    line = line.split(',')
                    tok, val = line[0], int(line[1])
                    for i in range(val):
                        b = ''
                        for j in range(4):
                            b += o.read(1)
                        o.read(1)
                        iden, t_l = decode_int(b)
                        try:
                            line = o.readline()
                            line = list(map(int, re.split(',|\n', line)[:-1]))
                            new_l = [0 for i in range(6)]
                            for _ in range(len(t_l)):
                                new_l[t_l[_]] = line[_]
                            try:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/tf[find_loc(iden)][str(iden)]*log10(21000000)/val
                            except:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/400*log10(21000000)/val
                            r_s.add(iden)
                        except:
                            pass
                    with lock:
                        if len(id_set) == 0:
                            id_set = r_s
                        else:
                            if len(id_set.intersection(r_s)) != 0:
                                id_set = id_set.intersection(r_s)
                            else:
                                id_set = id_set.union(r_s)
            if ele < line:
                break
            pos += 1
    if pos != 0:
        with open(path_to_index+'/'+di+'/'+di+'_'+str(pos-1)+'.txt', 'r', encoding='utf-8') as o:
            while True:
                line = o.readline()
                if not line:
                    break
                line = line.split(',')
                tok, val = line[0], int(line[1])
                if ele < tok:
                    break
                elif ele == tok:
                    for i in range(val):
                        b = ''
                        for j in range(4):
                            b += o.read(1)
                        o.read(1)
                        iden, t_l = decode_int(b)
                        try:
                            line = o.readline()
                            line = list(map(int, re.split(',|\n', line)[:-1]))
                            #print(line)
                            new_l = [0 for i in range(6)]
                            for _ in range(len(t_l)):
                                new_l[t_l[_]] = line[_]
                            try:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/tf[find_loc(iden)][str(iden)]*log10(21000000)/val
                            except:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/400*log10(21000000)/val
                            r_s.add(iden)
                        except:
                            pass
                    break
                else:
                    for i in range(val):
                        for j in range(4):
                            o.read(1)
                        o.readline()
        with lock:
            if len(id_set) == 0:
                id_set = r_s
            else:
                if len(id_set.intersection(r_s)) != 0:
                    id_set = id_set.intersection(r_s)
                else:
                    id_set = id_set.union(r_s)
            f_p += 1
    while not s_p:
        sleep(0.25)
    for id in id_set:
        try:
            vals[locations[id]][toks.index(ele)] = loc_s[id]
        except:
            vals[locations[id]][toks.index(ele)] = 0

def field_lookup(ele, t):
    global id_set
    global f_p
    loc_s = {}
    di = ele[0]
    pos = 0
    r_s = set()
    with open(path_to_index+'/'+di+'/sec.txt','r',encoding='utf-8') as o:
        for line in o:
            if ele == line:
                with open(path_to_index+'/'+di+'/'+di+'_'+str(pos-1)+'.txt', 'r', encoding='utf-8') as o:
                    line = o.readline()
                    line = line.split(',')
                    tok, val = line[0], int(line[1])
                    for i in range(val):
                        b = ''
                        for j in range(4):
                            b += o.read(1)
                        o.read(1)
                        iden, t_l = decode_int(b)
                        if t not in t_l:
                            o.readline()
                            continue
                        try:
                            line = o.readline()
                            line = list(map(int, re.split(',|\n', line)[:-1]))
                            new_l = [0 for i in range(6)]
                            for _ in range(len(t_l)):
                                new_l[t_l[_]] = line[_]
                            try:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/tf[find_loc(iden)][str(iden)]*log10(21000000)/val
                            except:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/400*log10(21000000)/val
                            r_s.add(iden)
                        except:
                            pass
                    with lock:
                        if len(id_set) == 0:
                            id_set = r_s
                        else:
                            if len(id_set.intersection(r_s)) != 0:
                                id_set = id_set.intersection(r_s)
                            else:
                                id_set = id_set.union(r_s)
            if ele < line:
                break
            pos += 1
    if pos != 0:
        with open(path_to_index+'/'+di+'/'+di+'_'+str(pos-1)+'.txt', 'r', encoding='utf-8') as o:
            while True:
                line = o.readline()
                if not line:
                    break
                line = line.split(',')
                tok, val = line[0], int(line[1])
                if ele < tok:
                    break
                elif ele == tok:
                    for i in range(val):
                        b = ''
                        for j in range(4):
                            b += o.read(1)
                        o.read(1)
                        iden, t_l = decode_int(b)
                        if t not in t_l:
                            o.readline()
                            continue
                        try:
                            line = o.readline()
                            line = list(map(int, re.split(',|\n', line)[:-1]))
                            #print(line)
                            new_l = [0 for i in range(6)]
                            for _ in range(len(t_l)):
                                new_l[t_l[_]] = line[_]
                            try:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/tf[find_loc(iden)][str(iden)]*log10(21000000)/val
                            except:
                                loc_s[iden] = sum([w[i]+new_l[i] for i in range(6)])/400*log10(21000000)/val
                            r_s.add(iden)
                        except:
                            pass
                    break
                else:
                    for i in range(val):
                        for j in range(4):
                            o.read(1)
                        o.readline()
        with lock:
            if len(id_set) == 0:
                id_set = r_s
            else:
                if len(id_set.intersection(r_s)) != 0:
                    id_set = id_set.intersection(r_s)
                else:
                    id_set = id_set.union(r_s)
            f_p += 1
    while not s_p:
        sleep(0.25)
    for id in id_set:
        try:
            vals[locations[id]][toks.index((ele, t))] = loc_s[id]
        except:
            vals[locations[id]][toks.index((ele, t))] = 0

def preprocess(s):
    
    s = s.replace('\\r', ' ')
    s = s.replace('\\"', ' ')
    s = s.replace('\\n', ' ')

    s = re.sub('[^A-Za-z0-9]+',' ', s)
    s = [e for e in s.split() if e.lower() not in stopwords]

    return s

def normal_query(q):
    global toks
    query = preprocess(q)
    toks = []
    for tok in query:
        ele = ps.stemWord(tok.lower())
        #print(ele)
        if ele not in toks:
            toks.append(ele)

def parse_query(q):
    global toks
    query = re.split(r':|\s', q)
    token = ""
    tags = {'t': 0, 'i': 1, 'c': 2, 'l': 3, 'r': 4, 'b': 5}
    flag = False
    for tok in query:
        if tok in tags.keys():
            token = tok
        else:
            ele = preprocess(tok.lower())
            if ele == []:
                continue
            ele = ps.stemWord(ele[0])
            if (ele,tags[token]) not in toks:
                toks.append((ele, tags[token]))

def init_state():
    global toks
    global f_p
    global s_p
    toks = []
    f_p = 0
    s_p = False

with open(file_path) as o:
    for line in o:
        init_state()
        if ':' not in line:
            start = time()
            normal_query(line)
            th = [threading.Thread(target=lookup, args=(toks[i], )) for i in range(len(toks))]
            for i in range(len(th)):
                th[i].start()
            while f_p < 3:
                sleep(0.5)
            title_id = list(id_set)
            locations = {title_id[i]: i for i in range(len(title_id))}
            vals = [[0 for i in range(len(toks))] for j in title_id]
            s_p = not s_p
            for i in range(len(th)):
                th[i].join()
            title_id = sorted(zip(title_id, vals), key= lambda x: sum(x[1]), reverse=True)[:n_records]
            end = time()
            elapsed = end-start
            with open('q_outputs.txt','a') as o:
                for i in range(len(title_id)):
                    o.write(str(title_id[i][0])+'\n')
                o.write('#'*10+'\n')
            with open('times.txt','a') as o:
                o.write(str(elapsed)+'\n')
        else:
            start = time()
            parse_query(line)
            th = [threading.Thread(target=field_lookup, args=(toks[i][0], toks[i][1], )) for i in range(len(toks))]
            for i in range(len(th)):
                th[i].start()
            while f_p < 3:
                sleep(0.5)
            title_id = list(id_set)
            locations = {title_id[i]: i for i in range(len(title_id))}
            vals = [[0 for i in range(len(toks))] for j in title_id]
            s_p = not s_p
            for i in range(len(th)):
                th[i].join()
            title_id = sorted(zip(title_id, vals), key= lambda x: sum(x[1]), reverse=True)[:n_records]
            end = time()
            elapsed = end-start
            with open('q_outputs.txt','a') as o:
                for i in range(len(title_id)):
                    o.write(str(title_id[i][0])+'\n')
                o.write('#'*10+'\n')
            with open('times.txt','a') as o:
                o.write(str(elapsed)+'\n')

print('All Queries are completed\n')
print('Searching for titles\n')
with open('master_ready.txt','w') as o:
    o.write('Ready!')