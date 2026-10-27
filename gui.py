
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading
import queue

from converter import convert, available_targets


class KonwerterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Uniwersalny konwerter plików")
        self.root.geometry("650x430")
        self.root.resizable(False, False)

        self.plik = tk.StringVar()
        self.folder = tk.StringVar()
        self.format = tk.StringVar()
        self.status = tk.StringVar(value="Wybierz plik do konwersji")

        self.trwa_konwersja = False
        self.wyniki = queue.Queue()

        self.utworz_okno()

    def utworz_okno(self):
        self.root.configure(bg="#eef2f6")

        styl = ttk.Style()
        styl.theme_use("clam")

        styl.configure(
            "TFrame",
            background="#eef2f6"
        )
        styl.configure(
            "TLabel",
            background="#eef2f6",
            font=("Arial", 10)
        )
        styl.configure(
            "TButton",
            font=("Arial", 10),
            padding=7
        )
        styl.configure(
            "TEntry",
            padding=6
        )

        ramka = ttk.Frame(self.root, padding=25)
        ramka.pack(fill="both", expand=True)

        tytul = ttk.Label(
            ramka,
            text="Uniwersalny konwerter plików",
            font=("Arial", 17, "bold")
        )
        tytul.pack(pady=(0, 20))

        ttk.Label(
            ramka, text="Plik wejściowy:"
        ).pack(anchor="w")

        wiersz1 = ttk.Frame(ramka)
        wiersz1.pack(fill="x", pady=(5, 15))

        ttk.Entry(
            wiersz1,
            textvariable=self.plik,
            state="readonly"
        ).pack(side="left", fill="x", expand=True)

        self.przycisk_plik = ttk.Button(
            wiersz1,
            text="Wybierz plik",
            command=self.wybierz_plik
        )
        self.przycisk_plik.pack(side="left", padx=(10, 0))

        ttk.Label(
            ramka, text="Folder zapisu:"
        ).pack(anchor="w")

        wiersz2 = ttk.Frame(ramka)
        wiersz2.pack(fill="x", pady=(5, 15))

        ttk.Entry(
            wiersz2,
            textvariable=self.folder,
            state="readonly"
        ).pack(side="left", fill="x", expand=True)

        self.przycisk_folder = ttk.Button(
            wiersz2,
            text="Wybierz folder",
            command=self.wybierz_folder
        )
        self.przycisk_folder.pack(side="left", padx=(10, 0))

        ttk.Label(
            ramka, text="Format docelowy:"
        ).pack(anchor="w")

        self.lista_formatow = ttk.Combobox(
            ramka,
            textvariable=self.format,
            state="disabled"
        )
        self.lista_formatow.pack(
            fill="x", pady=(5, 20)
        )
        self.lista_formatow.bind(
            "<<ComboboxSelected>>",
            self.sprawdz_przycisk
        )

        self.przycisk_konwertuj = ttk.Button(
            ramka,
            text="Konwertuj plik",
            command=self.rozpocznij_konwersje,
            state="disabled"
        )
        self.przycisk_konwertuj.pack(pady=5)

        self.pasek = ttk.Progressbar(
            ramka,
            mode="indeterminate"
        )
        self.pasek.pack(fill="x", pady=(15, 10))

        ttk.Label(
            ramka,
            textvariable=self.status,
            wraplength=580
        ).pack(anchor="w")

        ttk.Label(
            ramka,
            text="Programowanie V - Laboratorium 4",
            foreground="#666666"
        ).pack(side="bottom", pady=(15, 0))

    def wybierz_plik(self):
        sciezka = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[
                ("Obsługiwane pliki",
                 "*.csv *.json *.txt *.docx *.odt"),
                ("Wszystkie pliki", "*.*")
            ]
        )

        if not sciezka:
            return

        self.plik.set(sciezka)

        dostepne = available_targets(Path(sciezka))

        self.lista_formatow["values"] = [
            x.replace(".", "").upper()
            for x in dostepne
        ]

        self.format.set("")

        if dostepne:
            self.lista_formatow.config(state="readonly")
            self.status.set("Wybierz format docelowy")
        else:
            self.lista_formatow.config(state="disabled")
            self.status.set("Brak dostępnych konwersji")

        self.sprawdz_przycisk()

    def wybierz_folder(self):
        sciezka = filedialog.askdirectory(
            title="Wybierz folder zapisu"
        )

        if sciezka:
            self.folder.set(sciezka)

        self.sprawdz_przycisk()

    def sprawdz_przycisk(self, event=None):
        if (
            self.plik.get()
            and self.folder.get()
            and self.format.get()
            and not self.trwa_konwersja
        ):
            self.przycisk_konwertuj.config(state="normal")
        else:
            self.przycisk_konwertuj.config(state="disabled")

    def ustaw_stan(self, trwa):
        self.trwa_konwersja = trwa

        stan = "disabled" if trwa else "normal"

        self.przycisk_plik.config(state=stan)
        self.przycisk_folder.config(state=stan)

        if trwa:
            self.lista_formatow.config(state="disabled")
            self.pasek.start(10)
        else:
            self.pasek.stop()

            if self.lista_formatow["values"]:
                self.lista_formatow.config(state="readonly")

        self.sprawdz_przycisk()

    def rozpocznij_konwersje(self):
        plik = Path(self.plik.get())
        folder = Path(self.folder.get())
        format_docelowy = self.format.get().lower()

        if not plik.is_file():
            messagebox.showerror(
                "Błąd", "Wybrany plik nie istnieje."
            )
            return

        if not folder.is_dir():
            messagebox.showerror(
                "Błąd", "Folder zapisu nie istnieje."
            )
            return

        if "." + format_docelowy not in available_targets(plik):
            messagebox.showerror(
                "Błąd", "Nieobsługiwana konwersja."
            )
            return

        wynik = folder / (plik.stem + "." + format_docelowy)

        if wynik.exists():
            messagebox.showwarning(
                "Uwaga",
                "Plik wynikowy już istnieje.\n"
                "Wybierz inny folder lub usuń poprzedni plik."
            )
            return

        self.ustaw_stan(True)
        self.status.set("Trwa konwersja...")

        watek = threading.Thread(
            target=self.wykonaj_konwersje,
            args=(plik, format_docelowy, folder),
            daemon=True
        )
        watek.start()

        self.root.after(100, self.sprawdz_wynik)

    def wykonaj_konwersje(self, plik, format_docelowy, folder):
        try:
            wynik = convert(plik, format_docelowy, folder)
            self.wyniki.put(("sukces", str(wynik)))
        except Exception as blad:
            self.wyniki.put(("blad", str(blad)))

    def sprawdz_wynik(self):
        try:
            rodzaj, komunikat = self.wyniki.get_nowait()
        except queue.Empty:
            if self.trwa_konwersja:
                self.root.after(100, self.sprawdz_wynik)
            return

        self.ustaw_stan(False)

        if rodzaj == "sukces":
            self.status.set("Konwersja zakończona pomyślnie")
            messagebox.showinfo(
                "Sukces",
                "Plik został zapisany:\n" + komunikat
            )
        else:
            self.status.set("Błąd podczas konwersji")
            messagebox.showerror(
                "Błąd konwersji", komunikat
            )


if __name__ == "__main__":
    okno = tk.Tk()
    aplikacja = KonwerterGUI(okno)
    okno.mainloop()
