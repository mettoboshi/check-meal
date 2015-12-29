import os
import time
import requests
import bs4
from selenium import webdriver


def main():

    count = 60
    # base_url = 'http://tabelog.com/tokyo/A1305/'
    base_url = 'http://tabelog.com/tokyo/A1310/A131003/'

    restrant_urls = []
    for i in range(1, count + 1):
        restrant_urls.extend(get_url_list(base_url + 'rstLst/' + str(i) + '/?Srt=D&SrtT=rt'))

    '''
    restrant_urls = []
    # urls.append('http://tabelog.com/tokyo/A1305/A130503/13003984/')
    # urls.append('http://tabelog.com/tokyo/A1305/A130503/13114695/')
    restrant_urls.append('http://tabelog.com/tokyo/A1331/A133101/13116162/')
    restrant_urls.append('http://tabelog.com/tokyo/A1331/A133101/13159306/')
    '''

    for url in restrant_urls:
        make_urls(url + 'dtlrvwlst/')


def get_url_list(list_url):
    html_data = requests.get(list_url)
    soup = bs4.BeautifulSoup(html_data.text)
    li_lists = soup.findAll('li', attrs={'class': 'bkmk-rst'})
    detail_url_lists = []
    for li_list in li_lists:
        detail_url_lists.append(li_list.div.div.div.a.attrs['href'])

    return detail_url_lists


def make_urls(url):
    html_data = requests.get(url)
    soup = bs4.BeautifulSoup(html_data.text)

    count = int(int(soup.find("em", attrs={"class": "num"}).text) / 100) + 1

    comment_urls = []
    for i in range(1, count + 1):
        comment_urls.append(url + 'COND-0/smp1/?lc=2&rvw_part=all&PG=' + str(i))

    get_comments(comment_urls)


def get_comments(urls):
    '''
    urls = []
    for i in range(1, 6):
        # urls.append('http://tabelog.com/tokyo/A1305/A130503/13114695/dtlrvwlst/COND-0/smp1/?lc=0&rvw_part=all&PG=' + str(i))
        # urls.append('http://tabelog.com/tokyo/A1305/A130503/13114695/dtlrvwlst/COND-0/smp1/?lc=2&rvw_part=all&PG=' + str(i)) # 成蔵
        urls.append('http://tabelog.com/tokyo/A1305/A130503/13003984/dtlrvwlst/COND-0/smp1/?lc=2&rvw_part=all&PG=' + str(i)) # とん太
    '''

    driver = webdriver.PhantomJS()
    # driver.get(urls[0])

    for url in urls:
        get_html(url, driver)


def get_html(url, driver):
    time.sleep(1)
    driver.get(url)

    titles = driver.find_elements_by_css_selector(".rvw-item__rvw-title")

    mores = driver.find_elements_by_css_selector(".rvw-item__showall-trigger")

    for more in mores:
        more.click()

    contents = driver.find_elements_by_css_selector(".rvw-item__rvw-comment")

    min_num = min(len(titles), len(contents))

    for i in range(min_num):
        write_file(titles[i].text, True)
        write_file(contents[i].text, True)
        print(titles[i].text)

    return


def array_to_line(colmns, split):
    return (split.join(colmns))


def write_file(line_data, add_flag):
    data_folder = os.path.join(os.path.dirname(__file__), "data/")
    write_file = os.path.join(data_folder, "tabelog_comment_jinbocho.txt")

    write_type = "wb"
    if add_flag:
        write_type = "ab"

    with open(write_file, write_type) as outfile:
        outfile.write((line_data + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
