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

		self.directory = filedialog.askdirectory()
		
		while True:
			if self.directory == "":
				self.directory = filedialog.askdirectory()
			else:
				break