#escolher site que vai dar scrape e analisar
#ler sobre o selenium e utilizalo
#ler sobre a GUI q vai usar (acho q vou usar a dearPyGUI)
#links e outras coisas uteis no notion

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options 
import time

#get user input
name = input("Nome do anime: ").replace(" ", "-")
directory = input("Onde vc quer salvar os episodios: ").replace("\\", "/")
episodios = input('Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n')
episodio = input("Bote o numero do episodio que deseja baixar: ")

#yahari-ore-no-seishun-love-comedy-wa-machigatteiru-kan

#create chrome instance for later
nav_options = Options()
nav_options.add_argument("--headless")
nav_options.add_argument("--log-level=3")
nav = webdriver.Chrome(chrome_options=nav_options)

r = requests.get(f"https://goyabu.com/assistir/{name}/")
#if you dont put nothing in "name" it gets the latests anime in site :)
soup = bs(r.text, "html.parser")

videos_div = soup.find_all('div',attrs={'class': 'loop-content phpvibe-video-list miau'})
for videos in videos_div:
    for i,video in enumerate(videos.find_all('a',attrs={'class':'clip-link'})):
        if episodios == "t" or episodios == "e" and int(episodio) == i+1:

            video_link = video['href']
            nav.get(video_link)
            try:
                print(f"Baixando episodio {i+1} de {name}")
                download_link = nav.execute_script("return document.getElementsByClassName('jw-video jw-reset')[0].getAttribute('src')")
                response_download = requests.get(download_link)
                open(f"{directory}/{name}({i+1}).mp4", "wb").write(response_download.content)
                print("Episodio baixado!")
            except TimeoutException:
                print("erro")

nav.close()