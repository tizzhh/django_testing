from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from notes.tests.basefixture import SLUG_ARG, URLS, BaseTest

User = get_user_model()


class TestNoteEditDelete(BaseTest):
    NEW_NOTE_TITLE = 'Новое название записки'
    NEW_NOTE_TEXT = 'Новый текст записки'
    NEW_NOTE_SLUG = 'new-slug'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.after_create_redirect = URLS['success_url']
        cls.edit_url = URLS['edit_url']
        cls.delete_url = URLS['delete_url']
        cls.add_url = URLS['add_url']
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': SLUG_ARG[0],
        }
        cls.new_form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NEW_NOTE_SLUG,
        }

    def test_author_can_delete_note(self):
        expected_notes_count = Note.objects.count() - 1
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, self.after_create_redirect)
        self.assertEqual(Note.objects.count(), expected_notes_count)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())

    def test_non_author_cant_delete_note(self):
        expected_notes_count = Note.objects.count()
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), expected_notes_count)
        self.assertTrue(Note.objects.filter(pk=self.note.pk).exists())

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_url, data=self.new_form_data
        )
        self.assertRedirects(response, self.after_create_redirect)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)
        self.assertEqual(self.note.author, self.author)
        self.assertEqual(self.note.slug, self.NEW_NOTE_SLUG)

    def test_non_author_cant_edit_note(self):
        response = self.reader_client.post(
            self.edit_url, data=self.new_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.NOTE_TITLE)
        self.assertEqual(self.note.text, self.NOTE_TEXT)
        self.assertEqual(self.note.author, self.author)
        self.assertEqual(self.note.slug, SLUG_ARG[0])

    def test_anon_user_cant_create_note(self):
        expected_notes_count = Note.objects.count()
        response = self.client.post(self.add_url)
        expected_url = f'{URLS["login_url"]}?next={self.add_url}'
        self.assertRedirects(response, expected_url)
        self.assertEqual(Note.objects.count(), expected_notes_count)

    def test_auth_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(response, self.after_create_redirect)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.slug, SLUG_ARG[0])
        self.assertEqual(note.author, self.author)

    def test_slug_from_title(self):
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertRedirects(response, self.after_create_redirect)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(self.NOTE_TITLE))
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.author)

    def test_not_unique_slug(self):
        expected_notes_count = Note.objects.count()
        response = self.author_client.post(self.add_url, data=self.form_data)
        self.assertFormError(
            response,
            form='form',
            field='slug',
            errors=f'{SLUG_ARG[0]}{WARNING}',
        )
        self.assertEqual(Note.objects.count(), expected_notes_count)
