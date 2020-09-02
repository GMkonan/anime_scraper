from scrapers.anbient import anbient
from scrapers.goyabu import goyabu
from inputs import Input

#class with all the needed inputs provided in inputs.py
inputs = Input()

#get user input
site = inputs.site

name = inputs.name

directory = inputs.directory

episodios = inputs.episodios


if site == "g":
    goyabu(name,directory,episodios)

else:
    anbient(name,directory,episodios)