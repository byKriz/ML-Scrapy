from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    titulo = Field()
    precio = Field()
    ventas = Field()

class MercadoLibreCraeler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 10
    }
    download_delay = 5

    allowed_domains = ['listado.mercadolibre.com.ve', 'articulo.mercadolibre.com.ve']
    star_urls = ['https://listado.mercadolibre.com.ve/repuesto#D[A:repuesto]']

    rule = (
        # Paginación
        Rule(
            LinkExtractor(
                allow=r'/repuesto_Desde_'
            ), follow=True
        ),
        # Detalle de los Productos
        Rule(
            LinkExtractor(
                allow=r'/MLV-'
            ), follow=True, callback='parser_items'
        )
    )

    def parser_items(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()')
        item.add_xpath('ventas', '//span[@class="ui-pdp-subtitle"]/text()')

        yield item.load_item()

