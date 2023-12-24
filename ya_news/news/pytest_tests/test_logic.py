from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
    client, news_id, comment_form_data
):
    url = reverse('news:detail', args=news_id)
    client.post(url, data=comment_form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
    author_client, news_id, comment_form_data, news, author
):
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data=comment_form_data)
    assertRedirects(response, f'{url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(admin_client, news_id):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = reverse('news:detail', args=news_id)
    response = admin_client.post(url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, comment_id, news_id):
    url = reverse('news:delete', args=comment_id)
    response = author_client.delete(url)
    news_url = reverse('news:detail', args=news_id)
    assertRedirects(response, f'{news_url}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(admin_client, comment_id):
    url = reverse('news:delete', args=comment_id)
    response = admin_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
    author_client, comment_id, news_id, comment_form_data, comment
):
    url = reverse('news:edit', args=comment_id)
    response = author_client.post(url, data=comment_form_data)
    news_url = reverse('news:detail', args=news_id)
    assertRedirects(response, f'{news_url}#comments')
    comment.refresh_from_db()
    assert comment.text == comment_form_data['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client, comment_id, comment_form_data, comment
):
    url = reverse('news:edit', args=comment_id)
    response = admin_client.post(url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get()
    assert comment_from_db.text == comment.text
