import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from clint.textui import progress
import time
import os 
from colorama import Fore, Style

def anbient(name,diretorio,episodios):
	os.system('color')

	rAnbient = requests.get(f"https://www.anbient.com/search?search_api_views_fulltext={name}")
	search = bs(rAnbient.text, "html.parser")
	animeSearchList = {}
	animeEpsList = []
	episodio = ""

	for item in search.find_all('div',attrs={'id': 'search'}):
		for item_name in item.find_all('a', attrs={'rel': 'bookmark'}):
			print(item_name.text.strip())
			animeSearchList[item_name.text.strip()] = item_name['href']

	option = int(input(f"{Fore.CYAN}{Style.BRIGHT}Esses foram os resultados, bote o numero que corresponde ao anime que vc quer:{Style.RESET_ALL}"))
	for i,key in enumerate(animeSearchList):
		if option - 1 == i:
			link = f"https://www.anbient.com{animeSearchList[key]}"
			titulo = key
	
	nav_options = Options()
	nav_options.add_argument("--headless")
	nav_options.add_argument("--log-level=3")
	nav_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
	chrome = webdriver.Chrome(options=nav_options)
	
	rPage = chrome.get(link)
	links = chrome.execute_script("return document.getElementsByClassName('servidor zippyshare')[0].getElementsByTagName('li')")
	if episodios == "e":
		while True:
			if episodio != "":
				break
			else:
				for i in range(len(links)):
					print(f"{titulo} EP {i+1}")
				episodio = input(f"{Fore.CYAN}{Style.BRIGHT}Bote o numero do episodio que deseja baixar: {Style.RESET_ALL}")

	for i in range(len(links)):
		if episodios == "t" or episodios == "e" and int(episodio) == i+1:
			zipLinks = chrome.execute_script(f"return document.getElementsByClassName('servidor zippyshare')[0].getElementsByTagName('li')[{i}].getElementsByTagName('a')[0].getAttribute('href')")
			animeEpsList.append(zipLinks)
	for i in range(len(animeEpsList)):
		downloadLink = chrome.get(animeEpsList[i])
		time.sleep(1)
		dlButton = chrome.execute_script("return document.getElementById('dlbutton')['href']")
		download = requests.get(dlButton,stream=True)
		if episodios == "e":
			EP = episodio
		else:
			EP = i + 1
		with open(f"{diretorio}/{titulo.replace('.','')}({EP}).mp4", "wb") as f:
			totalLenght = int(download.headers.get('content-length'))
			print(f"{Fore.CYAN}{Style.BRIGHT}Baixando episodio {i+1} de {titulo}: {Style.RESET_ALL}")
			for chunk in progress.bar(download.iter_content(chunk_size=8192), expected_size=(totalLenght/8192) + 1):
				if chunk:
					f.write(chunk)
					f.flush()
			print(f"{Fore.GREEN}{Style.BRIGHT}Episodio baixado!{Style.RESET_ALL}")
	chrome.close()