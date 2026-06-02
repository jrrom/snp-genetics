from __future__ import print_function
import sys
import csv
import datetime
import time
import glob
import os, re
import math;
from pyspark.sql import SparkSession

import random
from copy import copy, deepcopy

import numpy as np
from random import randint

import pyspark;
from pyspark import SparkContext
import sklearn.metrics.pairwise;
rbf=sklearn.metrics.pairwise.rbf_kernel;

def extract(x):
	res = [0 for row in range(13)]
	res[0] = x[0];
	index = 1
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
	
	return res;
	#yield (9,(res[0],res[1]));

def rddTranspose(set1):
	rddT1 = set1.zipWithIndex().flatMap(lambda (x,i): [(i,j,e) for (j,e) in enumerate(x)])
	rddT2 = rddT1.map(lambda (i,j,e): (j, (i,e))).groupByKey().sortByKey()
	rddT3 = rddT2.map(lambda (i, x): sorted(list(x), cmp=lambda (i1,e1),(i2,e2) : cmp(i1, i2)))
	rddT4 = rddT3.map(lambda x: map(lambda (i, y): y , x))
	return rddT4;


if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: consensus <inputfile> <outfile2>", file=sys.stderr)
		exit(-1)
	
	inputfile = sys.argv[1]
	opfile2 = sys.argv[2];
	
	sc = SparkContext(appName="SNP-DataProcess")
	start_time = datetime.datetime.now()
	
	y1 = sc.textFile(inputfile)map(lambda x: np.array([float(y) for y in x.split("\t") if y!= ""]))
	y1 = rddTranspose(y1);
	y1 = y1.map(lambda x : extract(x))
	y1.saveAsTextFile(opfile2);
	

	
	
	
	
	
	
	
	
	
	
	
