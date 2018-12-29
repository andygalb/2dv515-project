import urllib3
from bs4 import BeautifulSoup
import string

class Scraper:

    #File constants
    downloads_folder = 'downloads'
    links_folder = 'links'
    words_folder = 'words'

    #Base URL to add to change links to absolute links
    base_url = "https://en.wikipedia.org"

    #Colon keywords to be disregarded
    negatives=["Wikipedia","Portal","Category","Talk","Help","File","Special"]

    url_list = []
    visited = []

    def __init__(self, root_url, download_limit):
        self.rootUrl = root_url
        self.downloadLimit = download_limit
        self.http = urllib3.PoolManager()

    def scrape(self):

        urllib3.disable_warnings()
        print("Root url:" + self.rootUrl)
        self.process_url(self.rootUrl)

        while len(self.visited) < self.downloadLimit:
            link = self.url_list.pop()
            self.process_url(link)

    def process_url(self, url):

        print("Processing:" + url)
        r = self.http.request('GET', url)
        web_content = r.data.decode("utf-8")
        soup = BeautifulSoup(web_content, 'html.parser')

        for link in soup.find_all('a'):
            if len(self.url_list) < self.downloadLimit and self.is_suitable_link(link):
                    self.url_list.insert(0, self.base_url + link.get('href'))

        f = open(self.downloads_folder+'/' + url.split('/')[-1], 'w')
        f.write(web_content)
        f.close

        self.extractLinks(r._request_url, soup)
        self.extract_words(r._request_url, soup)

        self.visited.append(url)
        return



    def extractLinks(self, url, soup):

        link_list = []

        for link in soup.body.find_all('a'):
            link_string = link.get('href')
            if self.is_suitable_link(link):
                    link_string = link_string.split("#")[0]
                    if not link_list.__contains__(link_string):
                        link_list.append(link_string)

        f = open(self.links_folder+'/' + url.split('/')[-1], 'w')
        for link in link_list:
            f.writelines(link + "\n")
        f.close()
        return



    def extract_words(self, url, soup):

        word_list = []
        text_array = []

        [s.extract() for s in soup('sup')]

        ptags = soup.body.find_all('p')

        for ptag in ptags:
            text = ptag.get_text()
            minor_text_array = text.split()
            for word in minor_text_array:
                text_array.append(word)

        for word in text_array:
            remove = dict.fromkeys(map(ord, '\n ' + string.punctuation))
            trimmed_word = word.strip()
            t = trimmed_word.translate(remove)
            word_list.append(t.lower())

        f = open(self.words_folder+'/' + url.split('/')[-1], 'w')
        for word in word_list:
            f.writelines(word + " ")
        f.close()
        return

# Filter methods to ensure link suitability etc.
# *****************************************************************************#

    def is_suitable_link(self, link):

        link_string = link.get('href')

        if link_string is None:
            return False
        if link_string[0] == "#":
            return False
        if not self.link_links_to_other_wikipedia_page(link_string):
            return False
        if self.link_contains_colon_operators(link_string):
            return False
        return True

    def link_links_to_other_wikipedia_page(self, link):

        if link.split("/")[1] == "wiki":
            return True
        return False

    def link_contains_colon_operators(self, link_string):

        split_link_string = link_string.split("/")
        final_url_segment = split_link_string[2]
        split_final = final_url_segment.split(":")

        if len(split_final) > 0:
            if self.negatives.__contains__(split_final[0]):
                return True
        return False
