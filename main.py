import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/')
def redirect_yt_chat():
    url = request.args.get('url', '')

    if not url.startswith('http') or not 'youtube.com' in url:
        return 'Invalid channel'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    each = None
    for each in soup.find_all('script'):
        if isinstance(each.contents, list) and len(each.contents) >= 1 and 'ytInitialData' in each.contents[0]:
            break
    if each:
        split = each.string.split('=', 1)
        initial_values = json.loads(split[1].strip().rstrip(';'))

        try:
            featured_video = initial_values['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer'][
                'content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0][
                'channelFeaturedContentRenderer']['items'][0]['videoRenderer']

            if featured_video['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['style'] == 'LIVE':
                return redirect(f"https://studio.youtube.com/live_chat?is_popout=1&v={featured_video['videoId']}")

        except KeyError:
            return 'No Live Stream'

    return 'No Live Stream'
