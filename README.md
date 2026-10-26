# Sprawozdanie — Laboratorium nr 2

**Przedmiot:** Programowanie V  
**Projekt:** Uniwersalny konwerter plików  
**Autor:** Andrii Pidkovych

## Cel
Celem laboratorium było przygotowanie podstaw uniwersalnego konwertera plików w języku Python, w tym obsługi formatów CSV, JSON i zaplanowania dalszej rozbudowy o formaty dokumentów.

## Zrealizowane funkcjonalności
- Konwersja CSV → JSON.
- Konwersja JSON → CSV.
- Obsługa kodowania UTF-8 i polskich znaków.
- Zachowanie nagłówków oraz kolejności kolumn.
- Walidacja danych wejściowych.
- Obsługa błędów i zabezpieczenie przed nadpisaniem istniejącego pliku.
- Przygotowanie macierzy konwersji i przykładowych danych.

## Wyniki testów
Oba kierunki konwersji zostały uruchomione pomyślnie. Testy automatyczne zakończyły się wynikiem OK.

## Dalsze etapy
W kolejnych laboratoriach planowana jest implementacja konwersji dokumentów TXT, DOCX, ODT i PDF oraz interfejsu graficznego Tkinter/ttk.

## Wykorzystane narzędzia
Python 3, Visual Studio Code, biblioteki standardowe `csv`, `json`, `pathlib` i `unittest`.


## Kamień milowy 2 – Laboratorium nr 3

Rozszerzono aplikację o obsługę formatów TXT, DOCX, ODT i PDF.

### Obsługiwane konwersje

| Format wejściowy | Format wyjściowy | Narzędzie |
|---|---|---|
| CSV | JSON | Python csv/json |
| JSON | CSV | Python csv/json |
| TXT | DOCX | python-docx |
| DOCX | PDF | LibreOffice |
| ODT | PDF | LibreOffice |

### Wymagania

- Python 3
- Biblioteka python-docx
- LibreOffice do konwersji PDF

Instalacja zależności:

`python -m pip install -r requirements.txt`

### Ograniczenia

Konwersja TXT → DOCX przenosi tekst i podział na akapity, ale nie odtwarza zaawansowanego formatowania.

Konwersje do PDF wymagają zainstalowanego LibreOffice. Aplikacja nie nadpisuje istniejących plików wynikowych.

### Wykorzystane narzędzia

Python, python-docx, LibreOffice, moduły subprocess i pathlib.