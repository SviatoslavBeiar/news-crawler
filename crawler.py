import feedparser
from newspaper import Article as NewsArticle
from transformers import pipeline
from datetime import datetime
import logging

from models import SessionLocal, Article, Log
import config


logging.basicConfig(
    filename='crawler.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)


topic_classifier = pipeline(
    'zero-shot-classification',
    model='facebook/bart-large-mnli'
)
sentiment_analyzer = pipeline(
    'sentiment-analysis'
)
LABELS = ['Politics', 'Economics', 'Sports']


def fetch_and_store():
    session = SessionLocal()
    total, errors = 0, []

    for feed_url in config.RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            try:
                url = entry.link
                if session.query(Article).filter_by(url=url).first():
                    continue


                news = NewsArticle(url)
                news.download()
                news.parse()
                text = news.text or ""


                topic_res = topic_classifier(
                    text,
                    candidate_labels=LABELS,
                    truncation=True,
                    max_length=512
                )
                topic = topic_res['labels'][0]


                sentiment_res = sentiment_analyzer(
                    text,
                    truncation=True,
                    max_length=512
                )
                sentiment = sentiment_res[0]['label'].lower()

                art = Article(
                    title=news.title,
                    url=url,
                    published_at=(
                        datetime.fromtimestamp(news.publish_date.timestamp())
                        if news.publish_date else None
                    ),
                    content=text,
                    category=topic,
                    sentiment=sentiment
                )
                session.add(art)
                session.commit()
                total += 1

            except Exception as e:
                logging.error(f"Error processing {entry.link}: {e}")
                errors.append(f"{entry.link}: {e}")


    log = Log(
        job_name='fetch_and_store',
        articles_fetched=total,
        errors='; '.join(errors)
    )
    session.add(log)
    session.commit()
    session.close()


if __name__ == '__main__':
    fetch_and_store()
