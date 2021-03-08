import feedparser


url_news = "https://news.tut.by/rss/index.rss"


def get_rss(url):
    return feedparser.parse(url)


def get_info_from_source(rss_news_set):
    new_set = []
    for item_news in rss_news_set:
        new_set.append({
            'title': item_news['title'],
            'source_link': item_news['links'][0]['href'],
            'image_link': item_news['links'][1]['href'],
            'tag_name': item_news['tags'][0]['term'],
            'tag_link': item_news['tags'][0]['scheme']
        })
    return new_set


def get_latest_news():
    news_feed = get_rss(url_news)
    news_set1 = get_info_from_source(news_feed.entries[:2])
    news_set2 = get_info_from_source(news_feed.entries[3:5])
    return news_set1, news_set2
