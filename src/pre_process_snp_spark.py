from __future__ import print_function
import datetime
from pyspark.sql import SparkSession

import random
from copy import copy, deepcopy

import numpy as np
from random import randint

import pyspark
from pyspark import SparkContext
import sklearn.metrics.pairwise
rbf = sklearn.metrics.pairwise.rbf_kernel

from .snp_functions import snp_single, snp_double

def rddTranspose(set1):
    rddT1 = set1.zipWithIndex().flatMap(lambda x_i: [(x_i[1], j, e) for (j, e) in enumerate(x_i[0])])
    rddT2 = rddT1.map(lambda i_j_e: (i_j_e[1], (i_j_e[0], i_j_e[2]))).groupByKey().sortByKey()
    rddT3 = rddT2.map(lambda i_x: sorted(list(i_x[1]), key=lambda t: t[0]))
    rddT4 = rddT3.map(lambda x: [y for (i, y) in x])
    return rddT4


def snp_spark(input_file, output_folder, snp_function):
    sc = SparkContext(appName="SNP-DataProcess")
    start_time = datetime.datetime.now()

    y1 = sc.textFile(input_file).map(lambda x: np.array([float(y) for y in x.split("\t") if y != ""]))
    y1 = rddTranspose(y1)
    y1 = y1.map(lambda x: snp_function(x))
    y1.saveAsTextFile(output_folder)

    sc.stop()
