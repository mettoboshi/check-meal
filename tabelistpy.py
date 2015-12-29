import os
import asyncio
import aiohttp
import bs4
import time
import requests


def main():

    base_url = "http://tabelog.com/tokyo/A1310/A131003/"
    html_data = requests.get(base_url + "rstLst/?Srt=D&SrtT=rt")
    soup = bs4.BeautifulSoup(html_data.text)

    restrant_num = int(soup.find('h2', attrs={'class': 'main-title'}).span.text)
    count = int(restrant_num / 20 + 2)
    urls = []

    for i in range(1, count):
        urls.append(base_url + 'rstLst/' + str(i) + '/?Srt=D&SrtT=rt')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_tsv_data(urls))


@asyncio.coroutine
def get_tsv_data(url_list):
    overrride_flg = False
    for url in url_list:
        list_html = yield from get_html(url)
        list_text = yield from list_html.read()

        line_lists = get_restrant_data(list_text)
        write_file(line_lists, overrride_flg)
        overrride_flg = True

    return


def get_html(url):
    time.sleep(1)
    return (yield from aiohttp.request('GET', url))


def get_restrant_data(list_text):
    soup = bs4.BeautifulSoup(list_text)
    restrant_list = soup.findAll('div', attrs={'class': 'rstlst-group-wrap'})

    restrant_datas = []
    for restrant in restrant_list:
        name = restrant.a.text

        explain_text = ''
        official = restrant.find('p', attrs={'class', 'official'})
        if official is not None:
            explain_text = official.a.text

        comment = restrant.find('p', attrs={'class', 'pickup'})
        if comment is not None:
            explain_text = comment.a.text

        colmns = [name, explain_text]
        restrant_datas.append(array_to_line(colmns, '\t'))

    return restrant_datas


def array_to_line(colmns, split):
    return (split.join(colmns))


def write_file(line_lists, add_flag):
    data_folder = os.path.join(os.path.dirname(__file__), "data/")
    write_file = os.path.join(data_folder, "tabelog_list_jinbocho.txt")

    write_type = "wb"
    if add_flag:
        write_type = "ab"

    with open(write_file, write_type) as outfile:
        for line_data in line_lists:
            outfile.write((line_data + "\r\n").encode("utf-8"))


if __name__ == "__main__":
    main()
