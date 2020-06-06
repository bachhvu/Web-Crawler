import scrapy
import re
import mysql.connector as mariadb
import datetime
now = datetime.datetime.now()
import hashlib

mariadb_connection = mariadb.connect(user='root', password='Bach98110', database='policy')
cursor = mariadb_connection.cursor()

class QuotesSpider(scrapy.Spider):
    name = "spider"
    
    def start_requests(self):
        urls = [line.rstrip('\n') for line in open('URL.txt')]
        for url in urls:
            print(urls)
            yield scrapy.Request(url, self.parseURL)

    def parseURL(self, response):
        link = response.css('a::attr(href)').re(r'^.*privacy.*$')
        for i in link:
            if len (i) > 0:
                yield response.follow(i, self.parse)
                yield {"link":i}

    def parse(self, response):
        page = response.url
        hash = hashlib.sha256(response.body).hexdigest()
        try:
            cursor.execute("INSERT INTO policy (URL,DateTime,Hash,Policy) VALUES (%s,%s,%s,%s)", (page,now,hash,response.body))
        except mariadb.Error as error:
            print("Error: {}".format(error))
        mariadb_connection.commit()

    

        
    



        
    
    
    
            
        