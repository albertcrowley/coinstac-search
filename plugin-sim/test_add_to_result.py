from unittest import TestCase
from reprosearch.util import update_meta_data_structure
import math

class TestAdd_to_result(TestCase):
    def test_add_to_result(self):
        result = {}
        update_meta_data_structure(result, "a", "7")
        self.assertTrue(result["a"]["numeric"])
        self.assertEqual(result["a"]["min"], 7, "didn't set min")
        self.assertEqual(result["a"]["max"], 7, "didn't set max")

        update_meta_data_structure(result, "a", "-2.2")
        self.assertTrue(result["a"]["numeric"])
        self.assertEqual(result["a"]["min"], -2.2, "didn't set min")
        self.assertEqual(result["a"]["max"], 7, "didn't set max")

        update_meta_data_structure(result, "b", "nan")
        self.assertFalse(result["b"]["numeric"])
        self.assertTrue(math.isnan(result["b"]["min"]), "NaN fail")
        self.assertTrue(math.isnan(result["b"]["max"]), "NaN fail")

        update_meta_data_structure(result, "b", "1.2e6")
        self.assertTrue(result["b"]["numeric"])
        self.assertEqual(result["b"]["min"], float('1.2e6'), "didn't set min")
        self.assertEqual(result["b"]["max"], float('1.2e6'), "didn't set max")

        update_meta_data_structure(result, "c", "other thing")
        self.assertFalse(result["c"]["numeric"])
        self.assertEqual(result["c"]["enumeration"], ["other thing"], "didn't enumerate")

