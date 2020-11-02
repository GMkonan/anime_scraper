import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from clint.textui import progress
import time
import os 
from colorama import Fore, Style
from PyInquirer import prompt, Separator
from pathlib2 import Path
import re

def get_path(titulo):
    path = Path('anime') / titulo
    path.mkdir(parents=True, exist_ok=True)
    return path

def anbient(name,diretorio,episodios):
	os.system('color')

	rAnbient = requests.get(f"https://www.anbient.com/search?search_api_views_fulltext={name}")
	search = bs(rAnbient.text, "html.parser")
	animeSearchList = {}
	animeEpsList = []
	episodio = ""
	lista_episodes = []

	for item in search.find_all('div',attrs={'id': 'search'}):
		for item_name in item.find_all('a', attrs={'rel': 'bookmark'}):
			animeSearchList[item_name.text.strip()] = item_name['href']
	questions = [
        {
        'type': 'list',
        'name': 'Anime_name',
        'message': "Esses foram os resultados, escolha qual baixar: ",
        'choices':[i for i in animeSearchList]
        }
    ]

	resposta = prompt(questions)
	link = f"https://www.anbient.com{animeSearchList[resposta['Anime_name']]}"
	titulo = resposta['Anime_name']
	
	nav_options = Options()
	nav_options.add_argument("--headless")
	nav_options.add_argument("--log-level=3")
	chrome = webdriver.Chrome(options=nav_options)

	rPage = chrome.get(link)
	time.sleep(3)
	links = chrome.execute_script("return document.getElementsByClassName('servidor zippyshare')[0].getElementsByTagName('li')")

	if episodios == None:
		options_eps = [
        {
        'type': 'checkbox',
        'name': 'episodes',
        'message': "Esses foram os resultados:",
        'choices':[
			{'name':f"{titulo} EP {i+1}"} for i in range(len(links))	
				]
        	}
    	]
		eps_options = prompt(options_eps)
		for i in eps_options['episodes']:
			for j in i:
				if j.isdigit():
					lista_episodes.append(j)
		for i in lista_episodes:
			zipLinks = chrome.execute_script(f"return document.getElementsByClassName('servidor zippyshare')[0].getElementsByTagName('li')[{i}].getElementsByTagName('a')[0].getAttribute('href')")
			animeEpsList.append(zipLinks)

	else:
		episodios = episodios.split("-")
		for i in range(int(episodios[0]), int(episodios[1])):
			zipLinks = chrome.execute_script(f"return document.getElementsByClassName('servidor zippyshare')[0].getElementsByTagName('li')[{i}].getElementsByTagName('a')[0].getAttribute('href')")
			animeEpsList.append(zipLinks)
			lista_episodes.append(i)
	for i in range(len(animeEpsList)):
		downloadLink = chrome.get(animeEpsList[i])
		time.sleep(1)
		dlButton = chrome.execute_script("return document.getElementById('dlbutton')['href']")
		download = requests.get(dlButton,stream=True)
		if diretorio == None:
			path = get_path(titulo)
		else:
			path = diretorio
		with open(f"{path}/{re.sub('[./: +]','',titulo)}({lista_episodes[i]}).mp4", "wb") as f:
			totalLenght = int(download.headers.get('content-length'))
			print(f"{Fore.CYAN}{Style.BRIGHT}Baixando episodio {lista_episodes[i]} de {titulo}: {Style.RESET_ALL}")
			for chunk in progress.bar(download.iter_content(chunk_size=8192), expected_size=(totalLenght/8192) + 1):
				if chunk:
					f.write(chunk)
					f.flush()
			print(f"{Fore.GREEN}{Style.BRIGHT}Episodio baixado!{Style.RESET_ALL}")
	chrome.close()