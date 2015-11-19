from flask import Flask, render_template
import feedparser
import random
from bs4 import BeautifulSoup
app = Flask(__name__)

DEFAULT_FEED = 'main'

def get_feed(url):
    return feedparser.parse(url).entries

def make_soup(item):
    return BeautifulSoup(item.summary, 'html.parser')

@app.route('/')
def respond():
    return hello_world(DEFAULT_FEED)

@app.route('/<path:path>')
def hello_world(path):
    url = 'https://www.texastribune.org/feeds/'+path
    items = get_feed(url)
    struct_items = []
    for item in items:
        soup = make_soup(item)
        img = soup.find('img') or {}
        if not img:
            continue
        struct_items.append({
            'headline': item.title,
            'img': img.get('src'),
            'date': ' '.join(item.published.split(' ')[:4])
        })
    return render_template('index.html', items=struct_items)

if __name__ == '__main__':
    app.run(debug=True)
