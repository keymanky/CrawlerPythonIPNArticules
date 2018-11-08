# -*- coding: utf-8 -*-

import scrapy
import uuid
import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class IpnTesisSpider(scrapy.Spider):

    name = 'ipntesis'
    path = '/Users/salgado/Desktop/articules/'

    urls = {}
    urls['articules'] = 'https://tesis.ipn.mx/handle/123456789/17551/browse?rpp=10143&sort_by=1&type=title&offset=0&etal=-1&order=ASC'
    urls['main'] = 'https://tesis.ipn.mx'

    def start_requests(self):

        """
            Metodo que scrapy ejecuta al iniciar, en esta se muestra el listado completo de articulos de posgrado ordenados por titulo
            :param
            :return: Nada, pero manda llamar la araña sig: abstractArticule
        """

        yield scrapy.Request(url= self.urls['articules'] , callback=self.abstractArticule, errback = self.errback_function)

    def abstractArticule(self, response):

        """
            Pagina del resumen del articulo
            :param response:
            :return: Nada, pero manda llamar la araña sig: getArticuleId
        """

        articules = response.css('.artifact-title a::attr(href)').extract()

        for item in articules:
            yield scrapy.Request( url= self.urls['main'] + item, callback=self.getArticuleId, errback = self.errback_function )


    def getArticuleId(self, response):

        """
            Pagina intermedia del articulo
            :param response:
            :return: Nada, pero manda llamar la araña sig: getArticuleDetails
        """

        url =  str (response.css('.item-view-toggle a::attr(href)').extract_first() )
        yield scrapy.Request( url=self.urls['main'] + url , callback=self.getArticuleDetails, errback = self.errback_function )

    def getArticuleDetails(self, response):

        """
            Obtiene todos los detalles del articulo y la url del pdf
            :param response:
            :return: Dicccionario Articulo y manda llamar "process_item" en pipelines.py ; al igual que la araña sig: downloadArticule con el uuid del archivo
        """
        
        url = response.css('.file-wrapper a::attr(href)').extract_first()

        with open(self.path + "traza.log", 'a') as f:
            f.write(str(url) + "\n")
        f.close()

        articule = {}
        articule['title'] = response.css('h1::text').extract_first()
        namefile = str( uuid.uuid1() ) + ".pdf"
        articule['file'] = namefile
        articule['url'] = self.urls['main'] + url
        articule['xmlproperties'] = response.css('table').extract_first()

        #Dentro de xmlproperties tenemos algo de la forma: '<table xmlns:i18n="http://apache.org/cocoon/i18n/2.1" xmlns="http://di.tamu.edu/DRI/1.0/" xmlns:oreatom="http://www.openarchives.org/ore/atom/" xmlns:ore="http://www.openarchives.org/ore/terms/" xmlns:atom="http://www.w3.org/2005/Atom" class="ds-includeSet-table detailtable"><tr class="ds-table-row odd "> <td class="label-cell">dc.contributor.author</td>   <td></td>   <td></td></tr><tr class="ds-table-row even ">   <td class="label-cell">dc.creator</td>  <td>2007-11</td>    <td></td></tr><tr class="ds-table-row odd ">    <td class="label-cell">dc.date.accessioned</td> <td>2008-11-26T19:22:29Z</td>   <td></td></tr><tr class="ds-table-row even ">   <td class="label-cell">dc.date.available</td>   <td>2008-11-26T19:22:29Z</td>   <td></td></tr><tr class="ds-table-row odd ">    <td class="label-cell">dc.date.issued</td>  <td>2008-11-26T19:22:29Z</td>   <td></td></tr><tr class="ds-table-row even ">   <td class="label-cell">dc.identifier.citation</td>  <td>Salgado Sota, Hilda Margarita. (2007). Conteo: una propuesta didáctica y su análisis (Maestría en Ciencias en Matemática Educativa), Instituto Politécnico Nacional, Centro de Investigación en Ciencia Aplicada y Tecnología Avanzada, Unidad Legaria, México.</td>    <td>es</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dc.identifier.uri</td>   <td>http://tesis.ipn.mx/handle/123456789/1658</td>  <td></td></tr><tr class="ds-table-row even ">   <td class="label-cell">dc.description</td>  <td>Tesis (Maestría en Ciencias en Matemática Educativa), Instituto Politécnico Nacional, CICATA, Unidad Legaria, 2007, 1 archivo PDF, (359 páginas). tesis.ipn.mx</td> <td>es</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dc.description.abstract</td> <td>RESUMEN: En el aprendizaje de las matemáticas se suelen observar problemas debido a la complejidad de los conceptos involucrados por su alto nivel de abstracción. Se han detectado problemas en el aprendizaje de los conceptos asociados al tema de conteo y en la adquisición de las técnicas de conteo. Dos conceptos básicos de conteo son el de la ordenación y la combinación. Estos conceptos sirven para contar secuencias que cumplen ciertas características como orden y repetición. Dichas características representan una gran dificultad para los estudiantes en el proceso de adquisición de estos conceptos. Esta tesis hace una propuesta didáctica para el aprendizaje de las ordenaciones y combinaciones apoyada en una teoría que centra su atención en las construcciones mentales necesarias para la adquisición del saber matemático. Dicha teoría se denomina APOE. En esta tesis se hace un análisis de la puesta en práctica de la propuesta didáctica con estudiantes de nivel universitario y en correspondencia con el marco teórico escogido. Se presenta dicho análisis y los resultados obtenidos, a partir del trabajo de los estudiantes con la propuesta realizada. Se hizo una descomposición genética de los conceptos de ordenación y combinación con las construcciones mentales que los alumnos pueden desarrollar para su aprendizaje. Basados en esta descomposición se diseñaron unas secuencias con las cuales se pretende inducir a los alumnos a hacer dichas construcciones. Se hizo el análisis de los resultados obtenidos lo que permitió refinar la descomposición y diseñar nuevas secuencias. Las secuencias utilizadas ayudaron a los alumnos a efectuar las construcciones mentales que se propusieron y llevaron a un mejor aprendizaje. Esta descomposición resuelve parte del tema de conteo (ordenación y combinación) por lo queda otra parte del tema para una futura investigación.</td>    <td>es</td></tr><tr class="ds-table-row even "> <td class="label-cell">dc.description.abstract</td> <td>ABSTRACT: Learning mathematics often causes problems to students. Given the complexity of the concepts involved and their high level of abstraction, their learning becomes a difficult task. Problems arise in the learning of the concepts of counting and in the acquisition of the techniques of counting. Two basic concepts in counting are permutations and combinations. These concepts are used to count sequences that have certain characteristics like order and repetition. Such characteristics are a source of difficulty for students in the process of construction of these concepts. This thesis considers a didactical approach for the learning of permutations and combinations based in a theory that centers its attention in the mental constructions that are necessary for the construction of mathematical concepts. This theory is called APOS. The didactical design was used to teach counting to students at the university level. Their problem solving strategies were analyzed according to the chosen theory. The analysis and the results from the work done by the students are presented and discussed. A genetic decomposition of the concepts of permutation and combination was designed by making hypothesis about the mental constructions that students may develop in their learning. Based on this decomposition some didactical sequences were designed with the idea to provide opportunities for the students to reflect and make the necessary abstractions to construct these concepts. The results were analyzed leading to a refinement of the decomposition and the design of new sequences. The sequences used helped the students make the mental constructions that had been proposed and the result was that they performed better. This decomposition deals with a part of the counting theme (permutations and combinations) leaving another part for a future analysis.</td>  <td>en</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dc.language.iso</td> <td>es</td> <td>es</td></tr><tr class="ds-table-row even "> <td class="label-cell">dc.title</td>    <td>Conteo: una propuesta didáctica y su análisis</td>  <td>es</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dc.type</td> <td>Thesis</td> <td>es</td></tr><tr class="ds-table-row even "> <td class="label-cell">dc.contributor.advisor</td>  <td>Trigueros Gaisman, María</td>   <td></td></tr><tr class="ds-table-row odd ">    <td class="label-cell">dc.contributor.advisor</td>  <td>Lezama Andalón, Javier</td> <td></td></tr><tr class="ds-table-row even ">   <td class="label-cell">dcterms.subject</td> <td>Aprendizaje de las matemáticas</td> <td>es</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dcterms.subject</td> <td>Matemática discreta</td>    <td>es</td></tr><tr class="ds-table-row even "> <td class="label-cell">dcterms.subject</td> <td>Learning mathematics</td>   <td>en</td></tr><tr class="ds-table-row odd ">  <td class="label-cell">dcterms.subject</td> <td>Discrete Mathematics</td>   <td>en</td></tr>'

        #Envialos los datos al pipeline y continuamos con el sig, request
        yield articule
        yield scrapy.Request(
            url=self.urls['main'] + url,
            callback=self.downloadArticule,
            errback = self.errback_function,
            meta={'identificator': namefile } )
        

    def downloadArticule(self, response):

        """
            Descarga el archivo pdf y lo guarda con un nombre unico
            :param response: and meta['identificador'] que es el uuid con el que renombraremos el pdf
            :return:
        """

        with open( self.path + response.meta['identificator'] , 'wb') as f:
            f.write(response.body)
            
            
    def errback_function(self, failure):

        self.logger.error(repr(failure))

        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
            with open(self.path + "error.log", 'a') as f:
                f.write(str(datetime.datetime.now()) + ">>>" + response.body + "\n")

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)
            with open(self.path + "error.log", 'a') as f:
                f.write(str(datetime.datetime.now()) + ">>>" + request + "\n")

        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            with open(self.path + "error.log", 'a') as f:
                f.write(str(datetime.datetime.now()) + ">>>" + request + "\n")

        else:
            with open( self.path + "error.log" , 'a') as f:
                f.write(str(datetime.datetime.now()) + ">>>" + failure + "\n")