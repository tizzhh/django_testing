from django.urls import reverse

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
