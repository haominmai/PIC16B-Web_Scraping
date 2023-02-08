# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/157336-interstellar']
    
     def parse(self,response):
        '''
        start on a movie page,
        navigate to the Cast & Crew page
    
        '''
        # our goal is: https://www.themoviedb.org/movie/157336-interstellar/cast

        # get link for cast & crew page
        cast_crew = response.css("a./movie/157336-interstellar/cast").attrib['href']
        cast_crew = response.urljoin(next_page)
        
        
        # call on parse_full_credits method
        yield scrapy.Request(cast_crew, callback=self.parsse_full_credits)
        
        