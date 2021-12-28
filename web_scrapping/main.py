import requests, lxml, time
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint


URL = 'https://habr.com/ru/all/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
KEYWORDS = ['ruby', 'python', 'Git', 'iOS', 'трансляции']
STOP_WORDS = ['Навальный', 'взрослых']


# не доделал
def has_stop_keywords(text):
    result = False
    if text:
        for word in STOP_WORDS:
            if word.lower() in text.lower():
                result = True
    return result

def check_keywords(text):
    result = False
    if text: #контент не всегда есть
        for word in KEYWORDS:
            if word.lower() in text.lower():
                # print('=====')
                # print(word)
                # print(text)
                result = True

    # result = result and not has_stop_keywords(text) 
    return result



def get_posts(check_content = False):
    articles_result = []

    result = requests.get(url=URL, headers=HEADERS)
    result.raise_for_status()

    soup = BeautifulSoup(result.content, 'lxml')
    headers = soup.select("article")

    for h in tqdm(headers):
        h_date = h.find('time').get('title')
        h_title = h.find(class_="tm-article-snippet__title-link").text
        link = 'https://habr.com' + h.find(class_="tm-article-snippet__title-link").get('href')
        hubs = h.find_all(class_="tm-article-snippet__hubs-item-link")

        hubs_text= ''
        if hubs:
            # hubs = {h.text.strip() for h in hubs} # нафига я так ?
            list = []
            for i in hubs:
                list.append(i)
            hubs_text = str(list)

        sumarry = h.find(class_='article-formatted-body article-formatted-body_version-2')
        if sumarry:
            list = []
            for i in sumarry:
                list.append(i)
            sumarry = str(list)

        # sumarry = h.find(class_='article-formatted-body article-formatted-body_version-2')

        # для быстродействия сначала в title если нет то уровнем ниже
        keyword_found = False
        if check_keywords(h_title):
            keyword_found = True
        elif check_keywords(hubs_text):
            keyword_found = True
        elif check_keywords(sumarry):
            keyword_found = True

        if check_content:
            post = requests.get(url=link, headers=HEADERS)
            result.raise_for_status()
            soup_post = BeautifulSoup(post.content, 'lxml')
            text_post = soup_post.find(id="post-content-body").text
            keyword_found = check_keywords(text_post)

        if keyword_found:
            item = {
                'date': h_date,
                'title': h_title,
                'link': link
            }
            articles_result.append(item)


    return articles_result


if __name__ == '__main__':
    # check_content=True - поиск по содержимому статьи
    list = get_posts(check_content=False)
    for i  in list:
        print(f"{i.get('date')} - {i.get('title')} - {i.get('link')}")