
"""Uruchamianie konwertera plików - Lab. 3."""

import argparse
from pathlib import Path

from converter import convert, available_targets


def main():
    parser = argparse.ArgumentParser(
        description="Uniwersalny konwerter plików - Lab. 3"
    )

    parser.add_argument(
        "source",
        type=Path,
        help="Ścieżka do pliku wejściowego"
    )

    parser.add_argument(
        "format",
        choices=["csv", "json", "docx", "pdf"],
        help="Format docelowy"
    )

    parser.add_argument(
        "output_dir",
        type=Path,
        help="Katalog zapisu"
    )

    args = parser.parse_args()

    try:
        targets = available_targets(args.source)

        if "." + args.format not in targets:
            raise ValueError(
                f"Nieobsługiwana konwersja: "
                f"{args.source.suffix} -> {args.format}"
            )

        result = convert(
            args.source,
            args.format,
            args.output_dir
        )

        print(f"Sukces! Zapisano: {result}")

    except (ValueError, OSError, UnicodeError, RuntimeError) as exc:
        parser.exit(1, f"Błąd: {exc}\n")


if __name__ == "__main__":
    main()
