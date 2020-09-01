#escolher site que vai dar scrape e analisar
#ler sobre o selenium e utilizalo
#ler sobre a GUI q vai usar (acho q vou usar a dearPyGUI)
#links e outras coisas uteis no notion
import os
import sys
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
from colorama import Fore, Style
from clint.textui import progress
from anbient import anbient
from goyabu import goyabu

os.system('color')

#get user input
site = input(f"{Fore.CYAN}De qual site vc quer baixar?{Style.RESET_ALL} {Fore.YELLOW}default = anbient{Style.RESET_ALL}\n{Fore.GREEN}anbient = a\ngoyabu = g\n{Style.RESET_ALL}")

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

if site == "g":
    goyabu(name,directory,episodios)

else:
    anbient(name,directory,episodios)