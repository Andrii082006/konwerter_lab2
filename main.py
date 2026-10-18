"""Uruchomienie: python main.py PLIK csv|json KATALOG_WYNIKOWY"""
import argparse
from pathlib import Path
from converter import convert


def main():
    parser = argparse.ArgumentParser(description='Konwerter CSV <-> JSON (Lab. 2)')
    parser.add_argument('source', type=Path, help='Plik wejściowy')
    parser.add_argument('format', choices=['csv', 'json'], help='Format docelowy')
    parser.add_argument('output_dir', type=Path, help='Istniejący katalog zapisu')
    args = parser.parse_args()
    try:
        result = convert(args.source, args.format, args.output_dir)
    except (ValueError, OSError, UnicodeError) as exc:
        parser.exit(1, f'Błąd: {exc}\n')
    print(f'Sukces! Zapisano: {result}')


if __name__ == '__main__':
    main()
