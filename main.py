import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse




def shorten_link(token, link):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.post('https://api-ssl.bitly.com/v4/bitlinks', headers=headers, json={"long_url": link})
    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, link):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary', headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def get_bitlink(url):
    parse = urlparse(url)
    return f'{parse.netloc}{parse.path}'


def recover_link(token, bitlink):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}', headers=headers)
    response.raise_for_status()
    return response.json()['long_url']


def main():
    load_dotenv()
    BITLY_TOKEN = os.getenv('BITLY_TOKEN')
    parser = argparse.ArgumentParser(description='Сервис коротких ссылок')
    parser.add_argument('url', help='Ссылка')
    args = parser.parse_args()
    url = args.url

    if url.startswith('https://bit.ly'):
        try:
            print('Восстановленная ссылка: ', recover_link(BITLY_TOKEN, get_bitlink(url)))
        except requests.exceptions.HTTPError as e:
            print('Ошибка!!!', e)
            exit()
    else:
        try:
            url = shorten_link(BITLY_TOKEN, url)
            print('Короткая ссылка: ', url)
        except requests.exceptions.HTTPError as e:
            print('Ошибка!!!', e)
            exit()
    try:
        count = count_clicks(BITLY_TOKEN, get_bitlink(url))
        print(f'По вашей ссылке прошли {count} раз(а)')
    except requests.exceptions.HTTPError as e:
        print('Ошибка!!!', e)

if __name__ == "__main__":
    main()