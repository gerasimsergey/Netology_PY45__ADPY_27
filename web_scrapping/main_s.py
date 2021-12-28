import requests, lxml, time
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint

URL = 'https://habr.com/ru/all/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'accept': '*/*'}
KEYWORDS = ['ruby', 'python', 'Go', 'C++', 'Git']
ANTY_KEYWORDS = ['Навальный']
keywords = set(KEYWORDS)

def get_habr_info():

    info = {}
    habr = requests.get(url=URL, headers=HEADERS)

    if habr.status_code != 200:
        print('Ошибка! Habr по ходу лежит или проблема с интернетом')
    else:
        soup = BeautifulSoup(habr.content, 'lxml')
        articles = soup.select("article")

        for i in tqdm(articles):
            date = i.find('time').get('title')
            title = i.find(class_="tm-article-snippet__title-link").text
            link = 'https://habr.com' + i.find(class_="tm-article-snippet__title-link").get('href')
            hubs = i.find_all(class_="tm-article-snippet__hubs-item-link")
            hubs = {h.text.strip() for h in hubs}
            post = requests.get(url=link, headers=HEADERS)

            if post.status_code != 200:
                print(f'Страница статьи {title} не доступна.')
            else:
                soup_post = BeautifulSoup(post.content, 'lxml')
                text_post = soup_post.find(id="post-content-body").text
                text_lower = text_post.lower()

                for skip_word in ANTY_KEYWORDS:
                    if skip_word.lower() in text_post:
                        continue # ==>

                for word in KEYWORDS:
                    if word.lower() in text_lower:
                        info[date] = [title, link]

                    if hubs & keywords:
                        info[date] = [title, link]

    return info

# def new_post():
#     post = get_habr_info()
#     posts = []
#     for date, post_info in post.items():
#         posts.append(f'{date} - {" - ".join(post_info)}')
#
#     return(posts)
#
# if __name__ == '__main__':
#     posts = new_post()
#     for i in posts:
#         print(i)