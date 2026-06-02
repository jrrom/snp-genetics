
#this file is for double sequence of ATGC format
#code is written here as followed by paper of DNA
import numpy as np
import os

def extract(x):
    res = [0 for row in range(12)]
    index = 0
    for i in range(len(x)):
        if x[i] == "AA":
            res[index+0] += 1
            res[index+1] += i
        elif x[i] == "TT":
            res[index+3] += 1
            res[index+4] += i
        elif x[i] == "GG":
            res[index+6] += 1
            res[index+7] += i
        elif x[i] == "CC":
            res[index+9] += 1
            res[index+10] += i

    if res[index+0] == 0:
        meanA = 0
    else:
        meanA = res[index+1] / res[index+0]
    if res[index+3] == 0:
        meanT = 0
    else:
        meanT = res[index+4] / res[index+3]
    if res[index+6] == 0:
        meanG = 0
    else:
        meanG = res[index+7] / res[index+6]
    if res[index+9] == 0:
        meanC = 0
    else:
        meanC = res[index+10] / res[index+9]

    for i in range(len(x)):
        if x[i] == "AA":
            if res[index+0] != 0:
                res[index+2] = ((i - meanA) ** 2) / res[index+0] + res[index+2]
        elif x[i] == "TT":
            if res[index+3] != 0:
                res[index+5] = ((i - meanT) ** 2) / res[index+3] + res[index+5]
        elif x[i] == "GG":
            if res[index+6] != 0:
                res[index+8] = ((i - meanG) ** 2) / res[index+6] + res[index+8]
        elif x[i] == "CC":
            if res[index+9] != 0:
                res[index+11] = ((i - meanC) ** 2) / res[index+9] + res[index+11]

    return res


def snp_double(folder):
    input_path = os.path.join(folder, "")
    output_path = os.path.join(folder, "output/")
    os.makedirs(output_path, exist_ok=True)

    for filename in os.listdir(input_path):
        if filename == "output":
            continue
        with open(os.path.join(input_path, filename), "r") as f, \
             open(os.path.join(output_path, filename), "w") as op:

            linelist = []
            # skip header line
            f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                line1 = line.split('\n')[0].split('\t')[11:]
                linelist.append(line1)

            linelist = np.array(linelist).transpose()
            final_list = list(map(lambda x: extract(x), linelist))

            for row in final_list:
                op.write("%s\n" % row)

