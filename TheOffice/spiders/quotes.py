# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['officequotes.net']
    start_urls = ['http://www.officequotes.net/no1-01.php']

    def parse(self, response):

        # pull stuff out here

        # yield as a dictionary
        new_episode = {
            'season': 0,
            'episode': 0,
            'scenes': {}
        }

        # use css selectors to get season and episode


        #loop through the response object and append the quotes to the scenes variable

            # new_scene = {
            #     'scene_number': 0,
            #     'quotes': {}
            # }


            # for index, quote in quotes:
            #
            #     new_scene['quotes'][index]({
            #         'author': 'Jim',
            #         'quote': 'kljdfa'
            #     })

        new_episode['scenes'][new_scene['scene_number']] = new_scene

        yield new_episode

        # Take current url, split by / and get the last part (the page name, like asdf.php)
        current_page = str(response.request.url).split('/')[-1]
        # Get the first link that happens after our current link
        next_page = response.css(f'.navEp a[href="{current_page}"] ~ a:first-of-type::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

        # command line
        # scrapy crawl quotes -o filename.json
