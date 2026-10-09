# Skula

Repozytorium aplikacji **Skula** do konta dziennika Synergia: wersji desktopowej dla Windows oraz mobilnej dla Androida. Obie pokazują dane dziennika i przechowują zaszyfrowaną kopię na urządzeniu.

Projekt jest niezależnym, nieoficjalnym klientem. Nie jest powiązany z producentem dziennika. Wersja desktopowa: **0.1.1**, Android: **0.13.0**. Status: prototypy rozwijane i sprawdzane lokalnie.

## Zmiana nazwy i migracja

Od 0.13.0 aplikacja nazywa się **Skula**, a pakiet Androida to pl.skula.android. To nowa aplikacja dla Androida: najpierw wyeksportuj JSON w poprzedniej wersji 0.12.1, zainstaluj Skulę obok niej i zaimportuj kopię. [Instrukcja migracji](skula-android/MIGRATION.md). Aktualizator Skuli oczekuje przyszłego repozytorium slq/skula-home; zadziała po jego zmianie nazwy i publikacji nowych plików.

## Możliwości

Repozytorium zawiera dwie aplikacje: [Skula dla Windows](skula-app/README.md) i [Skula dla Androida](skula-android/README.md). Wersja Android ma APK do instalacji przez USB, z logowaniem, odczytem danych po otwarciu, limitem 5 minut, lokalnymi przypomnieniami, zadaniami domowymi i opcjonalnymi powiadomieniami. Od 0.12.0 ma wbudowany aktualizator APK z GitHub Releases, opis zmian i instalację z potwierdzeniem Androida. Od 0.11.0 zachowuje pobrane ogłoszenia w zaszyfrowanym archiwum konta, także po ich zniknięciu z dziennika i zmianie roku. Od 0.10.0 ma wspólną wyszukiwarkę wszystkich pobranych sekcji i własnych przypomnień, dostępną ze Startu i Więcej. Od 0.9.0 pokazuje na Starcie nowe i zmienione wpisy od poprzedniego wejścia, także pobrane w tle. Od 0.8.0 pozwala oznaczać zadania jako zrobione i cofać ten lokalny status. Od 0.7.0 ma ekran Start „Dzisiaj / Jutro” i dolne menu z pozostałymi panelami pod Więcej. Jej [zakres pierwszej wersji](skula-android/MVP_SCOPE.md) opisuje adaptację wymagań desktopu.

- Oceny, wiadomości, ogłoszenia, frekwencja i plan lekcji.
- Terminarz w widoku kalendarza z listą poniżej lub samej listy.
- Wyszukiwanie i sortowanie wpisów oraz osobne pobieranie treści wiadomości.
- Powiadomienia Windows o nowych lub zmienionych danych.
- Własne przypomnienia z treścią i terminem dla wiadomości, ogłoszeń i wydarzeń.
- Zaszyfrowana kopia lokalna danych i opcjonalne zapamiętanie konta przez Windows DPAPI.
- Tryb demo z fikcyjnymi danymi, bez logowania do dziennika.

## Szybki start — Windows

Potrzebujesz Windows i standardowego Pythona **3.11 lub nowszego** z `pip` oraz `tkinter`. Testy uruchamiane są na Pythonie 3.12.

1. Sklonuj repozytorium lub rozpakuj jego ZIP do zwykłego folderu.
2. Otwórz folder [`skula-app`](skula-app/).
3. Uruchom [`Demo.cmd`](skula-app/Demo.cmd), aby obejrzeć aplikację na danych przykładowych.
4. Uruchom [`Start.cmd`](skula-app/Start.cmd), aby połączyć własne konto Synergia.

Przy pierwszym uruchomieniu skrypt tworzy `.venv` i instaluje zależności z PyPI; potrzebny jest internet. Instalator EXE nie jest jeszcze dostępny.

[README aplikacji](skula-app/README.md) zawiera instrukcję logowania, konfigurację przypomnień, informacje o danych lokalnych, ograniczenia integracji i rozwiązywanie problemów.

[USER_STORIES.md](skula-app/USER_STORIES.md) zawiera historie użytkownika dla wszystkich paneli, kryteria akceptacji, scenariusze testowe oraz kwestie do rozstrzygnięcia przed stworzeniem wersji mobilnej.

## Struktura repozytorium

```text
skula-home/
├── README.md
├── .gitignore
├── skula-app/               # Aplikacja Windows
│   ├── README.md
│   ├── USER_STORIES.md
│   ├── Start.cmd
│   ├── Demo.cmd
│   ├── Sprawdz-srodowisko.cmd
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── skula_app/
│   ├── tests/
│   ├── LICENSE
│   ├── THIRD_PARTY_NOTICES.md
│   └── licenses/
└── skula-android/           # Aplikacja Android
    ├── README.md
    ├── MVP_SCOPE.md
    ├── TESTING.md
    ├── NOTIFICATIONS.md
    ├── HOMEWORK.md
    ├── Build.ps1
    ├── Install-USB.ps1
    ├── app/
    ├── tests/
    └── tools/
```

## Rozwój i testy

Uruchom w PowerShell z katalogu głównego repozytorium:

```powershell
cd skula-app
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m skula_app --demo
.\.venv\Scripts\python.exe -m pytest tests -q
```

Testy używają osobnego magazynu danych i odpowiedzi syntetycznych. Nie potwierdzają zgodności integracji z każdym kontem lub konfiguracją szkoły.

## Prywatność i licencja

Zapis konta znajduje się poza repozytorium, domyślnie w `%LOCALAPPDATA%\Skula\state.dpapi`. Starsze instalacje zachowują obsługę zapisu w `%LOCALAPPDATA%\SzkolnyPanel`. Hasło jest zapisywane tylko po wybraniu opcji zapamiętania konta. Szczegóły ochrony danych opisano w [README aplikacji](skula-app/README.md#dane-lokalne-i-prywatność).

Nie dodawaj do repozytorium danych logowania, plików `state.dpapi`, cookies ani zrzutów ekranu z danymi uczniów lub nauczycieli. `.gitignore` wyklucza środowiska lokalne, cache Pythona i typowe pliki z danymi konta.

Kod aplikacji jest udostępniony na **AGPL-3.0-or-later**. Zachowaj [licencję](skula-app/LICENSE) oraz [informacje o źródłach i zależnościach](skula-app/THIRD_PARTY_NOTICES.md), w tym opisaną rozbieżność metadanych licencji `librus-apix`.
