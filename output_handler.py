import os
from time import sleep

while not os.path.isfile('dummy_ready_0.txt'):
	sleep(1)
while not os.path.isfile('dummy_ready_1.txt'):
	sleep(1)
while not os.path.isfile('dummy_ready_2.txt'):
	sleep(1)

f = [open('dummy_output_'+str(i)+'.txt') for i in range(3)]
t = open('times.txt')
l = []

def output_writer():
	global l
	with open('queries_op.txt','a') as o:
		for i in range(len(l)):
			o.write(l[i][0]+'\n')
		o.write(t.readline())
		o.write('\n')

def writer():
	global l
	for i in range(len(f)):
		while True:
			line = f[i].readline().rstrip('\n')
			if not line:
				return False
			if '#'*10 == line:
				break
			loc = line.find('-')
			num = ''
			for j in range(loc+1, len(line)):
				if line[j] == '-':
					l.append([line[:loc+1]+line[j:], int(num)])
					break
				num += line[j]
	l = sorted(l, key=lambda x: x[1])
	return True

while writer():	
	output_writer()
	l = []
for i in range(len(f)):
	f[i].close()
t.close()

print('All Outputs are present in the file\n')