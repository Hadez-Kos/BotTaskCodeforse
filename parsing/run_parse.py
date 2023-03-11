from bs4 import BeautifulSoup as BS
from config import URL_SITE
import requests as req
import asyncio
from task.database import Database


async def get_offer_page(table_list: list):
    list_task = list()
    list_theme = list()
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
                    'url': td[0].find('a').get('href')
                }

                dct_theme = {
                    'name': [i.text.strip() for i in theme.findAll('a')]
                }
                list_task.append(dct_task)
                list_theme.append(dct_theme)
    return list_task, list_theme


async def get_url(url: str):
    # читаем всем таблицы одной страницы
    response = req.get(url)
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

    # читаем таблицу данных с каждой страницы, пока цикл не закончиться
    while True:
        url_site = component_url[0] + '/page/' + str(number_page) + f'?{component_url[1]}'

        try:
            table_tasks = await get_url(url_site)
        except:
            break

        tasks, themes = await get_offer_page(table_tasks)

        await Database().insert_data_task(tasks)
        await Database().insert_data_theme(themes)

        if table_tasks:
            print(table_tasks)

        number_page += 1


if __name__ == '__main__':
    asyncio.run(main())
