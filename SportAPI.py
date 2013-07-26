import urllib2
import json


class SportAPI:
    
    api_key = None
    root_url = 'http://api.espn.com/v1/sports/'

    def __init__(self, api_key):
        self.api_key = api_key

    def get_news(self, sport, limit=10):
        url = self.root_url
        url += '%s/news/headlines?apikey=%s&limit=%s' \
                    % (sport, self.api_key, limit)
        data = json.loads(urllib2.urlopen(url).read())
        headlines = []
        for h in data.get('headlines', None):
            headlines.append(h.get('headline'))
        return headlines
