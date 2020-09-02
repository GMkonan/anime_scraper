from colorama import Fore, Style
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
from tkinter import *
import os

class Input():
	def __init__(self):

		os.system('color')

		root = Tk()
		root.withdraw()

		self.site = input(f"{Fore.CYAN}De qual site vc quer baixar?{Style.RESET_ALL} {Fore.YELLOW}default = anbient{Style.RESET_ALL}\n{Fore.GREEN}anbient = a\ngoyabu = g\n{Style.RESET_ALL}")
		
		self.name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")

		while True:
			if self.name == "":
				self.name = input(f"{Fore.CYAN}Nome do anime: {Style.RESET_ALL}")
			else:
				break

		self.directory = filedialog.askdirectory()
		
		while True:
			if self.directory == "":
				self.directory = filedialog.askdirectory()
			else:
				break

		self.episodios = input(f'{Fore.CYAN}{Style.BRIGHT}Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n{Style.RESET_ALL}')
		
		while True:
			if self.episodios == "":
				print(f"{Fore.RED}{Style.BRIGHT}Escolha uma opcao!{Style.RESET_ALL}")
				self.episodios = input(f'{Fore.CYAN}{Style.BRIGHT}Se quiser baixar todos os episodios aperte "t"\nCaso queira um especifico aperte "e"\n{Style.RESET_ALL}')
			else:
				break