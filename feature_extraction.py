import numpy as np
from scipy import stats
import scipy


path = ''
feature_vector_set = []
maxi = 0

for i in range(1, 26):
	filename = path + 'number_seq' + str(i) + '.txt'

	fin = open(filename, 'r')
	system_call_trace = fin.readline()
	system_call_trace_list = system_call_trace.split(' ')[:-1]
	system_call_trace_list = list(map(int, system_call_trace_list))
	fin.close()

	#print(len(system_call_trace_list))
	for j in range(0, len(system_call_trace_list)):
		if maxi < system_call_trace_list[j]:
			maxi = system_call_trace_list[j]


	gram1 = np.zeros((maxi + 1, 1), dtype=int)
	gram2 = np.zeros((maxi + 1, maxi + 1), dtype=int)
	gram3 = np.zeros((maxi + 1, maxi + 1, maxi + 1), dtype=int)


	for j in range(0, len(system_call_trace_list)):
		gram1[system_call_trace_list[j]] += 1
		if j != len(system_call_trace_list)-1:
			gram2[system_call_trace_list[j]][system_call_trace_list[j+1]] += 1
			if j != len(system_call_trace_list)-2:
				gram3[system_call_trace_list[j]][system_call_trace_list[j+1]][system_call_trace_list[j+2]] += 1
	gram1.flatten()
	gram2.flatten()
	gram3.flatten()


	gram1_freq = gram1[gram1 != 0]
	gram2_freq = gram2[gram2 != 0]
	gram3_freq = gram3[gram3 != 0]


	feature_vector = []
	feature_vector.append(np.quantile(gram1_freq, .25))
	feature_vector.append(np.quantile(gram2_freq, .25))
	feature_vector.append(np.quantile(gram3_freq, .25))
	feature_vector.append(np.quantile(gram1_freq, .5))
	feature_vector.append(np.quantile(gram2_freq, .5))
	feature_vector.append(np.quantile(gram3_freq, .5))
	feature_vector.append(np.quantile(gram1_freq, .75))
	feature_vector.append(np.quantile(gram2_freq, .75))
	feature_vector.append(np.quantile(gram3_freq, .75))
	feature_vector.append(np.max(gram1_freq))
	feature_vector.append(np.max(gram2_freq))
	feature_vector.append(np.max(gram3_freq))
	feature_vector = feature_vector + np.divide(feature_vector, len(system_call_trace_list)).tolist()
	feature_vector.append(np.std(gram1_freq))
	feature_vector.append(np.std(gram2_freq))
	feature_vector.append(np.std(gram3_freq))
	feature_vector.append(np.mean(gram1_freq))
	feature_vector.append(np.mean(gram2_freq))
	feature_vector.append(np.mean(gram3_freq))
	feature_vector.append(scipy.stats.skew(gram1_freq))
	feature_vector.append(scipy.stats.skew(gram2_freq))
	feature_vector.append(scipy.stats.skew(gram3_freq))
	feature_vector.append(scipy.stats.kurtosis(gram1_freq))
	feature_vector.append(scipy.stats.kurtosis(gram2_freq))
	feature_vector.append(scipy.stats.kurtosis(gram3_freq))
	feature_vector.append(scipy.stats.sem(gram1_freq))
	feature_vector.append(scipy.stats.sem(gram2_freq))
	feature_vector.append(scipy.stats.sem(gram3_freq))
	feature_vector.append(scipy.stats.entropy(gram1_freq))
	feature_vector.append(scipy.stats.entropy(gram2_freq))
	feature_vector.append(scipy.stats.entropy(gram3_freq))
	

	feature_vector_set.append(feature_vector)

fout = open('normal_feature_set.txt', 'w') # Modify to attacked_feature_set.txt for compromised data

for i in range(0, len(feature_vector_set)):
	for j in range(0, 42):
		fout.write('{:10.4f}'.format(feature_vector_set[i][j]) + ' ')
	fout.write('\n')