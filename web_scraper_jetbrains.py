import requests
from bs4 import BeautifulSoup
import string
import os

number_of_pages = int(input())
type_articles = input()


def get_all_pages():
    for i in range(1, number_of_pages + 1):
        r = requests.get(f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={i}')
        if not os.path.exists(f'Page_{i}'):
            os.mkdir(f'Page_{i}')
        with open(f'Page_{i}/page_{i}.html', 'w', encoding='UTF-8') as file:
            file.write(r.text)
    page_count = number_of_pages + 1
    return page_count


def collect_data(page_count):
    for page in range(1, page_count):
        with open(f'Page_{page}/page_{page}.html', encoding='UTF-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'html.parser')
        for article in soup.find_all('article'):
            article_type = article.find('span', {'class': 'c-meta__type'}).text
            if article_type == type_articles:
                article_link = article.find('a', {'data-track-action': 'view article'})['href']
                article_c = requests.get(f'https://www.nature.com{article_link}')
                article_title = article.find('a').text
                article_title = article_title.translate(str.maketrans('', '', string.punctuation))
                article_title = article_title.translate(str.maketrans(' ', '_'))
                article_soup = BeautifulSoup(article_c.content, "html.parser")
                try:
                    article_body = article_soup.find('div', {'class': 'c-article-body u-clearfix'}).text
                    with open(f'Page_{page}/{article_title}.txt', 'w', encoding='UTF-8') as file:
                        file.write(article_body)
                except:
                    article_body = article_soup.find('div', {'class': 'c-article-section'}).text
                    with open(f'Page_{page}/{article_title}.txt', 'w', encoding='UTF-8') as file:
                        file.write(article_body)


def main():
    page_count = get_all_pages()
    collect_data(page_count=page_count)


if __name__ == '__main__':
    main()
