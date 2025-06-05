from django.test import TestCase, Client
from django.urls import reverse
from .models import Business, SearchHistory
from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile

class BusinessModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='owner', password='pass', user_type='business')

    def test_business_creation(self):
        biz = Business.objects.create(
            owner=self.user,
            business_name="Test Cafe",
            category="Food",
            address="123 Street",
            pincode="10001",
            contact_info="9999999999",
            description="Nice place",
            business_type="physical",
            business_reg_no="REG123"
        )
        self.assertEqual(str(biz), "Test Cafe")
        self.assertEqual(biz.pincode, "10001")


class SearchHistoryModelTest(TestCase):
    def test_search_history_entry(self):
        user = CustomUser.objects.create_user(username='searcher', password='pass')
        history = SearchHistory.objects.create(
            user=user,
            category="Tech",
            query="10001"
        )
        self.assertIn("Tech", str(history))


class BusinessViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_user(username='admin', password='adminpass', is_staff=True, user_type='admin')
        self.business_user = CustomUser.objects.create_user(username='bizuser', password='bizpass', user_type='business')

    def test_business_register_get(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('business_register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register Your Business")

    def test_business_register_post(self):
        self.client.login(username='admin', password='adminpass')
        dummy_image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('business_register'), {
            'business_owner': self.business_user.id,
            'business_name': "BizHunt Cafe",
            'category': "Cafe",
            'address': "NY Street",
            'pincode': "123456",
            'contact_info': "1112223333",
            'description': "Great place",
            'opening_hours': "09:00",
            'closing_hours': "18:00",
            'website': "http://bizhunt.com",
            'social_media': "http://instagram.com/bizhunt",
            'business_type': "physical",
            'business_reg_no': "REG456",
            'additional_services': "WiFi",
            'business_images': dummy_image
        }, follow=True)
        self.assertContains(response, "registered successfully")

    def test_business_list_filtering(self):
        Business.objects.create(
            owner=self.business_user,
            business_name="Bistro",
            category="Food",
            address="New York",
            pincode="12345",
            contact_info="1234567890",
            description="Fine food",
            business_type="physical",
            business_reg_no="1234"
        )
        self.client.login(username='bizuser', password='bizpass')
        response = self.client.get(reverse('business_list'), {'query': 'New York'})
        self.assertContains(response, "Bistro")


class SmartSearchTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='pass', user_type='user')
        self.client.login(username='testuser', password='pass')
        Business.objects.create(
            owner=self.user,
            business_name="The Book Hub",
            category="Bookstore",
            address="Library Lane",
            pincode="88888",
            contact_info="7777777777",
            description="Books and more",
            business_type="physical",
            business_reg_no="BK001"
        )

    def test_fuzzy_search(self):
        response = self.client.get(reverse('smart_search'), {'q': 'Book'})
        self.assertContains(response, "The Book Hub")


class LiveSearchSuggestionsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(username='testuser', password='pass', user_type='user')
        Business.objects.create(
            owner=self.user,
            business_name="Quick Clean",
            category="Cleaning",
            address="Main Road",
            pincode="55555",
            contact_info="9999999999",
            description="Cleaning service",
            business_type="physical",
            business_reg_no="CL001"
        )

    def test_live_suggestions(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(reverse('live_search'), {'q': 'Clean'})
        self.assertContains(response, "Quick Clean")
