# CrawlerPythonIPNArticules

## description

Genera la base de datos de la pagina web https://tesis.ipn.mx/ de la seccion posgrados, esta base de datos contiene los valores de las tesis, sus detalles y el archivo pdf. El archivo generado es un .json que contiene el nombre del pdf guardado. 

## environment (prerequisites)

	Python 3.7
	Scrapy 1.5.1
	Directory /Users/salgado/Desktop/articules/
	Works at Nov 8 2018

## files

1. settings.py : variables globales de configuracion, timeout de cada request, delay, pipelines, etc
2. items.py : atributos del objeto que se procesara (obtendra, guardara)
3. logfile.log: resultados at Nov 8 2018 con mas de 4000 elementos descargados
4. middlewares.py: Archivo generado automaticamente por scrapy
5. pipelines.py: Archivo que procesa cada elemento, ver metodo process_item, es llamado cuando se llega a la pagina correcta ver ipntesis_spider.py
6. ipntesis_spider.py: Contiene la definicion de la araña, es decir el trace que se debe realizar para obtener los datos

