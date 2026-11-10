
# Sprawozdanie z projektu – Uniwersalny konwerter plików

**Przedmiot:** Programowanie V  
**Autor:** Andrii Pidkovych  
**Język programowania:** Python 3  
**Temat projektu:** Uniwersalny konwerter plików

## 1. Cel projektu

Celem projektu było stworzenie aplikacji umożliwiającej konwersję plików pomiędzy różnymi formatami. Program został napisany w języku Python i obsługuje formaty CSV, JSON, TXT, DOCX, ODT oraz PDF.

Głównym założeniem było przygotowanie prostego i funkcjonalnego narzędzia, które pozwala użytkownikowi wybrać plik wejściowy, format docelowy oraz miejsce zapisania wyniku.

Dodatkowym celem było zapewnienie poprawnej obsługi błędów, zachowania polskich znaków oraz zabezpieczenia przed przypadkowym nadpisaniem istniejących plików.

## 2. Wykorzystane technologie

Do realizacji projektu wykorzystano:

- **Python 3** – główny język programowania.
- **csv i json** – biblioteki standardowe do przetwarzania danych.
- **python-docx** – tworzenie dokumentów DOCX.
- **LibreOffice** – konwersja dokumentów DOCX i ODT do PDF.
- **Tkinter/ttk** – interfejs graficzny aplikacji.
- **pathlib** – obsługa ścieżek plików.
- **subprocess** – uruchamianie LibreOffice.
- **unittest** – automatyczne testowanie programu.
- **Visual Studio Code** – środowisko programistyczne wskazane w dokumentacji projektu.

## 3. Opis działania programu

Aplikacja umożliwia konwersję plików za pomocą interfejsu graficznego lub wiersza poleceń.

Użytkownik wskazuje plik wejściowy, wybiera jeden z dostępnych formatów wyjściowych oraz katalog docelowy. Program sprawdza poprawność danych, a następnie wykonuje odpowiednią konwersję.

W przypadku nieprawidłowego pliku, nieobsługiwanego formatu lub braku wymaganych narzędzi wyświetlany jest komunikat o błędzie.

Program sprawdza również, czy plik wynikowy już istnieje. Jeśli tak, konwersja zostaje zablokowana, aby uniknąć nadpisania danych.

## 4. Obsługiwane konwersje i ograniczenia

| Konwersja | Opis | Znane ograniczenia |
|---|---|---|
| CSV → JSON | Zamiana danych tabelarycznych na listę obiektów JSON | Wymagane unikalne, niepuste nagłówki; wartości pozostają tekstem |
| JSON → CSV | Zapis listy obiektów JSON w formacie tabelarycznym | Wymagana niepusta lista obiektów o identycznych polach i ich kolejności; obsługiwane są tylko proste wartości |
| TXT → DOCX | Tworzenie dokumentu Word z pliku tekstowego | Przenoszony jest tekst i podział na akapity, bez zaawansowanego formatowania |
| DOCX → PDF | Konwersja dokumentu Word do PDF | Wymaga LibreOffice; wygląd dokumentu może się nieznacznie zmienić |
| ODT → PDF | Konwersja dokumentu OpenDocument do PDF | Wymaga LibreOffice; możliwe różnice w układzie i czcionkach |

Inne pary formatów nie są obecnie obsługiwane.

## 5. Przykładowe dane testowe

Do sprawdzenia programu wykorzystano następujące przypadki:

### Test 1 – CSV → JSON

Plik wejściowy: `samples/osoby.csv`

Oczekiwany wynik: utworzenie poprawnego pliku JSON, zachowanie nazw pól, kolejności kolumn oraz polskich znaków, np. „Łódź”.

### Test 2 – JSON → CSV

Plik wejściowy: `samples/osoby.json`

Oczekiwany wynik: utworzenie pliku CSV z nagłówkami i poprawnym zapisaniem danych.

### Test 3 – Niepoprawny JSON

Plik wejściowy: `samples/bledny.json`

Oczekiwany wynik: wykrycie błędu składni JSON, wyświetlenie odpowiedniego komunikatu i przerwanie konwersji.

### Test 4 – TXT → DOCX

Plik wejściowy: tekst zawierający polskie znaki i dwa akapity.

Oczekiwany wynik: utworzenie dokumentu DOCX z zachowaniem zawartości obu akapitów.

### Test 5 – DOCX/ODT → PDF

Pliki wejściowe: przykładowe dokumenty DOCX i ODT.

Oczekiwany wynik: utworzenie poprawnych plików PDF.

## 6. Raport z przeprowadzonych testów

Testowanie przeprowadzono za pomocą modułu `unittest` oraz prób rzeczywistej konwersji dokumentów.

Uruchomienie testów:

```bash
python -m unittest discover -s tests -v
```

### Wyniki testów

| Test | Wynik |
|---|---|
| CSV → JSON | Pozytywny |
| JSON → CSV | Pozytywny |
| Ponowna konwersja CSV → JSON → CSV | Pozytywny |
| Obsługa błędnego JSON | Pozytywny |
| Blokowanie nadpisywania pliku | Pozytywny |
| Sprawdzanie dostępnych formatów | Pozytywny |
| Odrzucanie nieobsługiwanych konwersji | Pozytywny |
| TXT → DOCX | Pozytywny |
| Obsługa braku LibreOffice | Pozytywny |
| DOCX → PDF – próba rzeczywista | Pozytywny |
| ODT → PDF – próba rzeczywista | Pozytywny |

**Wynik testów automatycznych: 11 z 11 zakończonych pomyślnie.**

Dodatkowo wykonano rzeczywiste konwersje DOCX → PDF oraz ODT → PDF. W obu przypadkach otrzymano pliki z poprawnym nagłówkiem formatu PDF.

Nie przeprowadzono osobnego automatycznego testu obsługi interfejsu graficznego ani szczegółowego porównania wizualnego dokumentów PDF z oryginałami.

## 7. Problemy i ograniczenia

Podczas analizy projektu zidentyfikowano następujące ograniczenia:

1. Do konwersji dokumentów DOCX i ODT na PDF konieczne jest zainstalowanie LibreOffice.
2. Konwersja TXT do DOCX nie zachowuje zaawansowanego formatowania.
3. Program obsługuje tylko pięć określonych par formatów.
4. Konwersja JSON do CSV wymaga jednakowej struktury wszystkich obiektów.
5. Aplikacja nie nadpisuje istniejących plików wynikowych.
6. Wygląd plików PDF może zależeć od dostępnych czcionek oraz wersji LibreOffice.

## 8. Etapy realizacji projektu

Na podstawie struktury i dokumentacji projektu można wyróżnić następujące etapy prac:

### Etap 1 – Podstawowy konwerter

Implementacja konwersji CSV i JSON oraz walidacji danych.

### Etap 2 – Rozbudowa formatów

Dodanie konwersji TXT → DOCX oraz DOCX/ODT → PDF z wykorzystaniem python-docx i LibreOffice.

### Etap 3 – Interfejs użytkownika

Przygotowanie graficznego interfejsu aplikacji w Tkinter/ttk.

### Etap 4 – Testowanie

Przygotowanie testów automatycznych, sprawdzenie poprawności konwersji oraz obsługi błędów.

Przedstawione etapy są opisem rozwoju funkcjonalnego projektu, a nie zweryfikowaną historią commitów Git.

## 9. Wykorzystane źródła i narzędzia

W projekcie wykorzystano biblioteki i narzędzia:

- Python – https://docs.python.org/3/
- python-docx – https://python-docx.readthedocs.io/
- LibreOffice – https://www.libreoffice.org/
- Tkinter – dokumentacja standardowej biblioteki Python.
- unittest – dokumentacja standardowej biblioteki Python.

**Narzędzia AI:** ChatGPT (OpenAI) – wykorzystany do analizy projektu, sprawdzenia wyników testów oraz przygotowania niniejszego sprawozdania.

## 10. Wnioski końcowe

W ramach projektu wykonano aplikację umożliwiającą konwersję pomiędzy pięcioma parami formatów plików. Program obsługuje dane tekstowe, tabelaryczne i dokumenty biurowe.

Przeprowadzone testy automatyczne potwierdziły poprawność działania najważniejszych funkcji programu. Wszystkie 11 testów zakończyło się sukcesem. Dodatkowe próby potwierdziły możliwość generowania dokumentów PDF z plików DOCX i ODT.

Projekt pozwolił na praktyczne wykorzystanie bibliotek Pythona, obsługi plików, walidacji danych, automatyzacji konwersji dokumentów oraz testowania oprogramowania.

W przyszłości aplikację można rozbudować o dodatkowe formaty, konwersję wielu plików jednocześnie i bardziej zaawansowaną obsługę dokumentów.

**Podsumowując, najważniejsze założenia funkcjonalne projektu zostały zrealizowane, a sprawdzone funkcje działają poprawnie.**
