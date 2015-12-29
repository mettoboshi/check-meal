# coding:utf-8

import os
import sys
import csv
import numpy as np

from util import load_dump_file, write_dump_file, choice_word, wakati


def main():

    argvs = sys.argv
    argc = len(argvs)
    if (argc != 4):
        print('Usage: # python %s in_filename, out_filename, class_value' % argvs[0])
        quit()

    data_folder = os.path.join(os.path.dirname(__file__), "data/")

    load_dic_file_name = os.path.join(data_folder, "word_dic.dat")
    words_dic = load_dump_file(load_dic_file_name)

    tsv = csv.reader(open("./data/" + argvs[1]), delimiter='\t')

    words_data = []
    for tsv_line in tsv:
        if len(tsv_line) == 5:
            description = tsv_line[3] + tsv_line[4]
        else:
            description = tsv_line[3]

        lines = wakati(description)
        word_data = []
        for line in lines:
            word = choice_word(line)
            if word != '':
                word_data.append(word)

        words_data.append(word_data)

    feature_length = len(words_dic)

    traning_data = []
    for word_line in words_data:
        feature = np.zeros(feature_length)
        for word_colmn in word_line:
            if words_dic.get(word_colmn):
                feature[words_dic[word_colmn]['index']] = 1

        traning_data.append({"feature": feature, "class": int(argvs[3])})

    write_file_name = os.path.join(data_folder, argvs[2])
    write_dump_file(write_file_name, traning_data)


if __name__ == "__main__":
    main()
