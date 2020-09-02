import os
import time
from anbient import anbient
from goyabu import goyabu
from colorama import Fore, Style
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import *

root = Tk()
root.withdraw()

os.system('color')

#get user input
site = input(f"{Fore.CYAN}De qual site vc quer baixar?{Style.RESET_ALL} {Fore.YELLOW}default = anbient{Style.RESET_ALL}\n{Fore.GREEN}anbient = a\ngoyabu = g\n{Style.RESET_ALL}")

name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")
while True:
    if name == "":
        name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")
    else:
        break

directory = filedialog.askdirectory()

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