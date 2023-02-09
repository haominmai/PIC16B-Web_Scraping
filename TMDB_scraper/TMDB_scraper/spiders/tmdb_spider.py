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
        cast_crew = response.css('p.new_button a::attr(href)').get()
        #this gives us '/movie/157336-interstellar/cast'
        
        cast_crew = response.urljoin(cast_crew)
        # now we have 'https://www.themoviedb.org/movie/157336-interstellar/cast'
        
        yield scrapy.Request(cast_crew, callback=self.parse_full_credits)
        
    def parse_full_credits(self, response):
        '''
        start on the Cast & Crew page,
        yield a scrapy request for each actor (not crew) listed on the page
        '''
        
        # address to actor part
        actor = response.css('ol.people.credits')
        actor = actor.css('div.info')
        
        # get the link to each actor 
        actor_link = actor.css('a::attr(href)').getall()
        # it gives something like '/person/10297-matthew-mcconaughey'
        
        for link in actor_link:
            
            # get the whole link
            whole_link = response.urljoin(link)
            # we would get something like 'https://www.themoviedb.org/person/10297-matthew-mcconaughey'
            
            yield scrapy.Request(whole_link, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        '''
        start on the page of an actor,
        yield a dictionary for each of the movies 
        or TV shows on that actor has worked
        with two key-value pairs
        '''
        
        # extract actor's name from title 
        actor_name = response.css('h2.title a::text').get()
        
        # get the list of all movies or TV shows on which that actor has worked
        worked_list = response.css('div.credits_list a.tooltip bdi::text').getall()
        
        for movie_or_TV_name in worked_list:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}