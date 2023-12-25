from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, news_list, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list, home_url):
    response = client.get(home_url)
    assert 'object_list' in response.context
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_order(client, detail_url, comment_list):
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = [comment.created for comment in news.comment_set.all()]
    sorted_comments = sorted(all_comments)
    assert sorted_comments == all_comments


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_url):
    response = admin_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
