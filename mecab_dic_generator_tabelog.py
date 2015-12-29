import unicodedata
import os


def main():
    keyword_type = "tabelog"

    fout_folder = os.path.join(os.path.dirname(__file__), "data/")
    fin_name = os.path.join(fout_folder, "tabelog_list_jinbocho.txt")
    fout_name = os.path.join(fout_folder, "jinbocho.csv")

    with open(fout_name, mode='w', encoding='utf-8') as fout:
        with open(fin_name, mode='r', encoding='utf-8') as fin:
            for line in fin:
                words = line.split('\t')
                word = unicodedata.normalize('NFKC', words[0])
                word = word.lower()

                cost = int(max(-36000, -400 * len(word) ** 1.5))
                fout.write("%s,-1,-1,%d,名詞,一般,*,*,*,*,*,*,*,%s\n" % (word, cost, keyword_type))


if __name__ == "__main__":
    main()
