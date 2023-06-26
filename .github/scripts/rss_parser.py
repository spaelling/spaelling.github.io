import feedparser
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pytz
from bs4 import BeautifulSoup

# Load RSS feed URLs
with open('.github/scripts/feeds.json', 'r') as f:
    feeds = json.load(f)

def try_strptime(s, fmts=['%d-%b-%y','%m/%d/%Y']):
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue

    return None # or reraise the ValueError if no format matched, if you prefer
    
# Fetch and parse RSS feeds
news_items = []
for feed_url in feeds:
    feed = feedparser.parse(feed_url)
    feed_title = feed.feed.title
    for entry in feed.entries:
        # Check if 'GMT' is in the date string
        if 'GMT' in entry.published:
            # Replace 'GMT' with '+0000'
            entry.published = entry.published.replace('GMT', '+0000')

        # Parse the publication date string into a datetime object
        published_datetime = try_strptime(entry.published, ['%a, %d %b %Y %H:%M:%S %z','%Y-%m-%dT%H:%M:%S%z','%Y-%m-%dT%H:%M:%S.%f%z'])
        # published_datetime = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')

        summary = entry.summary if 'summary' in entry else ''
        soup = BeautifulSoup(summary, "html.parser")
        summary = soup.get_text()  # Convert HTML escape characters to regular characters and remove HTML tags
        summary = summary.split('. ')[0]  # Split by '\n'
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': published_datetime,
            'summary': summary,
            'feed_title': feed_title
        })

# Sort news items by publication date
news_items.sort(key=lambda x: x['published'], reverse=True)

# Load Jinja2 template
env = Environment(loader=FileSystemLoader('.github/templates'))
template = env.get_template('news.html')

# Render new HTML page
with open('curated_news/index.html', 'w') as f:
    f.write(template.render(news_items=news_items))
