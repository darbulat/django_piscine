from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from magazine.models import UserFavouriteArticle, Article


class LoginRequiredTest(TestCase):

    def register_user(self):
        data = {'username': 'admin', 'password1': 'admin123ADMIN', 'password2': 'admin123ADMIN'}
        self.client.post(reverse('register'), data=data)
        self.client.login(username='admin', password='admin123ADMIN')
        user = User.objects.get(username='admin')
        return user

    def test_not_auth_user(self):
        response = self.client.post(reverse('add_to_favourite'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('favourite'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('publications'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('publish'))
        self.assertEqual(response.status_code, 302)

    def test_registration_by_registered_user(self):
        self.register_user()
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 302)

    def test_add_favourite_twice(self):
        user = self.register_user()
        data = {
            'title': 'title',
            'synopsis': 'synopsis',
            'content': 'content',
        }
        self.client.post(reverse('publish'), data=data)
        article = Article.objects.filter(title='title').first()
        self.client.post(reverse('add_to_favourite'), data={'article_id': article.id})
        ufa = UserFavouriteArticle.objects.filter(article=article.id, user=user.id)
        len_1 = len(ufa)
        self.client.post(reverse('add_to_favourite'), data={'article_id': article.id})
        ufa = UserFavouriteArticle.objects.filter(article=article.id, user=user.id)
        len_2 = len(ufa)
        self.assertLess(len_2, len_1)
