import datetime
import numpy as np
from random import randint
from pyspark import SparkContext
from .snp_functions import snp_single, snp_double

def rddTranspose(set1):
    rddT1 = set1.zipWithIndex().flatMap(lambda x_i: [(x_i[1], j, e) for (j, e) in enumerate(x_i[0])])
    rddT2 = rddT1.map(lambda i_j_e: (i_j_e[1], (i_j_e[0], i_j_e[2]))).groupByKey().sortByKey()
    rddT3 = rddT2.map(lambda i_x: sorted(list(i_x[1]), key=lambda t: t[0]))
    rddT4 = rddT3.map(lambda x: [y for (i, y) in x])
    return rddT4


def snp_spark(input_string, output_string, snp_function):
    sc = SparkContext(appName="SNP-DataProcess")
    start_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    y1 = sc.textFile(input_string) \
        .filter(lambda line: line[0] == "T") \
        .map(lambda line: [a for a in line.split("\t")]) \
        .map(lambda line: line[11:])

    y1 = rddTranspose(y1)

    y1 = y1.map(lambda x: snp_function([np.array(x)]))

    y1.saveAsTextFile(output_string + str(start_time))
    sc.stop()
