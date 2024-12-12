from celery import shared_task
from .scraping import crunchscrape, venturescrape, vergescrape
from .models import Article

@shared_task
def scrape_all():
    
    news_data = []

    crunch_data = crunchscrape()
    news_data.extend(crunch_data)

    venture_data = venturescrape()
    news_data.extend(venture_data)

    verge_data = vergescrape()
    news_data.extend(verge_data)

    for data in news_data:
        Article.objects.create(
            headline=data['headline'],
            link=data['link'],
            summary=data['summary'],
        )