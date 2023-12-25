from http import HTTPStatus

from pytest_django.asserts import assertFormError, assertRedirects

from news.forms import WARNING
from news.models import Comment


def test_anonymous_user_cant_create_comment(
        client, comment_form_data, detail_url
):
    client.post(detail_url, data=comment_form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(
        author_client, comment_form_data, news, author, detail_url
):
    response = author_client.post(detail_url, data=comment_form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(reader_client, bad_words_data, detail_url):
    response = reader_client.post(detail_url, data=bad_words_data)
    assertFormError(response, 'form', 'text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client, detail_url, delete_url):
    response = author_client.delete(delete_url)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(reader_client, delete_url):
    response = reader_client.delete(delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(
        author_client,
        comment_form_data,
        comment,
        news,
        author,
        edit_url,
        detail_url,
):
    prev_time = comment.created
    response = author_client.post(edit_url, data=comment_form_data)
    assertRedirects(response, f'{detail_url}#comments')
    comment.refresh_from_db()
    new_time = comment.created
    assert comment.text == comment_form_data['text']
    assert comment.author == author
    assert comment.news == news
    assert prev_time == new_time


def test_user_cant_edit_comment_of_another_user(
        reader_client, comment_form_data, comment, edit_url
):
    response = reader_client.post(edit_url, data=comment_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_from_db = Comment.objects.get()
    assert comment_from_db.text == comment.text
    assert comment_from_db.author == comment.author
    assert comment_from_db.news == comment.news
    assert comment_from_db.created == comment.created
