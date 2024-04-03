# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest
import os
from dotenv import load_dotenv
from src.hebe_api import Hebe

load_dotenv()
EXAMPLE_HEBE_USERNAME = os.getenv("EXAMPLE_HEBE_USERNAME")
EXAMPLE_HEBE_PASSWORD = os.getenv("EXAMPLE_HEBE_PASSWORD")
if EXAMPLE_HEBE_USERNAME is None or EXAMPLE_HEBE_PASSWORD is None:
    raise Exception(
        "Unit tests need valid hebe credentials " "to validate the project"
    )


class TestHebeAPI(unittest.TestCase):
    def test_authenticate(self):
        hebe = Hebe(EXAMPLE_HEBE_USERNAME, EXAMPLE_HEBE_PASSWORD)
        hebe.authenticate()
        self.assertFalse(hebe.token is None)

    def test_get_orders(self):
        hebe = Hebe(EXAMPLE_HEBE_USERNAME, EXAMPLE_HEBE_PASSWORD)
        hebe.authenticate()
        self.assertFalse(hebe.token is None)
        orders = hebe.get_orders(max_orders=1)
        self.assertTrue(len(orders) > 0)

    def test_get_products_by_order(self):
        hebe = Hebe(EXAMPLE_HEBE_USERNAME, EXAMPLE_HEBE_PASSWORD)
        hebe.authenticate()
        self.assertFalse(hebe.token is None)
        orders = hebe.get_orders(max_orders=1)
        self.assertTrue(len(orders) > 0)
        products = hebe.get_order_products(orders[0])
        self.assertTrue(len(products) > 0)


if __name__ == '__main__':
    unittest.main()
