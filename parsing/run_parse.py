from bs4 import BeautifulSoup as BS
from config import URL_SITE
import requests as req
import asyncio
from task.database import Database


async def get_offer_page(table_list: list):  # Осуществляем сбор данных по каждой задаче в таблице
    list_task = list()
    try:
        for element in table_list:
            for tag in element.find_all('tr'):
                td = list(tag.findAll('td'))
                if td:
                    name, theme = td[1].findAll('div')
                    dct_task = {
                        'solution': int(td[4].find('a').text.strip()[1:]),
                        'name': name.find('a').text.strip(),
                        'number': td[0].find('a').text.strip(),
                        'difficulty': int(td[3].find('span').text.strip()),
                        'url': td[0].find('a').get('href'),
                        'theme': [i.text.strip().lower() for i in theme.findAll('a')]
                    }

                    list_task.append(dct_task)
    except:
        return None
    return list_task


async def convert_data_database(data_json: list):
    themes = set()
    for i in data_json:
        await Database().insert_data_task({'solution': i['solution'], 'name': i['name'], 'number': i['number'],
                                               'difficulty': i['difficulty'], 'url': i['url']})

        themes = themes | set(i['theme'])

    await Database().insert_data_theme(themes)
    for i in data_json:
        await Database().insert_data_intersection(i)


async def get_url(url: str):
    # читаем всем таблицы одной страницы
    response = req.get(url, params={'q': 'goog'}, headers={
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36',
        'Accept-Language': 'ru'})
    soup = BS(response.text, 'lxml')

    try:
        table_list = [i for i in soup.findAll("table", attrs={"class": "problems"})]
    except:
        return None

    return table_list


async def main():
    # зменение url страницы для чтения всех страниц
    number_page = 1
    component_url = URL_SITE.split('?')
    tasks = []

    # читаем таблицу данных с каждой страницы, пока цикл не закончиться
    while number_page < 2:
        url_site = component_url[0] + '/page/' + str(number_page) + f'?{component_url[1]}'

        try:
            table_tasks = await get_url(url_site)
        except:
            break

        if table_tasks:
            tasks += await get_offer_page(table_tasks)
        else:
            break

        number_page += 1

    await convert_data_database(tasks)


if __name__ == '__main__':
    asyncio.run(main())
