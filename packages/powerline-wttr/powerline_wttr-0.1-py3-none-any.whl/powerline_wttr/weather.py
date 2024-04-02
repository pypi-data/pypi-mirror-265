import requests
from functools import lru_cache
import datetime

def fetch_weather_from_wttr_in(pl, city, format):
    url = ""
    if city == "":
        url = f"https://wttr.in/?format={format}"
    else:
        url = f"https://wttr.in/{city}?format={format}"
    response = requests.get(url, timeout=10.0)
    pl.debug(response.text.strip())
    return response.text.strip()

@lru_cache
def _weather(pl, city='', **kwargs):
    format=kwargs.get('format', '%l:+%c+%f+%h+%p+%P+%m+%w')
    weather = fetch_weather_from_wttr_in(pl, city, format)
    return [{
      'contents': weather,
      'highlight_groups': ['information:regular'],
    }]   

def get_ttl_hash(ttl):
    utime = datetime.datetime.now().timestamp()
    return round(utime / (ttl + 1))

def weather(*args, **kwargs):
  ttl = kwargs.get('ttl', 60*60)
  return _weather(*args, hash=get_ttl_hash(ttl), **kwargs)
