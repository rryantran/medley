import feedparser
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# parse the feed
d = feedparser.parse(
    'https://www.criterion.com/feeds/the-daily')

# test output
print(d.feed.title)
print(d.entries[0].title)
print(d.entries[0].author)
print(d.entries[0].published)
print(d.entries[0].link)
