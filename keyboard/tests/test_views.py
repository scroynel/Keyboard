from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model

from keyboard.models import Category, Product, ProductComment
from wishlist.models import Wishlist
from keyboard.forms import CommentForm
from keyboard.views import ProductDetailView 


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


class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

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

        # Create users
        cls.user1 = User.objects.create(username='testuser', password='pass')
        cls.user2 = User.objects.create(username='testuser1', password='pass')

        # Create comments 
        cls.comment1 = ProductComment.objects.create(product=cls.product1, owner=cls.user1, rating=5)
        cls.comment2 = ProductComment.objects.create(product=cls.product1, owner=cls.user2, rating=4)

        cls.url = reverse('products_detail', kwargs={'category_slug': cls.category.slug, 'product_slug': cls.product1.slug})


    def test_product_detail_view_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    
    def test_product_detail_view_template_used(self):
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'keyboard/products_detail.html')


    def test_product_detail_view_form_class(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], CommentForm)


    def test_prodcut_detail_view_context(self):
        response = self.client.get(self.url)
        comments = response.context['comments']

        self.assertIn(self.comment1, comments)
        self.assertIn(self.comment2, comments)


class AjaxCommentAddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Create a User
        cls.user1 = User.objects.create_user(username='testuser', password='pass')

        # Create a category
        cls.category = Category.objects.create(name='Test Category', slug='test-category')

        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x39\x61',  # minimal GIF header bytes
            content_type='image/gif'
        )

        # Create a product
        cls.product1 = Product.objects.create(
            name = 'Test Product',
            slug = 'test-product',
            description = 'Description test product',
            price = 100.00,
            number = 567845,
            category = cls.category,
            image = image
        )

        cls.url = reverse('comment_add', kwargs={'category_slug': cls.category.slug, 'product_slug': cls.product1.slug})

    
    def test_ajax_comment_add_view_no_headers(self):
        self.client.login(username='testuser', password='pass')
        data = {
            'description': 'Test description1',
            'rating': 3,
            'owner': self.user1,
            'product': self.product1
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 400)


    def test_ajax_comment_add_view_with_headers(self):
        self.client.login(username='testuser', password='pass')
        data = {
            'description': 'Test description2',
            'rating': 4,
            'owner': self.user1,
            'product': self.product1
        }
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}

        response = self.client.post(self.url, data, **headers)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('avg_rating', response.json())
        self.assertIn('comments_count', response.json())
        self.assertIn('comment_list', response.json())
        self.assertEqual(ProductComment.objects.count(), 1)

    
    def test_ajax_comment_add_view_one_comment(self):
        ProductComment.objects.create(
            description = 'Test description1',
            rating = 3,
            owner = self.user1,
            product = self.product1
        )

        self.client.login(username='testuser', password='pass')
        data = {
            'description': 'Test description2',
            'rating': 4,
            'owner': self.user1,
            'product': self.product1
        }
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = self.client.post(self.url, data, **headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('status_error', response.json())
        self.assertEqual(ProductComment.objects.count(), 1)

    
    def test_ajax_comment_add_view_no_comment(self):
        self.client.login(username='testuser', password='pass')
        data = {
            'description': '',
            'rating': 6,
            'owner': self.user1,
            'product': self.product1
        }
        headers = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        response = self.client.post(self.url, data, **headers)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ProductComment.objects.count(), 0)