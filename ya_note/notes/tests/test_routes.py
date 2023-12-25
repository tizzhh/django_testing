from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.tests.basefixture import BaseTest, URLS

User = get_user_model()


class TestRoutes(BaseTest):
    def test_pages_availabiliy(self):
        urls_clients_statuses = (
            # выглядит как-то криво, но что-то лучше придумать не вышло
            # думал сделать через zip() и 3 списка, но все равно криво
            (URLS['home_url'], self.client, HTTPStatus.OK),
            (URLS['login_url'], self.client, HTTPStatus.OK),
            (URLS['logout_url'], self.client, HTTPStatus.OK),
            (URLS['signup_url'], self.client, HTTPStatus.OK),
            (URLS['list_url'], self.author_client, HTTPStatus.OK),
            (URLS['success_url'], self.author_client, HTTPStatus.OK),
            (URLS['add_url'], self.author_client, HTTPStatus.OK),
            (URLS['edit_url'], self.author_client, HTTPStatus.OK),
            (URLS['detail_url'], self.author_client, HTTPStatus.OK),
            (URLS['delete_url'], self.author_client, HTTPStatus.OK),
            (URLS['edit_url'], self.reader_client, HTTPStatus.NOT_FOUND),
            (URLS['detail_url'], self.reader_client, HTTPStatus.NOT_FOUND),
            (URLS['delete_url'], self.reader_client, HTTPStatus.NOT_FOUND),
        )
        for url, client, expected_status in urls_clients_statuses:
            with self.subTest(
                url=url, client=client, expected_status=expected_status
            ):
                response = client.get(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirect_for_anonymous_user(self):
        urls = (
            URLS['edit_url'],
            URLS['detail_url'],
            URLS['delete_url'],
            URLS['add_url'],
            URLS['list_url'],
            URLS['success_url'],
        )

        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{URLS["login_url"]}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
