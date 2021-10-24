import os
import sys
import xml.sax
import re
import Stemmer
from bz2 import BZ2File

file_count = 0
n_postings = 0
posting_limit = 1000000
temp_index = {}
ps = Stemmer.Stemmer('english')
path_to_dummy = sys.argv[2]
path_to_dump = sys.argv[1]
#skip = int(sys.argv[3])
#pos = skip

if not os.path.isdir(path_to_dummy):
    os.mkdir(path_to_dummy)

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
            'infobox', 'category', 'categories', 'title', 'body', 'links', 'link', 'references', 'reference', 'html', 'xml', 'url', 'https', 'http', 'www', \
            'web', 'com', 'co', 'org', 'cfm', 'edu', 'refbegin', 'reflist', 'refend', 'cite', 'bibliography', 'notes', 'gt', 'lt'\
            'ref', 'quote', '']

stopwords = {k:{'value':True} for k in stopwords}

def freq(fr):
    b = ''
    l = [v for v in fr if v != 0]
    for v in l:
        val = v.to_bytes(2, 'big')
        for i in range(len(val)):
            b += chr(val[i])
    return b

def checker():
    for key in temp_index.keys():
        if temp_index[key]['length'] != len(temp_index[key].keys())-1:
            return False
    return True

def temp_writer(p):
    global n_postings
    global file_count
    global temp_index
    with open(path_to_dummy+'/dummy_'+str(file_count)+'.txt', 'w', encoding='utf-8') as file:
        for key in sorted(temp_index.keys()):
            file.write(key+','+str(temp_index[key]['length'])+'\n')
            temp_index[key].pop('length')
            for id in sorted(temp_index[key].keys()):
                file.write(str(id)+','+','.join([str(temp_index[key][id][v]) for v in sorted(temp_index[key][id].keys(), reverse=True)])+'\n')
    n_postings = 0
    temp_index = {}
    file_count += 1
    print('\nWriting to Dummy '+str(file_count)+' Succesful!'+'-'+str(p))

'''def writer():
    count = 0
    with open(path_to_index+'/indexes.txt', 'w', encoding='utf-8') as file:
        for key in sorted(index.keys()):
            file.write(key+','+str(index[key]['length'])+'\r\n')
            index[key].pop('length')
            for id in sorted(index[key].keys()):
                file.write(encode_int(id, index[key][id][1], 4)+freq(index[key][id][0])+'\n')'''

def temp_create_index(e, id, tag):
    global n_postings
    try:
        temp_index[e]['length']
    except:
        temp_index[e] = {'length': 1, id: {128: 0, 64: 0, 32: 0, 16: 0, 8: 0, 4: 0}}
        temp_index[e][id][tag] += 1
        n_postings += 1
        if n_postings >= posting_limit:
            temp_writer(pos)
        return True
    try:
        temp_index[e][id][tag] += 1
        #temp_index[e][id][1] = temp_index[e][id][1]|tag
    except:
        temp_index[e][id] = {128: 0, 64: 0, 32: 0, 16: 0, 8: 0, 4: 0}
        temp_index[e][id][tag] += 1
        temp_index[e]['length'] += 1
        n_postings += 1
        if n_postings >= posting_limit:
            temp_writer(pos)
    return True

'''def create_index(e, id, tag):
    
    try:
        index[e]['length']
    except:
        index[e] = {'length': 1, id: [[0 for i in range(6)], tag]}
        index[e][id][0][7 - int(log(tag, 2))] += 1
        return True
    try:
        index[e][id][0][7 - int(log(tag, 2))] += 1
        index[e][id][1] = index[e][id][1]|tag
    except:
        index[e][id] = [[0 for i in range(6)], tag]
        index[e][id][0][7 - int(log(tag, 2))] += 1
        index[e]['length'] += 1
    return True'''

def preprocess(s, id, tag):

    global stopwords
    global invalid_tokens
    
    s = s.replace('\\r', ' ')
    s = s.replace('\\"', ' ')
    s = s.replace('\\n', ' ')

    s = re.sub('[^a-z0-9]+',' ', s)
    
    '''for number in numbers:
        #create_index(number ,id, tag)
        temp_create_index(number, id, tag)'''
    s = re.sub(r'[a-z0-9]*\d[a-z0-9]*', ' ', s)
    
    s = s.split(' ')

    for e in s:
        try:
            stopwords[e]['value']
        except:
            word = ps.stemWord(e)
            #create_index(word, id, tag)
            temp_create_index(word, id, tag)

    return s

def encode_int(n, t, l):
    b = n.to_bytes(l, 'big')
    c = (b[0]|t).to_bytes(1, 'big')+b[1:]
    #print(c)
    s = ""
    for i in range(len(c)):
        s += chr(int(c[i]))
    return s

def decode_int(s):
    b = b''
    for i in range(len(s)):
        b += ord(s[i]).to_bytes(1, 'big')
    return int.from_bytes(b, 'big')

class TextHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.tag = ""
        self.id = ""
        self.revision = ""
        self.title = ""
        self.text = ""
        self.page_count = 0
        #self.skip_count = skip
        #self.skipped = False

    def startElement(self, tag, attributes):
        '''if tag == 'page':
            self.skipped = False
            if self.skip_count > 0:
                self.skip_count -= 1
                self.skipped = True
                return
        if self.skipped:
            return'''
        self.tag = tag
        if tag == 'revision':
            self.revision = True
        if tag == 'text':
            self.text = ""
        if tag == 'title':
            self.title = ""

    def characters(self, content):
        #if self.skipped:
            #return
        if self.tag == "id" and not self.revision:
            self.id = int(content)

        if self.tag == 'title':
            self.title += content.lower()

        if self.tag == 'text':
            self.text += content.lower()

    def endElement(self, tag):
        #global pos
        #if self.skipped:
            #return
        if self.tag == 'text':
            preprocess(self.title, self.id, 128)
            results = re.findall(r"(\{\{infobox\s.*\n)(.+\n)*(\}\})", self.text)
            if results != []:
                self.text = re.sub(r"(\{\{infobox\s.*\n)(.+\n)*(\}\})",' ',self.text)
                preprocess(' '.join([' '.join(list(e)) for e in results]), self.id, 64)
            results = re.findall(r"\[\[category.*\n", self.text)
            if results != []:
                self.text = re.sub(r"\[\[category.*\n",' ', self.text)
                preprocess(' '.join(results), self.id, 32)
            results = re.findall(r"(\=+external links\=+\n)(.*\{\{.+\}\}\n)+", self.text)
            if results != []:
                self.text = re.sub(r"(\=+external links\=+\n)(.*\{\{.+\}\}\n)+",' ', self.text)
                preprocess(' '.join([' '.join(list(e)) for e in results]), self.id, 16)
            results = re.findall(r"(\=+references\=+\n)(.*(\{|\[)+.+(\}|\])+\n)+", self.text)
            if results != []:
                self.text = re.sub(r"(\=+references\=+\n)(.*(\{|\[)+.+(\}|\])+\n)+",' ', self.text)
                preprocess(' '.join([' '.join(list(e)) for e in results]), self.id, 8)
            preprocess(self.text, self.id, 4)
        if tag == 'page':
            self.page_count += 1
            #pos += 1
            '''if self.page_count == 250000:
                if temp_index != {}:
                    temp_writer(pos)
                exit()'''
            print('\rPages: '+str(self.page_count), end="")
        if tag == 'revision':
            self.revision = False
        self.tag = ''

parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

handler = TextHandler()
parser.setContentHandler(handler)

    #parser.parse("sam_input.xml")
    #try:
parser.parse(BZ2File(path_to_dump))
    #writer()
if temp_index != {}:
    temp_writer()
    '''except:
        print('Invalid Query')'''
    '''for i in range(len(sec_index)):
        print(sec_index[i][0])
        print("-----INDEXES-----")
        for j in range(len(index[i])):
            print(index[i][j])
            print("-----DOC IDS-----")
            for k in range(len(data[i][j])):
                print(data[i][j][k][0])
        print('#'*50)'''