#!/usr/bin/env python
# coding: utf-8

# In[1]:


import scrapy

class apmblog(scrapy.Spider):
    name = 'apm_blog'
    allowed_domains = ['scoutapm.com']
    start_urls = ['https://scoutapm.com/blog/categories/engineering']
    custom_settings = {"FEEDS":{"tmp/apm_blog.csv":{"format":"csv"}}}
    
    def parse(self,response):
        posts = response.xpath("//div[@class='post-partial']")
        for post in posts:
            link = post.css('a').attrib['href']
            url = response.urljoin(link)
            yield scrapy.Request(url = url, callback= self.parse_details)
         #pagination   
        next_page = response.xpath("//a[@class='glyphicon glyphicon-menu-right']").attrib['href']
        if next_page is not None:
            next_p = response.urljoin(next_page)
            yield scrapy.Request(url = next_p,callback=self.parse)
            
    def parse_details(self,response):
        name = response.css('h1::text').extract_first()
        author = response.css('a.author-link::text').extract_first()
        alink = response.css('a.author-link').attrib['href']
        author_link = response.urljoin(alink)
        post_link = response.url
        yield {
            'Name':name,
            'Author':author,
            'Author Profile':author_link,
            'Post': post_link
        }

