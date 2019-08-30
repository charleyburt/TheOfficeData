# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['officequotes.net']
    start_urls = ['http://www.officequotes.net/no1-01.php']

    def parse(self, response):

        season = response.css('td[bgcolor="#FFF8DC"] b:first-of-type::text').get().split('-')[0]
        episode = response.css('td[bgcolor="#FFF8DC"] b:first-of-type::text').get().split('-')[1]

        title = response.css('td[bgcolor="#FFF8DC"] b:nth-of-type(2)::text').get()

        written_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[3].strip()
        directed_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[4].strip()
        transcribed_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[5].strip()

        # yield as a dictionary
        new_episode = {
            'season': season,
            'episode': episode,
            'title': title,
            'written_by': written_by,
            'directed_by': directed_by,
            'transcribed_by': transcribed_by,
            'scenes': {}
        }

        # use css selectors to get season and episode


        #loop through the response object and append the quotes to the scenes variable

            # new_scene = {
            #     'scene_number': 0,
            #     'quotes': {}
            # }

            quotes = response.css('.quote')
            quotes_text = response.css('.quote::text').getall()
            quotes_prepared = [q.strip() for q in quotes_text if q.strip() != '']

            for index, quote in quotes:
                author = quote.css('b:first-of-type::text').get()[:-1]
                quote = quotes_prepared[index]
                new_scene['quotes'][index]({
                    'author': author,
                    'quote': quote
                })

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
