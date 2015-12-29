# coding:utf-8

import os
import pickle
import MeCab


def write_dump_file(write_file_name, data):
    write_type = "wb"

    outfile = open(write_file_name, write_type)
    outfile.write(pickle.dumps(data, protocol=2))


def load_dump_file(load_file):
    words_dic = {}
    if os.path.isfile(load_file):
        words_dic = pickle.loads(open(load_file, 'rb').read())

    return words_dic


def array_to_line(colmns):
    return ("\t".join(colmns))


def write_files(details, write_file, add_flag):
    write_type = "wb"
    if add_flag:
        write_type = "ab"

    with open(write_file, write_type) as outfile:
        for detail in details:
            outfile.write((detail + "\r\n").encode("utf-8"))


def wakati(words):
    mecab = MeCab.Tagger("-Ochasen")
    article = mecab.parse(words)
    word_lines = article.split("\n")

    return word_lines


def choice_word(word_line):
    word = word_line.split("\t")
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
                return word[0]

    return ''
