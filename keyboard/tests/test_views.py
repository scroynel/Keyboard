from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from keyboard.models import Category, Product
from wishlist.models import Wishlist

User = get_user_model()


class ProductViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Create a user
        cls.user = User.objects.create_user(username='testuser', password='pass')

        # Create a category
        cls.category = Category.objects.create(name='Test Category', slug='test-category')

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # minimal GIF header bytes
            content_type='image/gif'
        )

        # Create products
        cls.product1 = Product.objects.create(
            name = 'Test Product',
            slug = 'test-product',
            description = 'Description test product',
            price = 100.00,
            number = 567845,
            category = cls.category,
            image = image
        )
        cls.product2 = Product.objects.create(
            name = 'Test Product1',
            slug = 'test-product1',
            description = 'Description test product1',
            price = 200.00,
            number = 643675,
            category = cls.category,
            image = image
        )

        cls.url = reverse('products', kwargs={'category_slug': cls.category.slug})


    def test_product_view_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)


    def test_product_view_template_used(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'keyboard/products.html')

    
    def test_product_view_category_products_displayed(self):
        response = self.client.get(self.url)
        products = response.context['products']

        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)
        self.assertEqual(products.count(), 2)


    def test_product_view_context_category(self):
        response = self.client.get(self.url)

        self.assertEqual(response.context['category_slug'], self.category.slug)
    

    def test_product_view_invalid_category(self):
        url = reverse('products', kwargs={'category_slug': 'invalid'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


    def test_product_view_context_user_wishlist_auth(self):
        self.client.login(username='testuser', password='pass')
        response = self.client.get(self.url)

        self.assertIn('user_wishlist', response.context)


    def test_product_view_context_user_wishlist_anonymous(self):
        response = self.client.get(self.url)

        self.assertNotIn('user_wishlist', response.context)


class MainViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.url = reverse('main')

    def test_main_view_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    
    def test_main_view_template_used(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'keyboard/main.html')


    def test_main_view_context_products(self):
        response = self.client.get(self.url)

        self.assertIn('products', response.context)