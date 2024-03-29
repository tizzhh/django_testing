from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.basefixture import BaseTest, URLS

User = get_user_model()


class TestHomePage(BaseTest):
    def test_auth_client_has_add_button(self):
        response = self.reader_client.get(URLS['home_url'])
        self.assertIn(
            'href="/add/"', response.content.decode(encoding='utf-8')
        )

    def test_anon_client_has_no_add_button(self):
        response = self.client.get(URLS['home_url'])
        self.assertNotIn(
            'href="/add/"', response.content.decode(encoding='utf-8')
        )

    def test_notes_list_for_different_users(self):
        names = (
            (self.author_client, True),
            (self.reader_client, False),
        )
        for client, note_in_list in names:
            response = client.get(URLS['list_url'])
            self.assertIn('object_list', response.context)
            self.assertIs(
                self.note in response.context['object_list'], note_in_list
            )

    def test_pages_contains_form(self):
        urls = (
            URLS['add_url'],
            URLS['edit_url'],
        )
        for url in urls:
            response = self.author_client.get(url)
            self.assertIsInstance(response.context.get('form'), NoteForm)
