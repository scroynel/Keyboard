from django.test import TestCase
from django.contrib.auth import get_user_model
from keyboard.forms import CommentForm
from keyboard.models import Product, Category, ProductComment


User = get_user_model()


class CommentFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='testuser1', password='pass')
        cls.category = Category.objects.create(name='Test category', slug='test-category')
        cls.product = Product.objects.create(
            name = 'Test Product',
            slug = 'test-product',
            description = 'Description test product',
            price = 100.00,
            number = 567845,
            category = cls.category
        )

    
    def test_comment_form_valid_data(self):
        data = {
            'description': 'Test description1',
            'rating': 5
        }

        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

        # Create a comment instance but don't save yet
        comment = form.save(commit=False)
        comment.product = self.product
        comment.owner = self.user1
        comment.save()

        self.assertEqual(ProductComment.objects.count(), 1)
        self.assertEqual(ProductComment.objects.first().description, 'Test description1')
        self.assertEqual(ProductComment.objects.first().rating, 5)

    
    def test_comment_form_without_description(self):
        data = {
            'description': '', # Invalid because it's required 
            'rating': 4
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    
    def test_comment_form_without_rating(self):
        data = {
            'description': 'Test description1'
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)


    def test_comment_form_out_of_range(self):
        data = {
            'description': 'Test description1',
            'rating': 10
        }
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    
    def test_comment_form_description_widget(self):
        form = CommentForm()
        widget = form.fields['description'].widget
        
        self.assertEqual(widget.attrs['class'], 'w-full')
        self.assertEqual(widget.attrs['rows'], 5)
        self.assertEqual(widget.attrs['placeholder'], 'Leave your comment ...')