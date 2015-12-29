import os
import asyncio
import aiohttp
import bs4
import time


def main():

    urls = []
    # urls.append('http://tabelog.com/tokyo/rstLst/1/?sa=%E6%9D%B1%E4%BA%AC%E9%83%BD')
    # urls.append('http://tabelog.com/tokyo/rstLst/2/?sa=%E6%9D%B1%E4%BA%AC%E9%83%BD')
    for i in range(33, 61):
        urls.append('http://tabelog.com/tokyo/A1305/rstLst/' + str(i) + '/?Srt=D&SrtT=rt')
    # urls.append('http://tabelog.com/tokyo/A1305/rstLst/2/?Srt=D&SrtT=rt')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_tsv_data(urls))


@asyncio.coroutine
def get_tsv_data(url_list):
    for url in url_list:
        list_html = yield from get_html(url)
        list_text = yield from list_html.read()

        url_detail_list = get_url_list(list_text)

        for url in url_detail_list:
            detail_html = yield from get_html(url)
            detail_text = yield from detail_html.read()

            details = get_details(detail_text, url)
            write_files(details, True)

        # url = 'http://tabelog.com/tokyo/A1316/A131603/13168848/'
        # detail_html = yield from get_html(url)
        # detail_text = yield from detail_html.read()

        # details = get_details(detail_text)
        # write_files(details)

    return


@asyncio.coroutine
def get_htmls(urls):
    htmls = []
    for url in urls:
        htmls.append(get_html(url))
    return htmls


def get_html(url):
    time.sleep(1)
    return (yield from aiohttp.request('GET', url))


def get_url_list(lists_data):
    soup = bs4.BeautifulSoup(lists_data)
    li_lists = soup.findAll('li', attrs={'class': 'bkmk-rst'})
    detail_url_lists = []
    for li_list in li_lists:
        detail_url_lists.append(li_list.div.div.div.a.attrs['href'])

    return detail_url_lists


def get_details(html_detail, url):
    soup = bs4.BeautifulSoup(html_detail)

    details = []

    # 店名
    shop_name = soup.findAll('span', attrs={'class': 'display-name'})[0].text

    # Rank
    rank = soup.findAll('strong', attrs={'class': 'score'})[0].span.text

    # 住所
    addless = soup.findAll('p', attrs={'rel': 'v:addr'})[0].text

    # TEL
    # tels = []
    # tel_lists = soup.findAll('div', attrs={'id': 'tel_info'})[0].findAll('strong')
    # for tel_list in tel_lists:
    #     tels.append(tel_list.text)

    # tel = ",".join(tels)

    # maintext
    # maintexts = []
    # maintext = "-"

    # maintext_list = soup.find('div', attrs={'id': 'contents-maintext'})

    # if (maintext_list is not None):
    #     maintexts.append(maintext_list.h3.text)
    #     maintexts.append(maintext_list.span.text)
    #     maintext = ",".join(maintexts)

    # おすすめ
    # push_menu = '-'
    # push_menu = soup.find('div', attrs={'id': 'push-menu'}).strong.text
    # if push_menu is not None:
    #         push_menu = '食べるべき一品: ' + push_menu

    # colmns = [shop_name, addless, tel, maintext]
    colmns = [shop_name, rank, addless, url]
    details.append(to_line(colmns))

    return details


def to_line(colmns):
    return ("\t".join(colmns))


def write_files(details, add_flag):
    data_folder = os.path.join(os.path.dirname(__file__), "data/")
    write_file = os.path.join(data_folder, "tabelog_basic.txt")

    write_type = "wb"
    if add_flag:
        write_type = "ab"

    with open(write_file, write_type) as outfile:
        for detail in details:
            outfile.write((detail + "\r\n").encode("utf-8"))


if __name__ == "__main__":
    main()
