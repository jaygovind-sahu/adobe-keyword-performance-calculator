import unittest

from keyword_perf.payload.product_list_parser import ProductListParser


class ProductListParserTestCase(unittest.TestCase):
    def test_zero_revenue(self):
        parser = ProductListParser('Electronics;Ipod - Touch - 32GB;1;;')
        self.assertEqual(parser.category, 'Electronics')
        self.assertEqual(parser.product_name, 'Ipod - Touch - 32GB')
        self.assertEqual(parser.item_count, 1)
        self.assertEqual(parser.total_revenue, 0)

    def test_some_revenue(self):
        parser = ProductListParser('Electronics;Zune - 32GB;2;500;')
        self.assertEqual(parser.category, 'Electronics')
        self.assertEqual(parser.product_name, 'Zune - 32GB')
        self.assertEqual(parser.item_count, 2)
        self.assertEqual(parser.total_revenue, 500.00)
