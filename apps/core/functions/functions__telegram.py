import urllib.request
import urllib.parse
from project.settings import TELEGRAM_GET_LINK

def SendMessage(msg):
    msg = urllib.parse.quote(msg)
    url = TELEGRAM_GET_LINK + msg
    contents = urllib.request.urlopen(url).read()
    return contents