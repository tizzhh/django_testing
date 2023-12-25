from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, news_list, home_url):
    response = client.get(home_url)
    object_list = response.context.get('object_list', [])
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_list, home_url):
    response = client.get(home_url)
    object_list = response.context.get('object_list', [])
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_order(client, detail_url_with_comments):
    response = client.get(detail_url_with_comments)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = [comment.created for comment in news.comment_set.all()]
    sorted_comments = sorted(all_comments)
    assert sorted_comments == all_comments


def test_anonymous_client_has_no_form(client, detail_url_with_comments):
    response = client.get(detail_url_with_comments)
    assert 'form' not in response.context


def test_authorized_client_has_form(admin_client, detail_url_with_comments):
    response = admin_client.get(detail_url_with_comments)
    assert 'form' in response.context
    # из-за проверки выше .get() для проверки key-error не требуется, думаю
    assert isinstance(response.context['form'], CommentForm)
