import os
import sys
import json
from time import sleep

file_no = int(sys.argv[1])
low_limit = int(sys.argv[2])
up_limit = int(sys.argv[3])

while not os.path.isfile('master_ready.txt'):
	sleep(1)

tf = {}
with open('./titles/titles_{}'.format(file_no)+'.json') as o:
	tf = json.load(o)

l = []
i = 1

with open('./q_outputs.txt') as o:
	while True:
		line = o.readline()
		if not line:
			break
		line = line.rstrip('\n')
		if '#'*10 in line:
			l.append('#'*10)
			i = 1
			continue
		if int(line) > up_limit and int(line) <= low_limit:
			i += 1
			continue
		try:
			l.append(line+'-'+str(i)+'-'+tf[line].rstrip('\n'))
		except:
			pass
		i += 1

with open('dummy_output_'+str(file_no)+'.txt','w') as o:
	for i in range(len(l)):
		o.write(l[i]+'\n')

with open('dummy_ready_'+str(file_no)+'.txt','w') as o:
	o.write('Ready!'+'\n')