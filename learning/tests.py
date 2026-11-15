from django.contrib.auth import SESSION_KEY, get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    password = 'Study-Hub-Galaxy-47!'

    def signup_data(self, **overrides):
        return {
            'username': 'student',
            'password1': self.password,
            'password2': self.password,
            **overrides,
        }

    def test_guest_can_visit_home_and_account_forms(self):
        response = self.client.get(reverse('learning:home'))
        self.assertContains(response, 'Sign up')
        self.assertNotContains(response, 'Log out')
        for name in ('login', 'signup'):
            response = self.client.get(reverse(f'learning:{name}'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'csrfmiddlewaretoken')

    def test_signup_hashes_password_and_signs_student_in(self):
        response = self.client.post(reverse('learning:signup'), self.signup_data(), follow=True)
        self.assertRedirects(response, reverse('learning:home'))
        self.assertContains(response, 'Welcome, student!')
        self.assertContains(response, 'Log out')
        user = get_user_model().objects.get(username='student')
        self.assertNotEqual(user.password, self.password)
        self.assertTrue(user.check_password(self.password))
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    def test_invalid_signup_does_not_create_user(self):
        for overrides in ({'password2': 'different'}, {'password1': '123', 'password2': '123'}):
            response = self.client.post(reverse('learning:signup'), self.signup_data(**overrides))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertFalse(get_user_model().objects.exists())

    def test_duplicate_username_is_rejected(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        response = self.client.post(reverse('learning:signup'), self.signup_data())
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_and_logout(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        response = self.client.post(reverse('learning:login'), {
            'username': 'student', 'password': self.password,
        }, follow=True)
        self.assertRedirects(response, reverse('learning:home'))
        self.assertContains(response, 'Welcome, student!')
        response = self.client.post(reverse('learning:logout'), follow=True)
        self.assertRedirects(response, reverse('learning:home'))
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertNotContains(response, 'Welcome, student!')

    def test_wrong_password_is_rejected(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        response = self.client.post(reverse('learning:login'), {
            'username': 'student', 'password': 'wrong',
        })
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_login_next_accepts_local_url_and_rejects_external_url(self):
        get_user_model().objects.create_user(username='student', password=self.password)
        for target, expected in (
            (reverse('learning:science'), reverse('learning:science')),
            ('https://example.com/', reverse('learning:home')),
        ):
            response = self.client.post(reverse('learning:login'), {
                'username': 'student', 'password': self.password, 'next': target,
            })
            self.assertRedirects(response, expected)

    def test_signed_in_student_cannot_create_another_account(self):
        user = get_user_model().objects.create_user(username='student', password=self.password)
        self.client.force_login(user)
        response = self.client.post(reverse('learning:signup'), self.signup_data(username='another'))
        self.assertRedirects(response, reverse('learning:home'))
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_account_posts_require_csrf_and_logout_requires_post(self):
        client = Client(enforce_csrf_checks=True)
        for name in ('signup', 'login', 'logout'):
            self.assertEqual(client.post(reverse(f'learning:{name}')).status_code, 403)
        user = get_user_model().objects.create_user(username='student', password=self.password)
        client.force_login(user)
        self.assertEqual(client.get(reverse('learning:logout')).status_code, 405)
        response = client.get(reverse('learning:home'))
        response = client.post(reverse('learning:logout'), {
            'csrfmiddlewaretoken': client.cookies['csrftoken'].value,
        })
        self.assertRedirects(response, reverse('learning:home'))
        self.assertNotIn(SESSION_KEY, client.session)
