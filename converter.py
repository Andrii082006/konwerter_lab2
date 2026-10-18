"""Konwersje CSV <-> JSON dla kamienia milowego Lab. 2."""
import csv
import json
from pathlib import Path

REGISTRY = {('.csv', '.json'), ('.json', '.csv')}


def available_targets(source: Path) -> list[str]:
    return sorted(dst for src, dst in REGISTRY if src == source.suffix.lower())


def convert(source: Path, target_format: str, output_dir: Path) -> Path:
    source = Path(source)
    output_dir = Path(output_dir)
    target_format = target_format.lower().lstrip('.')
    if not source.is_file():
        raise ValueError(f'Plik wejściowy nie istnieje: {source}')
    if not output_dir.is_dir():
        raise ValueError(f'Katalog docelowy nie istnieje: {output_dir}')
    if (source.suffix.lower(), '.' + target_format) not in REGISTRY:
        raise ValueError(f'Nieobsługiwana konwersja: {source.suffix} -> {target_format}')
    target = output_dir / f'{source.stem}.{target_format}'
    if target.exists():
        raise FileExistsError(f'Plik wynikowy już istnieje: {target}')
    if target_format == 'json':
        with source.open('r', encoding='utf-8-sig', newline='') as stream:
            reader = csv.DictReader(stream)
            if not reader.fieldnames or any(not h for h in reader.fieldnames):
                raise ValueError('CSV musi mieć niepuste nagłówki kolumn.')
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ValueError('Nagłówki CSV muszą być unikalne.')
            rows = list(reader)
            if any(None in row for row in rows):
                raise ValueError('CSV zawiera wiersz z większą liczbą pól niż nagłówków.')
        content = json.dumps(rows, ensure_ascii=False, indent=2)
        target.write_text(content + '\n', encoding='utf-8')
    else:
        try:
            with source.open('r', encoding='utf-8-sig') as stream:
                rows = json.load(stream)
        except json.JSONDecodeError as exc:
            raise ValueError(f'Niepoprawny JSON (wiersz {exc.lineno}, kolumna {exc.colno}): {exc.msg}') from exc
        if not isinstance(rows, list) or not rows or not all(isinstance(r, dict) for r in rows):
            raise ValueError('JSON musi być niepustą listą obiektów, np. [{"imie": "Ala"}].')
        headers = list(rows[0])
        if not headers or not all(isinstance(h, str) and h for h in headers):
            raise ValueError('Nazwy pól JSON muszą być niepustymi napisami.')
        if any(list(row) != headers for row in rows):
            raise ValueError('Wszystkie obiekty JSON muszą mieć te same pola w tej samej kolejności.')
        if any(not isinstance(value, (str, int, float, bool, type(None))) for row in rows for value in row.values()):
            raise ValueError('Wartości JSON muszą być proste: tekst, liczba, boolean lub null.')
        with target.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
    return target
