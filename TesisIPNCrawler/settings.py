
BOT_NAME = 'TesisIPNCrawler'

SPIDER_MODULES = ['TesisIPNCrawler.spiders']
NEWSPIDER_MODULE = 'TesisIPNCrawler.spiders'

ROBOTSTXT_OBEY = False
DOWNLOADER_TIMEOUT = 1200 #20 minutos maximo para descargar el pdf
DOWNLOAD_DELAY = 6
ITEM_PIPELINES = {
    'TesisIPNCrawler.pipelines.TesisipncrawlerPipeline': 300,
}
SPIDER_MIDDLEWARE = {
    'TesisIPNCrawler.middleware.middlewares.py'
}
