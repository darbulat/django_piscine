import requests
import json
import dewiki
import sys


def request_wikipedia(page: str):
    url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "parse",
        "page": page,
        "prop": "wikitext",
        "format": "json",
        "redirects": "true"
    }

    res = requests.get(url=url, params=params)
    res.raise_for_status()
    data = json.loads(res.text)
    if data.get("error") is not None:
        raise Exception(data["error"]["info"])
    return dewiki.from_string(data["parse"]["wikitext"]["*"])


def main():
    if len(sys.argv) != 2:
        return print("Wrong number of arguments")
    try:
        wiki_data = request_wikipedia(sys.argv[1])
    except Exception as e:
        return print(e)
    with open(f"{sys.argv[1]}.wiki", "w") as f:
        f.write(wiki_data)


if __name__ == '__main__':
    main()
