from django.test import TestCase
from datetime import date, timedelta
from .utils import calculate_streaks
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Habit



class StreakTests(TestCase):

    def test_empty_logs(self):

        result = calculate_streaks([])
        self.assertEqual(result['current_streak'], 0)
        self.assertEqual(result['longest_streak'], 0)

    def test_active_streak(self):
        today = date.today()

        dates = [today - timedelta(days=i) for i in range(5)]
        result = calculate_streaks(dates)
        self.assertEqual(result['current_streak'], 5)
        self.assertEqual(result['longest_streak'], 5)

    def test_broken_streak(self):
        today = date.today()

        dates = [today, today - timedelta(1), today - timedelta(4), today - timedelta(5)]
        result = calculate_streaks(dates)
        self.assertEqual(result['current_streak'], 2)
        self.assertEqual(result['longest_streak'], 2)

class HabitAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass1234')

        resp = self.client.post(
            '/api/token/',
            {'username': 'testuser', 'password': 'pass1234'},
            format='json'
        )
        token = resp.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_habit(self):
        resp = self.client.post('/api/habits/', {'name': 'Morning run', 'color': '#a6e3a1'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_list_only_own_habits(self):
        other = User.objects.create_user(username='other', password='pass')
        Habit.objects.create(user=other, name='Other habit')

        Habit.objects.create(user=self.user, name='My habit')

        resp = self.client.get('/api/habits/')

        self.assertEqual(len(resp.data), 1)

