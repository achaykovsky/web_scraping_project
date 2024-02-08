import unittest

from bs4 import BeautifulSoup

from scrapping import find_column_indices


class TestFindColumnIndices(unittest.TestCase):

    def test_valid_header_row(self):
        header_row = BeautifulSoup(
            "<tr><th>animal</th><th>collateral adjective</th></tr>", "html.parser"
        )
        animal_index, collateral_adjective_index = find_column_indices(header_row)
        self.assertEqual(animal_index, 0)
        self.assertEqual(collateral_adjective_index, 1)

    def test_header_row_without_columns(self):
        header_row = BeautifulSoup("<tr></tr>", "html.parser")
        with self.assertLogs(level="WARNING") as cm:
            animal_index, collateral_adjective_index = find_column_indices(header_row)
        self.assertEqual(animal_index, None)
        self.assertEqual(collateral_adjective_index, None)
        self.assertIn("Row does not have enough columns. Skipping.", cm.output[0])

    def test_additional_columns(self):
        header_row = BeautifulSoup(
            "<tr><th>Animal</th><th>Extra</th><th>Collateral Adjective</th></tr>",
            "html.parser",
        )
        animal_index, collateral_adjective_index = find_column_indices(header_row)
        self.assertEqual(animal_index, 0)
        self.assertEqual(collateral_adjective_index, 2)

    def test_missing_header_row(self):
        header_row = None
        animal_index, collateral_adjective_index = find_column_indices(header_row)
        self.assertEqual(animal_index, None)
        self.assertEqual(collateral_adjective_index, None)

    def test_empty_header_row(self):
        header_row = BeautifulSoup("<tr></tr>", "html.parser")
        animal_index, collateral_adjective_index = find_column_indices(header_row)
        self.assertEqual(animal_index, None)
        self.assertEqual(collateral_adjective_index, None)


if __name__ == "__main__":
    unittest.main()
