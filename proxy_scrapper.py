from pynput import keyboard
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore


print(f'{Fore.GREEN}f2 - check http proxies')
print(f'{Fore.GREEN}f3 - check http{Fore.RED + "s"}{Fore.GREEN} proxies')

IS_HTTP = False
IS_HTTPS = False


ua = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'

URL = 'https://free-proxy-list.net/'
HEADERS = {'user-agent': ua}


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def get_proxies(html):
    soup = BeautifulSoup(html, 'html.parser')
    proxies = [x.text for x in soup.findAll("td")]  # это формирует список с кашей из тегов td, в которых хранятся проксяки
    proxies_list = {}
    i = 0
    while i < len(proxies):
        if IS_HTTP:             # флаги выставляются в True при нажатии на клавишу в функции on_press_func
            proxy_type = 'no'   # В формируемом списке no - http, yes - https
        elif IS_HTTPS:
            proxy_type = 'yes'
        # ищу регуляркой ip и формирую список только с http или https, индекс i + 6 хранит в себе инфу о типе
        if re.match(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', proxies[i]) and proxies[i + 6] == proxy_type:
        # отталкиваюсь от индекса с ip для формирования информации о прокси в словаре.
            ip = proxies[i]
            port = proxies[i + 1]
            country = proxies[i + 3]
            proxy_type2 = proxies[i + 4]   # elite, anonymous type etc...
            time = proxies[i + 7]
            proxies_list[ip] = [port, country, proxy_type, proxy_type2, time]
        i += 1
    return proxies_list


def check_proxies(link):
    html = get_html(URL)
    if html.status_code == 200:
        bad_proxy_count = 1
        for ip, proxy_info in get_proxies(html.text).items():
            proxy1 = f'http://{ip}:{proxy_info[0]}'
            proxy2 = f'https://{ip}:{proxy_info[0]}'
            proxies = {'http': proxy1, 'https': proxy2}
            try:
                requests.get(link, proxies=proxies, timeout=2, headers=HEADERS)
                print(Fore.GREEN + f'IP: {ip}:{proxy_info[0]} \nCountry: {proxy_info[1]} | https: {proxy_info[2]} | {proxy_info[3]}\ntime: {proxy_info[4]}\n')     
            except:
                print(Fore.RED + f'{bad_proxy_count} Bad proxy\n')
                bad_proxy_count += 1
    else:
        print(f'status code = {html.status_code}')


def on_press_func(key):
    global IS_HTTP, IS_HTTPS
    if key == keyboard.Key.f2:
        IS_HTTP = True
        link = 'http://www.cypherpunks.ru/'
        check_proxies(link)
    if key == keyboard.Key.f3:
        IS_HTTPS = True
        link = 'https://rutracker.org'
        check_proxies(link)


with keyboard.Listener(
        on_press=on_press_func,
        ) as listener:
    listener.join()
