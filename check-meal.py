# coding:utf-8

import os
import numpy as np
# from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

from util import load_dump_file


def main():
    data_folder = os.path.join(os.path.dirname(__file__), "data/")

    load_file_name = os.path.join(data_folder, "traning_data.dat")
    traning_datas = load_dump_file(load_file_name)

    load_file_name2 = os.path.join(data_folder, "test_data.dat")
    test_datas = load_dump_file(load_file_name2)

    x = np.array([v["feature"] for v in traning_datas])
    y = np.array([v["class"] for v in traning_datas])

    lr = LogisticRegression(C=1.0, penalty='l2')
    lr.fit(x, y)

    # print(lr.coef_)
    # print(lr.intercept_)
    # print(lr.score(x, y))

    # p = np.asarray([lr.predict(xi) for xi in x])
    p = [lr.predict(xi) for xi in x]

    # print(p)

    x2 = np.array([v["feature"] for v in test_datas])

    # lr = LogisticRegression(C=1.0, penalty='l2')
    # lr.fit(x2, y2)
    q = np.asarray([lr.predict(xi) for xi in x2])

    print(q)

if __name__ == "__main__":
    main()
