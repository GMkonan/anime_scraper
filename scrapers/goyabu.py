import os
import sys
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
from colorama import Fore, Style
from clint.textui import progress
from PyInquirer import prompt

def goyabu(name,directory,episodios): 
    r = requests.get(f"https://goyabu.com/?s={name}")

    soup_search = bs(r.text, "html.parser")

    videos_in_menu = soup_search.find_all('div',attrs={'class': 'loop-content phpvibe-video-list miau'})

    link = f"https://goyabu.com/assistir/{name.replace(' ', '-').lower()}/"

    animeSearchList = {}

    for h4s in videos_in_menu:
        if len(h4s) <= 1:
            print(f"{Fore.RED}Nenhum resultado,Tem certeza que digitou o nome correto?{Style.RESET_ALL}")
            quit()
        titles = h4s.find_all("h4",attrs={'class': 'video-title'})
        for title in titles:
            for t in title.find_all("a"):
                animeSearchList[t['title']] = t['href']
        questions = [
        {
        'type': 'list',
        'name': 'Anime_name',
        'message': "Esses foram os resultados, escolha qual baixar: ",
        'choices':[i for i in animeSearchList]
        }
        ]
        resposta = prompt(questions)
        link = animeSearchList[resposta['Anime_name']]
        titulo = resposta['Anime_name']

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
    if episodios == "e":
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
                    for chunk in progress.bar(response_download.iter_content(chunk_size=8192), expected_size=(total_length/8192) + 1): 
                        if chunk:
                            f.write(chunk)
                            f.flush()
                print(f"{Fore.GREEN}{Style.BRIGHT}Episodio baixado!{Style.RESET_ALL}")


    nav.close()