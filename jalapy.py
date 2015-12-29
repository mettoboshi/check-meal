import os
import asyncio
import aiohttp
import bs4
import re
from util import write_files, array_to_line


@asyncio.coroutine
def get_tsv_data(url_list):
    for url in url_list:
        list_html = yield from get_html(url)
        # list_text = yield from list_html.read()
        list_text = yield from list_html.text(encoding='shift_jis')
        # print(list_text)

        url_detail_list = get_url_list(list_text)

        for url in url_detail_list:
            pass
            # print(url)

        for url in url_detail_list:
            detail_html = yield from get_html(url)
            detail_text = yield from detail_html.read()

            details = get_details(detail_text)
            write_files(details, write_file, True)

        '''
        url = 'http://www.jalan.net/kankou/spt_13106ag2130012302/'
        detail_html = yield from get_html(url)
        detail_text = yield from detail_html.text(encoding='shift_jis')
        # print(detail_text)
        details = get_details(detail_text)
        write_files(details, True)
        '''

    return


@asyncio.coroutine
def get_htmls(urls):
    htmls = []
    for url in urls:
        htmls.append(get_html(url))

    return htmls


def get_html(url):
    return (yield from aiohttp.request('GET', url))


def get_url_list(lists_data):
    soup = bs4.BeautifulSoup(lists_data)
    item_infos = soup.findAll('div', attrs={'class': 'item-info'})
    detail_url_lists = []
    for item_info in item_infos:
        detail_url_lists.append(item_info.p.a.attrs['href'])

    return detail_url_lists


def get_details(html_detail):
    soup = bs4.BeautifulSoup(html_detail)
    details = []

    # 店名
    shop_name = soup.h1.text
    # print(shop_name)

    # 基本情報
    basic_colmns = soup.findAll('table', attrs={'class': 'basicInfoTable'})[1].findAll('th')

    colmnCount = 0
    addless = '-'
    tel = '-'

    for colmn in basic_colmns:
        if colmn.text == '所在地':
            # 住所
            addless = replace_specialized(replace_escape(soup.findAll('table', attrs={'class': 'basicInfoTable'})[1].findAll('td')[colmnCount].text))

        elif colmn.text == 'お問い合わせ':
            # TEL
            tel = replace_escape(soup.findAll('table', attrs={'class': 'basicInfoTable'})[1].findAll('td')[colmnCount].text)
        colmnCount = colmnCount + 1

    # 概要
    overview = soup.findAll('div', attrs={'class': 'aboutArea'})[0].p.text

    colmns = [shop_name, addless, tel, overview]
    details.append(array_to_line(colmns))

    return details


def replace_escape(string):
    ret = re.sub(r'[\r\n\t]', '', string)
    ret = ret.replace('\u3000', ' ')
    return ret


def replace_specialized(string):
    ret = string.replace('観光MAP', '')
    ret = ret.replace('印刷用MAP', '')
    return ret

'''
def array_to_line(colmns):
    return ("\t".join(colmns))


def write_files(details, add_flag):
    write_type = "wb"
    if add_flag:
        write_type = "ab"

    with open(write_file, write_type) as outfile:
        for detail in details:
            outfile.write((detail + "\r\n").encode("utf-8"))
'''

data_folder = os.path.join(os.path.dirname(__file__), "data/")
write_file = os.path.join(data_folder, "jalan2.txt")

urls = []
# urls.append('http://www.jalan.net/kankou/130000/page_1/?screenId=OUW1221')
urls.append('http://www.jalan.net/kankou/130000/page_2/?screenId=OUW1221')

loop = asyncio.get_event_loop()
loop.run_until_complete(get_tsv_data(urls))
