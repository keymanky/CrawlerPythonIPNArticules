# -*- coding: utf-8 -*-

import json
import os

class TesisipncrawlerPipeline(object):

    path = '/Users/salgado/Desktop/articules/'
    school = 'INSTITUTO POLITECNICO NACIONAL'
    grade = 'POSTGRADUATE'
    #grade = "BACHELOR'S DEGREE"

    def __init__(self):
        with open(self.path + 'result.json', 'a') as fp:
            fp.write('[')

    def __del__(self):
        with open(self.path + 'result.json', 'a') as fp:
            fp.seek(-1, os.SEEK_END)
            fp.truncate()
            fp.write(']')
            fp.close()

    def searchLanguage(self, text, htmldelimiter):

        """
            Busca el prefijo es, en que representan el idioma de la caracteristica, este prefijo esta dentro del nodo htmldelimiter en el texto
            :param text: Texto en donde buscara, htmldelimiter delimitador html donde se encuentra el prefijo del lenguaje
            :return: Spanish, English or NA
        """

        text = text.strip()

        index_language = text.find(htmldelimiter)
        if index_language < 0:
            return 'NA'

        length_delimiter = len(htmldelimiter)
        language = text[length_delimiter:  length_delimiter + 2].upper()

        if language == 'ES':
            return 'Spanish'
        elif language == 'EN':
            return 'English'
        else:
            return 'NA'

    def searchWord(self, text, word, htmldelimiter):

        """
            Busca el valor de la palabra "word" en el texto "text"; el valor (si es que se encuentra) esta entre las etiquetas "htmldelimiter" vecinas inmediatas al valor de "word".Por Ejemplo word: dc.date.accessioned, valor: 2008-11-26T19:22:29Z, delimitador:<td> texto:<td class="label-cell">dc.date.accessioned</td><td>2008-11-26T19:22:29Z</td>
            :param text: Texto en donde buscara, Word: Nombre de la caracterisitica a buscar, htmldelimiter: delimitador html entre el cual esta el "word" y "valor"
            :return: Diccionario word, valor
        """

        word = word.strip()
        end_htmldelimiter = "</" + htmldelimiter[1:]
        index_word = text.find(word)
        result = {}

        if index_word < 0:
            return ''

        index_end = text.find(end_htmldelimiter, index_word + len(word) + len(htmldelimiter) + len(end_htmldelimiter))

        # pe: author</td>    <td>Salgado Sota, Hilda Margarita , dc.creator</td> <td>2007-11, dc.identifier.uri</td> <td>http://tesis.ipn.mx/handle/123456789/1658 ...
        word_and_value = text[index_word: index_end]
        index_value = word_and_value.find(htmldelimiter)

        if index_value < 0:
            return ''

        # pe: Salgado Sota, Hilda Margarita, 2007-11, http://tesis.ipn.mx/handle/123456789/1658
        value = word_and_value[index_value + len(htmldelimiter):]

        if len(value) <= 0:
            return ''

        language = self.searchLanguage(text[index_end + len(end_htmldelimiter):], htmldelimiter)
        result[language] = value

        return result

    def findNth(self, haystack, needle, n):

        """
            Retorna la posicion de n ocurrencia de "needle" encontrada en el texto "haystack"
            :param haystack: Texto en donde buscara, needle: Elemento a buscar, n ocurrencia a considerar empieza en 0 para la primera
            :return: -1 en caso de no existir, intero que representa la posicion deseada
        """

        parts = haystack.split(needle, n + 1)

        if len(parts) <= n + 1:
            return -1
        return len(haystack) - len(parts[-1]) - len(needle)

    def open_spider(self, spider):
        print( 'ARAÑA ABIERTA :::::::' )

    def close_spider(self, spider):
        print( 'ARAÑA CERRADA :::::::' )

    def process_item(self, item, spider):

        """
            Metodo que se ejecuta cuando se encuentran los detalles del articulo (ver araña ipntesis_spider.py), procesa el html y lo guarda en un archivo con formato .json
            :param item: Diccionario con los elementos encontrados en el html, spider: Araña que la ejecuto
            :return:
        """

        print( 'ARAÑA CON ITEMS :::::::' )


        text = item['xmlproperties']
        text = text.replace('\n', '')
        text = text.replace('\t', '')

        find_words = ["dc.contributor.author",
                      "dc.creator",
                      "dc.date.available",
                      "dc.date.issued",
                      "dc.date.created",
                      "dc.identifier.citation",
                      "dc.identifier.uri",
                      "dc.description",
                      "dc.description.abstract",
                      "dc.type",
                      "dc.contributor.advisor",
                      "dcterms.subject"]

        articule = {}
        articule['title'] = item['title']
        articule['file'] = item['file']
        articule['url'] = item['url']
        articule['school'] = self.school
        articule['grade'] = self.grade

        descriptions = {}
        for item in find_words:

            #En caso de ser una caracteristica que se puede repetir n veces, ejecuta el filtrado n veces y lo almacena en formato json de la forma caracteriticaX donde x es 1...n
            if  item == "dc.description.abstract" or item =="dcterms.subject" or item == "dc.contributor.advisor":
                i = 0
                while 1:
                    n = self.findNth(text, item, i)
                    if n > 1:
                        descriptions[item + str(i+1)] = self.searchWord( text[n:] , item, "<td>")
                    else:
                        break
                    i+=1
            else:
                descriptions[item] = self.searchWord(text, item, "<td>")

        articule['details'] = descriptions

        with open(self.path + 'result.json', 'a') as fp:
            json.dump(articule , fp)
            fp.write(',')

        #return item
