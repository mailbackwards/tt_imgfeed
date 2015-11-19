from flask import Flask, render_template
import feedparser
import random
from bs4 import BeautifulSoup
app = Flask(__name__)

DEFAULT_SECTION = 'economy'

def get_feed(url):
    return feedparser.parse(url).entries

def make_soup(item):
    return BeautifulSoup(item.summary, 'html.parser')

@app.route('/<path:section>')
def hello_world(section):
    if not section:
        section = DEFAULT_SECTION
    url = 'https://www.texastribune.org/feeds/sections/'+section
    items = get_feed(url)
    struct_items = []
    for item in items:
        soup = make_soup(item)
        img = soup.find('img') or {}
        struct_items.append({
            'headline': item.title,
            'img': img.get('src', 'http://www.fillmurray.com/200/300'),
            'date': ' '.join(item.published.split(' ')[:4])
        })
    return render_template('index.html', items=struct_items)

if __name__ == '__main__':
    app.run(debug=True)
