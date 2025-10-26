from django.test import SimpleTestCase
from django.urls import reverse, resolve

from keyboard.views import ProductView, ProductDetailView, AjaxCommentAddView


class ProductUrlsTest(SimpleTestCase):
    @classmethod
    def setUpTestData(cls):
        pass


    def test_products_url_resolves(self):
        url = reverse('products', args=['category1'])
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, ProductView)

    
    def test_product_detail_url_resolves(self):
        url = reverse('products_detail', args=['category1', 'product_slug1'])
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, ProductDetailView)


    def test_product_comment_add_url_resolves(self):
        url = reverse('comment_add', args=['category1', 'product_slug1'])
        resolver = resolve(url)

        self.assertEqual(resolver.func.view_class, AjaxCommentAddView)