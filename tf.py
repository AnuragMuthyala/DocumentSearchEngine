import os
import json
import sys

file_no = sys.argv[1]
n_postings = 0
running_val = 0
tf = {}

while True:
	if not os.path.isfile('./dummy/dummy_'+file_no+'.txt'):
		break
	with open('./dummy/dummy_'+file_no+'.txt') as o:
		while True:
			line = o.readline()
			if not line:
				break
			line = line.split(',')
			tok, val = line[0], int(line[1])
			for i in range(val):
				id = int(o.readline().split(',')[0])
				try:
					tf[id] += 1
				except:
					tf[id] = 1
					n_postings += 1
			if n_postings >= 1000000:
				running_val += n_postings
				print(str(file_no)+'--'+str(running_val))
				n_postings = 0

	with open('./dummy/real_result_'+file_no+'.json','w') as o:
		json.dump(tf, o)