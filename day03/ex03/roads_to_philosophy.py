import sys
import requests
from bs4 import BeautifulSoup


class RoadsToPhilosophy:

    URL = 'https://en.wikipedia.org/'

    def __init__(self):
        self.prev = []

    def search_wikipedia(self, path: str) -> None:
        url = self.URL + path
        try:
            res = requests.get(url=url)
            res.raise_for_status()
        except requests.HTTPError as e:
            if res.status_code == 404:
                return print("It's a dead end !")
            return print(e)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.find(id='firstHeading').text
        if title in self.prev:
            return print("It leads to an infinite loop !")
        self.prev.append(title)
        print(title)
        if title == 'Philosophy':
            return print("{} roads from {} to Philosophy".format(len(self.prev), self.prev[0] if len(self.prev) > 0 else 'Philosophy'))
        content = soup.find(id='mw-content-text')
        all_links = content.select('p > a')
        for link in all_links:
            if (link.get('href') is not None
                    and link['href'].startswith('/wiki/')
                    and not link['href'].startswith('/wiki/Wikipedia:')
                    and not link['href'].startswith('/wiki/Help:')):
                return self.search_wikipedia(link['href'])
        return print("It leads to a dead end !.")


def main():
    wiki = RoadsToPhilosophy()
    if len(sys.argv) != 2:
        return print('wrong argument count!')
    wiki.search_wikipedia('/wiki/' + sys.argv[1])


if __name__ == '__main__':
    main()
