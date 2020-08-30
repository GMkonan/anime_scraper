#escolher site que vai dar scrape e analisar
#ler sobre o selenium e utilizalo
#ler sobre a GUI q vai usar (acho q vou usar a dearPyGUI)
#links e outras coisas uteis no notion

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 
import time

#get user input
name = input("Nome do anime: ")   #.replace(" ", "-").lower()
directory = input("Onde vc quer salvar os episodios: ").replace("\\", "/")
episodios = input('Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n')

if episodios == "e":
    episodio = input("Bote o numero do episodio que deseja baixar: ")


#yahari-ore-no-seishun-love-comedy-wa-machigatteiru-kan

r = requests.get(f"https://goyabu.com/?s={name}")

soup_search = bs(r.text, "html.parser")

videos_in_menu = soup_search.find_all('div',attrs={'class': 'loop-content phpvibe-video-list miau'})

link = f"https://goyabu.com/assistir/{name.replace(' ', '-').lower()}/"

animes = {}

for h4s in videos_in_menu:
    titles = h4s.find_all("h4",attrs={'class': 'video-title'})
    for title in titles:
        for t in title.find_all("a"):
            animes[t['title']] = t['href']
            print(t['title'])

option = input("Esses foram os resultados, bote o numero que corresponde ao anime que vc quer:")
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
for videos in videos_div:
    for i,video in enumerate(videos.find_all('a',attrs={'class':'clip-link'})):
        if episodios == "t" or episodios == "e" and int(episodio) == i+1:

            video_link = video['href']
            nav.get(video_link)
            try:
                download_link = nav.execute_script("return document.getElementsByClassName('jw-video jw-reset')[0].getAttribute('src')")
                print(f"Baixando episodio {i+1} de {titulo}")
                response_download = requests.get(download_link)
                open(f"{directory}/{titulo.replace('.', '')}({i+1}).mp4", "wb").write(response_download.content)
                print("Episodio baixado!")
            except TimeoutException:
                print("erro")

nav.close()