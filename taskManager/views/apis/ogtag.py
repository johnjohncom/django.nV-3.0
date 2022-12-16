import urllib.request
from bs4 import BeautifulSoup

from django.http import JsonResponse


def retrive(request):
    url = request.GET.get('url', '')

    ogtag = __parse_og_tags(url)

    return JsonResponse(ogtag)


def __parse_og_tags(url):
    with urllib.request.urlopen(url) as response:
        html_bytes = response.read()

    html_string = html_bytes.decode('utf-8')

    soup = BeautifulSoup(html_string, 'html.parser')

    og_tags = soup.find_all(
        'meta', {'property': lambda x: x and x.startswith('og:')})

    tags = {}
    for tag in og_tags:
        name = tag.get('property')
        content = tag.get('content')
        tags[name] = content
    
    return tags

