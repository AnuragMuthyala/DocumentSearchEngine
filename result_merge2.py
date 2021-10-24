import os
import sys

pointer_list = []
data = []
index = {}
toks = []
init = 0
min_tok = 'NULL'
pos = []
file_count = 0
flags = [128, 64, 32, 16, 8, 4]
n_postings = 0
posting_limit = 1000000
path_to_dummy = sys.argv[1]
path_to_index = sys.argv[2]
last_char = 'a'

i = 0
while i < 4:
    if os.path.isfile(path_to_dummy+'/dummy_'+str(i)+'.txt'):
        pointer_list.append(open(path_to_dummy+'/dummy_'+str(i)+'.txt', 'r', encoding='utf-8'))
        data.append([])
    else:
        break
    i += 1
print(i)
active = i

limit = 25000

i = 0
while i < 4:
    if os.path.isfile(path_to_dummy+'/dummy_'+str(i)+'.txt'):
        line = pointer_list[i].readline().split(',')
        token, val = line[0], int(line[1])
        up_limit = limit
        if val < limit:
            up_limit = val
        for _ in range(up_limit):
            line = pointer_list[i].readline().split(',')
            data[i].append([int(line[0]), [int(v) for v in line[1:]]])
        toks.append([token, val-up_limit])
    else:
        break
    i += 1

#print(toks)

def encode_int(n, t, l):
    b = n.to_bytes(l, 'big')
    c = (b[0]|t).to_bytes(1, 'big')+b[1:]
    #print(c)
    s = ""
    for i in range(len(c)):
        s += chr(int(c[i]))
    return s

def freq(fr):
    b = ''
    l = [v for v in fr if v != 0]
    for v in l:
        val = v.to_bytes(2, 'big')
        for i in range(len(val)):
            b += chr(val[i])
    return b

def writer():
    global file_count
    global index
    global n_postings
    global last_char
    count = 0

    file = open(path_to_index+'/'+last_char+'/'+last_char+'_'+str(file_count)+'.txt', 'w', encoding='utf-8')

    for key in sorted(index.keys()):
        if key[0] != last_char:
            file.close()
            print(last_char+' changed to '+key[0])
            last_char = key[0]
            file_count = 0
            file = open(path_to_index+'/'+last_char+'/'+last_char+'_'+str(file_count)+'.txt', 'w', encoding='utf-8')
        file.write(key+','+str(index[key]['length'])+'\n')
        index[key].pop('length')
        for id in sorted(index[key].keys()):
            tag = sum([flags[i] for i in range(len(flags)) if index[key][id][i] != 0])
            file.write(encode_int(id, tag, 4)+','+','.join([str(v) for v in index[key][id] if v != 0])+'\n')

    file.close()

    index = {}
    n_postings = 0
    file_count += 1
    print('\rFile '+str(file_count)+' written successfully!', end="")

def isempty(j):
    global active
    global init
    line = pointer_list[j].readline()
    if not line:
        toks[j] = 'NULL'
        active -= 1
        print(active)
        #print(toks)
        if active == 0:
            return
        if init == j:
            for _ in range(init+1, len(toks)):
                if toks[_] != 'NULL':
                    init = _
                    break
        return False
    line = line.split(',')
    toks[j] = [line[0], int(line[1])]
    up_limit = limit
    if up_limit > toks[j][1]:
        up_limit = toks[j][1]
    data[j] = []
    for _ in range(up_limit):
        line = pointer_list[j].readline().split(',')
        data[j].append([int(line[0]), [int(v) for v in line[1:]]])
    toks[j][1] -= up_limit
    return True

def find_min():
    global pos
    global min_tok
    #print(min_tok)
    min_tok = toks[init][0]
    pos = [init]
    for j in range(init+1, len(toks)):
        if toks[j] == 'NULL':
            continue
        if toks[j][0] < min_tok:
            min_tok = toks[j][0]
            pos = [j]
        elif toks[j][0] == min_tok:
            pos.append(j)
    #print(min_tok)
    #print(pos)
    index[min_tok] = {'length': 0}

def add_index():
    global pos
    global n_postings
    for j in pos:
        c = True
        while c:
            c = not c
            for k in range(len(data[j])):
                try:
                    index[min_tok][data[j][k][0]] = [index[min_tok][data[j][k][0]][i] + data[j][k][1][i] for i in range(6)]
                except:
                    index[min_tok][data[j][k][0]] = data[j][k][1]
                    index[min_tok]['length'] += 1
                    n_postings += 1
            up_limit = limit
            if toks[j][1] == 0:
                isempty(j)
                continue
            if toks[j][1] > 0 and toks[j][1] < limit:
                up_limit = toks[j][1]
            c = not c
            data[j] = []
            for _ in range(up_limit):
                line = pointer_list[j].readline().split(',')
                data[j].append([int(line[0]), [int(v) for v in line[1:]]])
            toks[j][1] -= up_limit

while active > 1:
    find_min()
    add_index()
    if n_postings >= posting_limit:
        writer()

if active == 1:
    while active == 1:
        min_tok = toks[init][0]
        pos = [init]
        index[min_tok] = {'length': 0}
        add_index()

if index != {}:
    writer()