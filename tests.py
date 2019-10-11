from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

class ContractorTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the contractor project homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    def test_cart(self):
        """Test the contractor project cartpage."""
        result = self.client.get('/cart')
        self.assertEqual(result.status, '200 OK')

if __name__ == '__main__':
    unittest_main()