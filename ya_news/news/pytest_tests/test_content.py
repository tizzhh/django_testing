from django.conf import settings
from django.urls import reverse

HOME_URL = reverse('news:home')


def test_news_count(client, news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count <= settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list):
    response = client.get(HOME_URL)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_order(client, comment_list, news_with_comment_id):
    url = reverse('news:detail', args=news_with_comment_id)
    response = client.get(url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


def test_anonymous_client_has_no_form(client, news_with_comment_id):
    url = reverse('news:detail', args=news_with_comment_id)
    response = client.get(url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, news_with_comment_id):
    url = reverse('news:detail', args=news_with_comment_id)
    response = admin_client.get(url)
    assert 'form' in response.context
