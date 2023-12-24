import pytest
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='news title',
        text='news text',
    )
    return news


@pytest.fixture
def news_list(author):
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    news = News.objects.bulk_create(all_news)
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='comment text',
    )
    return comment


@pytest.fixture
def comment_list(news, author):
    now = timezone.now()
    all_comments = []
    for i in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Comment text {i}',
        )
        comment.created = now + timedelta(days=i)
        comment.save()
        all_comments.append(comment)
    return all_comments


@pytest.fixture
def news_id(news):
    return (news.pk,)


@pytest.fixture
def news_with_comment_id(news, comment):
    return (news.pk,)


@pytest.fixture
def comment_id(comment):
    return (comment.pk,)


@pytest.fixture
def comment_form_data():
    return {
        'text': 'new comment text'
    }
