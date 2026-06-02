
#this file is for double sequence of ATGC format
#code is written here as followed by paper of DNA
import numpy as np
import os

def extract(x):
	res = [0 for row in range(12)]
	#res[0] = x[0];
	index = 0
	for i in range(len(x)):
		if(x[i]=="AA"):
			res[index+0] = res[index+0]+1;
			res[index+1] = res[index+1]+i;
		elif(x[i]=="TT"):
			res[index+3] = res[index+3]+1;
			res[index+4] = res[index+4]+i;
		elif(x[i]=="GG"):
			res[index+6] = res[index+6]+1;
			res[index+7] = res[index+7]+i;
		elif(x[i]=="CC"):
			res[index+9] = res[index+9]+1;
			res[index+10] = res[index+10]+i;
	
	if(res[index+0] == 0):
		meanA = 0
	else: 
		meanA = res[index+1]/res[index+0];
	if(res[index+3] == 0):
		meanT = 0
	else:
		meanT = res[index+4]/res[index+3];
	if(res[index+6] == 0):
		meanG = 0;
	else:
		meanG = res[index+7]/res[index+6];
	if(res[index+9] == 0):
		meanC = 0
	else:
		meanC = res[index+10]/res[index+9];
	for i in range(len(x)):
		if(x[i]=="AA"):
			if(res[index+0] != 0):
				res[index+2] = ((i - meanA) ** 2)/res[index+0] + res[index+2];
		elif(x[i]=="TT"):
			if(res[index+3] != 0):
				res[index+5] = ((i - meanT) ** 2)/res[index+3] + res[index+5];
		elif(x[i]=="GG"):
			if(res[index+6] != 0):
				res[index+8] = ((i - meanG) ** 2)/res[index+6] + res[index+8];
		elif(x[i]=="CC"):
			if(res[index+9] != 0):
				res[index+11] = ((i - meanC) ** 2)/res[index+9] + res[index+11];
	
	#res =  [1,2,3,4,5]	
	return res;

input_path = "/home/iiti/Documents/SNP-Preprocessing/diversity rice/diversity_rice31.oryzasnp.hapmap/"
output_path = input_path + "output/"

#loop in a folder
for filename in os.listdir(input_path):
	if(filename == "output"):
		continue
	#opening file
	f = open(input_path+filename, "r")
	#op file in writing  mode
	op = open(output_path+filename, "w")

	linelist = []
	count = 0
	#Reading labels 1st line
	line = f.readline()
	#reading from file and saving in a list
	while True:
		line = f.readline()
		#print((line))
		if not line:
			break
		line1 = line.split('\n')[0].split('\t')[11:]
		linelist.append(line1)


	linelist = (np.array(linelist).transpose())		#transposing the obtained list

	final_list = list(map(lambda x : extract(x), linelist))

	print(final_list[0][0])

	for row in final_list:
		op.write("%s\n" % row)

#lineList.transpose()

#print(lineList)




























