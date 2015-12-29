# coding:utf-8

import os
import sys
import csv

from util import load_dump_file, write_dump_file, choice_word, wakati


def main():
    word_dic = {}
    index = 0

    argvs = sys.argv
    argc = len(argvs)
    if (argc != 3):
        print('Usage: # python %s in_filename, out_filename' % argvs[0])
        quit()

    data_folder = os.path.join(os.path.dirname(__file__), "data/")
    tsv = csv.reader(open("./data/" + argvs[1]), delimiter='\t')

    dic_file_name = os.path.join(data_folder, argvs[2])
    word_dic = load_dump_file(dic_file_name)

    index = len(word_dic)
    word_list = []

    for tsv_line in tsv:
        # mecab = MeCab.Tagger("-Ochasen")
        if len(tsv_line) == 5:
            description = tsv_line[3] + tsv_line[4]
        else:
            description = tsv_line[3]

        lines = wakati(description)
        # article = mecab.parse(description)
        # lines = article.split("\n")

        word_data = []
        for line in lines:
            word = choice_word(line)

            '''
            word = line.split("\t")
            if len(word) > 3:
                if word[3].count('名詞'):
                    if word[3].count('サ変接続'):
                        pass
                    elif word[3].count('接頭詞'):
                        pass
                    elif word[3].count('代名詞'):
                        pass
                    elif word[3].count('特殊'):
                        pass
                    elif word[3].count('数'):
                        pass
                    else:
                        if not word_dic.get(word[0]):
                            word_dic[word[0]] = {'index': index, 'word': word[0]}
                            index += 1
                        word_data.append(word[0])
            '''

            if word != '':
                if not word_dic.get(word):
                    word_dic[word] = {'index': index, 'word': word}
                    index += 1
                    word_data.append(word)

        word_list.append(word_data)

    write_dump_file(dic_file_name, word_dic)

    '''
    traning_file_name = os.path.join(data_folder, argvs[2])
    write_dump_file(traning_file_name, word_list)
    '''
    print('outfile : %s' % argvs[2])

if __name__ == "__main__":
    main()
