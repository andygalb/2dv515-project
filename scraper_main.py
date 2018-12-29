import scraper

#rootUrl = 'https://en.wikipedia.org/wiki/Tim_Berners-Lee'
rootUrl = 'https://en.wikipedia.org/wiki/Ada_Lovelace'

scraper = scraper.Scraper(rootUrl, 5)
scraper.scrape()




