import random

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate
from .models import IBAN


IBAN_VALID = [
    'ES4801287757815211672272',
    'ES7714653685388769844773',
    'ES3001821984159473684262',
    'BE35978495651737',
    'DE21500105176956912567',
    'DE09500105174983549148',
]

# TODO: add more cases, maybe use a fuzzy generator like
# https://factoryboy.readthedocs.io/en/latest/fuzzy.html
IBAN_INVALID = [
    '',
    'ES4801287757111111111111',
    'invalid',
]


class IBANTests(APITestCase):
    def setUp(self):
        super().setUp()

        # admin user
        self.admin = User.objects.create(is_superuser=True, is_staff=True, username='admin')
        self.admin.set_password('123')
        self.admin.save()

        # test user
        self.user = User.objects.create(username='testuser', first_name='test', last_name='user')
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        super().tearDown()

        User.objects.all().delete()
        IBAN.objects.all().delete()

    def _ok_test(self, test, *args, **kwargs):
        test(*args, **kwargs)
        IBAN.objects.all().delete()

    def _fail_test(self, test, *args, **kwargs):
        try:
            test(*args, **kwargs)
        except AssertionError:
            IBAN.objects.all().delete()
            return

        IBAN.objects.all().delete()
        raise AssertionError

    def test_create(self, user=None):
        if user is None:
            user = self.admin
        self.client.login(username=user.username, password='123')

        number = random.choice(IBAN_VALID)
        url = reverse('iban-list')
        data = {
            'number': number,
            'user': {
                'first_name': 'test',
                'last_name': 'user',
            },
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IBAN.objects.count(), 1)
        self.assertEqual(IBAN.objects.get().number, number)

    def test_list(self, user=None):
        if user is not None:
            self.client.login(username=user.username, password='123')

        # populate some IBANS
        for number in IBAN_VALID:
            IBAN.objects.create(user=self.user, number=number)

        url = reverse('iban-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(IBAN.objects.count(), len(IBAN_VALID))

    def test_delete(self, user=None):
        if user is None:
            user = self.admin
        self.client.login(username=user.username, password='123')

        # populate some IBANS
        for number in IBAN_VALID:
            IBAN.objects.create(user=self.user, number=number)

        url = reverse('iban-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(IBAN.objects.count(), len(IBAN_VALID))

        url = reverse('iban-detail', kwargs={'pk': IBAN.objects.first().pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('iban-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(IBAN.objects.count(), len(IBAN_VALID) - 1)

    def test_update(self, user=None):
        if user is None:
            user = self.admin
        self.client.login(username=user.username, password='123')

        # populate some IBANS
        number = random.choice(IBAN_VALID)
        number2 = random.choice(IBAN_VALID)
        iban = IBAN.objects.create(user=self.user, number=number)

        url = reverse('iban-detail', kwargs={'pk': iban.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], iban.number)

        response = self.client.patch(url, data={'number': number2}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        iban = IBAN.objects.get(pk=iban.pk)
        self.assertEqual(iban.number, number2)

        data = {
            'number': number,
            'user': {
                'first_name': 'John',
                'last_name': 'Doe',
            },
        }

        response = self.client.put(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        iban = IBAN.objects.get(pk=iban.pk)
        self.assertEqual(iban.number, number)
        self.assertEqual(iban.user.first_name, 'John')
        self.assertEqual(iban.user.last_name, 'Doe')

    def test_permissions(self):
        self._ok_test(self.test_list, None)
        self._ok_test(self.test_list, self.admin)
        self._ok_test(self.test_list, self.user)

        self._ok_test(self.test_create, self.admin)
        self._fail_test(self.test_create, self.user)

        self._ok_test(self.test_delete, self.admin)
        self._fail_test(self.test_delete, self.user)

        self._ok_test(self.test_update, self.admin)
        self._fail_test(self.test_update, self.user)
