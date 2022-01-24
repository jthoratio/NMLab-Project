path = 'trace_data/'
for i in range(1, 26):
	filename = path + 'test' + str(i)
	fi = open(filename, 'r')
	fo=open("number_seq" + str(i) + ".txt", 'w')
	line=fi.readline()
	num_dict = {}
	order=0
	while line:
		if line in num_dict:
			fo.write(str(num_dict[line]) + ' ')
		else:
			num_dict[line] = order
			order += 1
			fo.write(str(num_dict[line]) + ' ')
		line=fi.readline()
	fi.close()
	fo.close()