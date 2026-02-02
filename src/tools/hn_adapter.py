import httpx
from tools.base import SourceAdapter
from services.logger import get_logger

logger = get_logger('HackerNews')

HN_TOP = 'https://hacker-news.firebaseio.com/v0/topstories.json'
HN_ITEM = 'https://hacker-news.firebaseio.com/v0/item/{}.json'

class HackerNewsAdapter(SourceAdapter):
    def fetch_items(self, hours: int = 24):
        items = []
        try:
            with httpx.Client(timeout=10) as client:
                ids = client.get(HN_TOP).json()[:30]
                for item_id in ids:
                    data = client.get(HN_ITEM.format(item_id)).json()
                    if not data or 'title' not in data:
                        continue

                    items.append({
                        'source': 'hackernews',
                        'title': data['title'],
                        'content': data.get('text', ''),
                        'url': f'https://news.ycombinator.com/item?id={item_id}'
                    })

            logger.info(f'Fetched {len(items)} items from Hacker News')
        except Exception as e:
            logger.error(f'HN fetch failed: {e}')

        return items
