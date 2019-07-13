import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    global thumbnail
    thumbnail = None
    start_urls = [
        'https://voaspecialenglish.blogspot.com/',
    ]

    def parse_next(self, response):
        global thumbnail
        yield {
            'title': response.css('h1.metadata__title::text').get(),
            'content': response.css('div.post-body').get(),
            'youtube': response.css('iframe::attr("src")').get(),
            'thumbnail': thumbnail
        }


    def parse(self, response):
        for quote in response.css('a.card__image'):
            next_page = quote.css('a.card__image::attr("href")').get()
            global thumbnail
            thumbnail = quote.css('img.card__img::attr("src")').get()
            if next_page is not None:
                yield response.follow(next_page, self.parse_next)
