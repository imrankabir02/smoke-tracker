from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Achievement, UserAchievement, SmokeLog, Profile

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        Profile.objects.create(user=self.user)
        self.client.login(username='testuser', password='password')

        # Create achievements
        self.achievement1 = Achievement.objects.create(
            title="Test Achievement 1",
            description="Test Description 1",
            points_reward=10,
            achievement_type='logging',
            criteria_type='total_logs',
            criteria_value=10
        )
        self.achievement2 = Achievement.objects.create(
            title="Test Achievement 2",
            description="Test Description 2",
            points_reward=20,
            achievement_type='logging',
            criteria_type='total_logs',
            criteria_value=20
        )

    def test_featured_achievement_logic(self):
        # Create some smoke logs for the user
        for i in range(5):
            SmokeLog.objects.create(user=self.user)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        featured_achievement = response.context.get('featured_achievement')
        self.assertIsNotNone(featured_achievement)
        self.assertEqual(featured_achievement['achievement'], self.achievement1)
        self.assertEqual(featured_achievement['progress_data']['current'], 5)
        self.assertEqual(featured_achievement['progress_data']['progress'], 50)
