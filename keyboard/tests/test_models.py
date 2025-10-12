from django.test import TestCase
from keyboard.models import Product, Category, ProductComment
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductModelsTest(TestCase):
    @classmethod 
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Test category', slug='test-category')
        cls.product = Product.objects.create(
            name = 'Test Product',
            slug = 'test-product',
            description = 'Description test product',
            price = 100.00,
            number = 567845,
            category = cls.category
        )

        # Create users
        cls.user1 = User.objects.create(username='testuser', password='pass')
        cls.user2 = User.objects.create(username='testuser1', password='pass')
        cls.user3 = User.objects.create(username='testuser2', password='pass')

        # Create comments 
        cls.comment1 = ProductComment.objects.create(product=cls.product, owner=cls.user1, rating=5)
        cls.comment2 = ProductComment.objects.create(product=cls.product, owner=cls.user2, rating=4)
        cls.comment3 = ProductComment.objects.create(product=cls.product, owner=cls.user3, rating=3)


    def test_product_model_creation(self):
        self.assertIsNotNone(self.product.id)

        self.assertEqual(self.product.name, 'Test Product')
        self.assertGreaterEqual(self.product.price, 0)
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.number, 567845)
        
    
    def test_product_str(self):
        self.assertEqual(self.product.__str__(), self.product.name)


    def test_product_absolute_url(self):
        expected_url = reverse('products_detail', kwargs={'category_slug': self.category.slug, 'product_slug': self.product.slug})

        self.assertEqual(self.product.get_absolute_url(), expected_url)

    
    def test_product_wishlist_add_url(self):
        expected_url = reverse('wishlist:wishlist_add', kwargs={'product_slug': self.product.slug})

        self.assertEqual(self.product.get_wishlist_add_url(), expected_url)


    def test_product_wishlist_delete_url(self):
        expected_url = reverse('wishlist:wishlist_delete', kwargs={'product_slug': self.product.slug})

        self.assertEqual(self.product.get_wishlist_delete_url(), expected_url)


    def test_product_property_average_rating(self):
        self.assertEqual(self.product.average_rating, 4.0)

    
    def test_category(self):
        expected_url = reverse('products', kwargs={'category_slug': self.category.slug})

        self.assertEqual(self.category.get_absolute_url(), expected_url)

    
    def test_product_comment_rating(self):
        comments = ProductComment.objects.filter(product=self.product)
        for comment in comments:
            with self.subTest(comment=comment):
                self.assertGreater(comment.rating, 0)

