# coding:utf-8

import os

from util import load_dump_file, write_dump_file


def main():
    data_folder = os.path.join(os.path.dirname(__file__), "data/")
    data1_file_name = os.path.join(data_folder, "traning_jalan2.dat")
    traning_data_list = load_dump_file(data1_file_name)

    data2_file_name = os.path.join(data_folder, "traning_tabelog2.dat")
    traning_data_list2 = load_dump_file(data2_file_name)

    traning_data_list.extend(traning_data_list2)

    traning_file_name = os.path.join(data_folder, "test_data.dat")
    write_dump_file(traning_file_name, traning_data_list)

if __name__ == "__main__":
    main()
