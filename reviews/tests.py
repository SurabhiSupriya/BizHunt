from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from business.models import Business
from .models import Review

CustomUser = get_user_model()

class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser', password='testpass', user_type='user'
        )
        self.business = Business.objects.create(
            owner=self.user,
            business_name='Test Biz',
            category='Retail',
            address='123 Market St',
            pincode='12345',
            contact_info='9999999999',
            description='Retail business',
            business_type='physical',
            business_reg_no='RB123'
        )

    def test_add_review_get_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_review', args=[self.business.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Write a Review')

    def test_add_review_post_success(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_review', args=[self.business.id])
        response = self.client.post(url, {
            'rating': '5',
            'comment': 'Excellent service!'
        }, follow=True)
        self.assertRedirects(response, reverse('business_list'))
        self.assertTrue(Review.objects.filter(business=self.business, user=self.user).exists())

    def test_add_review_post_invalid_data(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('add_review', args=[self.business.id])
        response = self.client.post(url, {
            'rating': '',  # Missing rating
            'comment': 'No stars'
        })
        self.assertEqual(response.status_code, 200)  # Form not submitted
        self.assertFalse(Review.objects.exists())

    def test_add_review_requires_login(self):
        url = reverse('add_review', args=[self.business.id])
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, f"/login/?next={url}")

    def test_business_reviews_view(self):
        Review.objects.create(business=self.business, user=self.user, rating=4, comment="Nice")
        url = reverse('business_reviews', args=[self.business.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice')
