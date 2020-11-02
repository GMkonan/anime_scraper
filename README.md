# Anime Downloader

## Esse scraper baixa animes do site Anbient
Um pequeno script em python para baixar animes do site Anbient.Basta passar uma parte do nome do anime.
Exemplo: 'Fate/Stay Night' pode ser encontrado passando apenas a palavra 'fate'.
Se quiser passar mais de uma palavra apenas passe com hífens como por Exemplo:
Para encontrar 'sword art online' digite 'sword-art-online'.

![example_images](example_images/execution.gif)

## Exemplos:

### Argumentos

O script aceita argumentos opcionais

#### Range
Seleciona para baixar os episodios entre o range especificado.
`-r range  O range de episodios q quer baixar`
```Python anime.py -r 1-5 fate```

#### Diretorio
Especifica o diretorio onde você quer salvar os eps.
`-d diretorio O caminho da pasta onde os animes serão baixados`
```python anime.py -d E:/animes/Nisemonogatari nisemonogatari```