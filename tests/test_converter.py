import json
import tempfile
import unittest
from pathlib import Path
from converter import available_targets, convert

ROOT = Path(__file__).resolve().parents[1]


class ConverterTests(unittest.TestCase):
    def test_targets(self):
        self.assertEqual(available_targets(Path('plik.csv')), ['.json'])
        self.assertEqual(available_targets(Path('plik.txt')), ['.docx'])

    def test_csv_to_json(self):
        with tempfile.TemporaryDirectory() as folder:
            target = convert(ROOT / 'samples/osoby.csv', 'json', Path(folder))
            rows = json.loads(target.read_text(encoding='utf-8'))
            self.assertEqual(rows[0]['miasto'], 'Łódź')
            self.assertEqual(list(rows[0]), ['imie', 'miasto', 'wiek', 'uwagi'])

    def test_json_to_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            target = convert(ROOT / 'samples/osoby.json', 'csv', Path(folder))
            self.assertIn('Łódź', target.read_text(encoding='utf-8'))

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'Niepoprawny JSON'):
                convert(ROOT / 'samples/bledny.json', 'csv', Path(folder))

    def test_unsupported_pair(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'Nieobsługiwana'):
                convert(ROOT / 'samples/notatka.txt', 'json', Path(folder))

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            convert(ROOT / 'samples/osoby.csv', 'json', Path(folder))
            with self.assertRaises(FileExistsError):
                convert(ROOT / 'samples/osoby.csv', 'json', Path(folder))

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            result = convert(ROOT / 'samples/osoby.csv', 'json', folder)
            other = folder / 'other'
            other.mkdir()
            recovered = convert(result, 'csv', other)
            self.assertEqual((ROOT / 'samples/osoby.csv').read_text(encoding='utf-8').splitlines(), recovered.read_text(encoding='utf-8').splitlines())


if __name__ == '__main__':
    unittest.main()
