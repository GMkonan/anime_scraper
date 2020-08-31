#escolher site que vai dar scrape e analisar
#ler sobre o selenium e utilizalo
#ler sobre a GUI q vai usar (acho q vou usar a dearPyGUI)
#links e outras coisas uteis no notion
import os
import sys
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 
import time
from colorama import Fore, Style
from clint.textui import progress

os.system('color')

#get user input
name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")
while True:
    if name == "":
        name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")
    else:
        break

directory = input(f"{Fore.CYAN}{Style.BRIGHT}Onde vc quer salvar os episodios: {Style.RESET_ALL}").replace("\\", "/")
while True: 
    if directory == "":
        directory = input(f"{Fore.CYAN}{Style.BRIGHT}Onde vc quer salvar os episodios: {Style.RESET_ALL}").replace("\\", "/")
    else:
        break

episodios = input(f'{Fore.CYAN}{Style.BRIGHT}Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n{Style.RESET_ALL}')
while True:
    if episodios == "":
        print(f"{Fore.RED}{Style.BRIGHT}Escolha uma opcao! {Style.RESET_ALL}")
        episodios = input(f'{Fore.CYAN}{Style.BRIGHT}Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n{Style.RESET_ALL}')
    else:
        break


#yahari-ore-no-seishun-love-comedy-wa-machigatteiru-kan

r = requests.get(f"https://goyabu.com/?s={name}")

soup_search = bs(r.text, "html.parser")

videos_in_menu = soup_search.find_all('div',attrs={'class': 'loop-content phpvibe-video-list miau'})

link = f"https://goyabu.com/assistir/{name.replace(' ', '-').lower()}/"

animes = {}

for h4s in videos_in_menu:
    if len(h4s) <= 1:
        print(f"{Fore.RED}Nenhum resultado,Tem certeza que digitou o nome correto?{Style.RESET_ALL}")
        quit()
    titles = h4s.find_all("h4",attrs={'class': 'video-title'})
    for title in titles:
        for t in title.find_all("a"):
            animes[t['title']] = t['href']
            print(t['title'])

option = input(f"{Fore.CYAN}{Style.BRIGHT}Esses foram os resultados, bote o numero que corresponde ao anime que vc quer:{Style.RESET_ALL}")
for i,key in enumerate(animes):
    if int(option) - 1 == i:
        titulo = key
        link = animes[key]

#create chrome instance for later
nav_options = Options()
nav_options.add_argument("--headless")
nav_options.add_argument("--log-level=3")
nav = webdriver.Chrome(chrome_options=nav_options)

request_anime_link = requests.get(link)
#if you dont put nothing in "name" it gets the latests anime in site :)
soup = bs(request_anime_link.text, "html.parser")

videos_div = soup.find_all('div',attrs={'class': 'loop-content phpvibe-video-list miau'})
episodio = ""
while True:
    if episodio != "":
        break
    else:
        for lista_de_eps in videos_div:
            for eps in lista_de_eps.find_all("a",attrs={'class': 'clip-link'}):
                print(f"{eps['title']}\n")
        episodio = input(f"{Fore.CYAN}{Style.BRIGHT}Bote o numero do episodio que deseja baixar: {Style.RESET_ALL}")

for videos in videos_div:
    for i,video in enumerate(videos.find_all('a',attrs={'class':'clip-link'})):
        if episodios == "t" or episodios == "e" and int(episodio) == i+1:
            video_link = video['href']
            nav.get(video_link)
            download_link = nav.execute_script("return document.getElementsByClassName('jw-video jw-reset')[0].getAttribute('src')")
            response_download = requests.get(download_link, stream=True)
            with open(f"{directory}/{titulo.replace('.', '')}({i+1}).mp4", "wb") as f:
                total_length = int(response_download.headers.get('content-length'))
                print(f"{Fore.CYAN}{Style.BRIGHT}Baixando episodio {i+1} de {titulo}: {Style.RESET_ALL}")
                for chunk in progress.bar(response_download.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                    if chunk:
                        f.write(chunk)
                        f.flush()
            print(f"{Fore.GREEN}{Style.BRIGHT}Episodio baixado!{Style.RESET_ALL}")


nav.close()