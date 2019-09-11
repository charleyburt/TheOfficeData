# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['officequotes.net']
    start_urls = ['http://www.officequotes.net/no1-05.php']

    def parse(self, response):
        season, episode = response.css('td[bgcolor="#FFF8DC"] b:first-of-type::text').get().split(' - ')
        title = response.css('td[bgcolor="#FFF8DC"] b:nth-of-type(2)::text').get()
        written_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[3].strip()
        directed_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[4].strip()
        transcribed_by = response.css('td[bgcolor="#FFF8DC"]::text').getall()[5].strip()
        scenes = response.css('div.quote')

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

        # loop through scenes in episode
        for index, scene in enumerate(scenes):
            new_scene = {
                'scene_number': index + 1,
                'quotes': {}
            }

            scene_lines_text = scene.css('::text').getall()
            scene_lines_cleaned = [q.strip() for q in scene_lines_text if q.strip() != '']

            # loop through every other line in scene (which is the line with the author name)
            for index, text in enumerate(scene_lines_cleaned[::2]):
                if ':' in text[:]:
                    new_scene['quotes'][index] = {
                        'author': text[: ],
                        'quote': scene_lines_cleaned[(index * 2) + 1]
                    }


            # append new scene to episode
            new_episode['scenes'][new_scene['scene_number']] = new_scene

        yield new_episode

        # # Take current url, split by / and get the last part (the page name, like asdf.php)
        # current_page = str(response.request.url).split('/')[-1]

        # # Get the first link that happens after our current link
        # next_page = response.css(f'.navEp a[href="{current_page}"] ~ a::attr(href)').get()
        # if next_page:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        # # command line
        # # scrapy crawl quotes -o filename.json
