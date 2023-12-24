from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

FIXTURE_NAMES = [
    'home_url',
    'detail_url',
    'edit_url',
    'delete_url',
    'login_url',
    'logout_url',
    'signup_url',
]
URLS = {name: pytest.lazy_fixture(name) for name in FIXTURE_NAMES}


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url, parametrized_client, expected_status',
    (
        (URLS['home_url'], pytest.lazy_fixture('client'), HTTPStatus.OK),
        (URLS['detail_url'], pytest.lazy_fixture('client'), HTTPStatus.OK),
        (URLS['login_url'], pytest.lazy_fixture('client'), HTTPStatus.OK),
        (URLS['logout_url'], pytest.lazy_fixture('client'), HTTPStatus.OK),
        (URLS['signup_url'], pytest.lazy_fixture('client'), HTTPStatus.OK),
        (
            URLS['edit_url'],
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK,
        ),
        (
            URLS['delete_url'],
            pytest.lazy_fixture('author_client'),
            HTTPStatus.OK,
        ),
        (
            URLS['edit_url'],
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND,
        ),
        (
            URLS['delete_url'],
            pytest.lazy_fixture('reader_client'),
            HTTPStatus.NOT_FOUND,
        ),
    ),
)
def test_pages_availability(url, parametrized_client, expected_status):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        URLS['edit_url'],
        URLS['delete_url'],
    ),
)
def test_redirect_for_anonymous_client(client, url, login_url):
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
