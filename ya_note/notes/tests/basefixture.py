from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class BaseTest(TestCase):
    NOTE_TITLE = 'Название записки'
    NOTE_TEXT = 'Текст записки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='author')
        cls.reader = User.objects.create(username='reader')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            text=cls.NOTE_TEXT,
            slug=SLUG_ARG[0],
            author=cls.author,
        )


SLUG_ARG = ('test_slug',)
URLS_DATA_WITHOUT_ARG = {
    'home_url': 'notes:home',
    'login_url': 'users:login',
    'logout_url': 'users:logout',
    'signup_url': 'users:signup',
    'list_url': 'notes:list',
    'success_url': 'notes:success',
    'add_url': 'notes:add',
}
URLS = {key: reverse(val) for key, val in URLS_DATA_WITHOUT_ARG.items()}

URLS_DATA_WITH_ARG = {
    'edit_url': 'notes:edit',
    'detail_url': 'notes:detail',
    'delete_url': 'notes:delete',
}

URLS.update(
    {
        key: reverse(val, args=SLUG_ARG)
        for key, val in URLS_DATA_WITH_ARG.items()
    }
)
