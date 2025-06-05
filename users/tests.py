from django.test import TestCase, Client
from django.urls import reverse
from users.models import CustomUser
from business.models import Business
from django.core.files.uploadedfile import SimpleUploadedFile

class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_post_user(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Alice',
            'last_name': 'Smith',
            'username': 'alice',
            'email': 'alice@example.com',
            'contact_number': '1234567890',
            'address': '123 Street',
            'gender': 'female',
            'signup_type': 'user',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }, follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(CustomUser.objects.filter(username='alice').exists())

    def test_signup_post_business(self):
        response = self.client.post(reverse('signup'), {
            'first_name': 'Bob',
            'last_name': 'Jones',
            'username': 'bob',
            'email': 'bob@example.com',
            'contact_number': '1234567890',
            'address': '456 Avenue',
            'gender': 'male',
            'signup_type': 'business',
            'business_name': 'Bob Cafe',
            'business_address': 'Café Street',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }, follow=True)
        self.assertRedirects(response, reverse('login'))
        user = CustomUser.objects.get(username='bob')
        self.assertEqual(user.business_name, 'Bob Cafe')
        self.assertTrue(Business.objects.filter(owner=user).exists())

    def test_login_view(self):
        user = CustomUser.objects.create_user(username='testuser', password='password123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        }, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_login_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'invalid',
            'password': 'wrong'
        }, follow=True)
        self.assertContains(response, "Invalid username or password")

    def test_logout_view(self):
        user = CustomUser.objects.create_user(username='logoutuser', password='logoutpass')
        self.client.login(username='logoutuser', password='logoutpass')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('login'))


class ProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='profileuser', password='pass', user_type='business'
        )
        self.business = Business.objects.create(
            owner=self.user,
            business_name='TestBiz',
            category='Food',
            address='NY',
            pincode='12345',
            contact_info='9999999999',
            description='A business',
            business_type='physical',
            business_reg_no='B123'
        )

    def test_profile_view(self):
        self.client.login(username='profileuser', password='pass')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestBiz')

    def test_edit_profile_get(self):
        self.client.login(username='profileuser', password='pass')
        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')

    def test_edit_profile_post(self):
        self.client.login(username='profileuser', password='pass')
        new_image = SimpleUploadedFile("test.jpg", b"image_content", content_type="image/jpeg")
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'UpdatedName',
            'business_name': 'UpdatedBiz',
            'category': 'UpdatedCategory',
            'business_contact': '0001112222',
            'business_website': 'http://updated.com',
            'business_image': new_image
        }, follow=True)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.business.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')
        self.assertEqual(self.business.business_name, 'UpdatedBiz')


class StaticPageTests(TestCase):
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_us_view(self):
        response = self.client.get(reverse('about_us'))
        self.assertEqual(response.status_code, 200)

    def test_privacy_policy_view(self):
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
