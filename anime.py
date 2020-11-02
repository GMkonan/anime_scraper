from scrapers.anbient import anbient
from scrapers.goyabu import goyabu
#from inputs import Input
from pyfiglet import Figlet
from argparse import ArgumentParser

#Just a great title
fonte = Figlet(font='slant')
print(fonte.renderText('Anime Donwloader'))


parser = ArgumentParser(description='Esse eh um pequeno script para baixar animes.')

parser.add_argument('-r',required=False,default=None,metavar='range',
help="O range de episodios q quer baixar")


parser.add_argument('-d',required=False,default=None,metavar='diretorio',
help="O caminho da pasta onde os animes serão baixados")

parser.add_argument("anime",help="o titulo do anime que vc quer baixar entre hifens (-) ex: sword-art-online")
args = parser.parse_args()

parser.print_help()

name = args.anime


directory = args.d

episodios = args.r


anbient(name,directory,episodios)