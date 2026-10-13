# Skula Android

**Szkolne sprawy w jednym miejscu.**

Natywna aplikacja do przeglądania dziennika Synergia: pełny plan dnia, nowości, wiadomości, oceny i zadania — z zaszyfrowaną kopią dostępną offline.

**Android 8.0+** · **Java 17 + Python 3.13** · **[AGPL-3.0-or-later](LICENSE)**

[Zrzuty ekranu](#zrzuty-ekranu) · [Instalacja](#instalacja) · [Budowanie](#budowanie-ze-źródeł) · [Dokumentacja](#dokumentacja) · [Współpraca](#współpraca)

Skula jest niezależnym, nieoficjalnym klientem. Nie jest powiązana z producentem dziennika.

## Zrzuty ekranu

Działająca aplikacja na Androidzie 12, z fikcyjnymi danymi w trybie demo. Zrzuty przedstawiają interfejs wersji 0.14.0. Kliknij obraz, aby zobaczyć go w pełnym rozmiarze.

<p align="center">
  <a href="docs/screenshots/start.png"><img src="docs/screenshots/start.png" width="200" alt="Start Skuli z powitaniem, wyborem dnia i rozwiniętą listą nowości"></a>
  <a href="docs/screenshots/timetable.png"><img src="docs/screenshots/timetable.png" width="200" alt="Pełny plan dnia z czterema lekcjami, godzinami i salami"></a>
  <a href="docs/screenshots/messages.png"><img src="docs/screenshots/messages.png" width="200" alt="Lista wiadomości z nadawcami i filtrem nieprzeczytanych"></a>
  <a href="docs/screenshots/calendar.png"><img src="docs/screenshots/calendar.png" width="200" alt="Miesięczny kalendarz z oznaczeniami dni zawierających wpisy"></a>
</p>

<p align="center"><em>Start i nowości · Pełny plan dnia · Wiadomości · Kalendarz</em></p>

## Co potrafi Skula

| Obszar | Możliwości |
| --- | --- |
| **Start** | Wszystkie nowości od poprzedniego wejścia, cały plan na dzisiaj lub jutro, zadania, wydarzenia i przypomnienia. |
| **Dziennik** | Oceny, wiadomości, ogłoszenia, frekwencja, terminarz i plan lekcji. Szczegóły wpisów oraz przejście do oficjalnego dziennika. |
| **Wyszukiwanie** | Jedna wyszukiwarka siedmiu sekcji i własnych przypomnień, filtry źródeł i sortowanie. |
| **Zadania** | Terminy, filtry i lokalne oznaczanie wykonania. Treść pobierana na żądanie. |
| **Kalendarz** | Lekcje, wydarzenia, zadania i przypomnienia w widoku miesiąca lub listy. Opcjonalny eksport do kalendarza Google na telefonie. |
| **Offline** | Zaszyfrowana kopia pobranych danych, archiwum ogłoszeń i zachowanie poprzednich wpisów przy błędzie odczytu. |
| **Przypomnienia** | Własny tekst i termin, szybkie odroczenie, alarmy lokalne oraz opcjonalne powiadomienia o zmianach w dzienniku. |
| **Kopie i aktualizacje** | Eksport/import JSON bez hasła, sprawdzanie wydań APK i instalacja zatwierdzana przez Androida. |

Aplikację można poznać **bez konta szkolnego** — wystarczy uruchomić demo.

## Instalacja

Potrzebujesz Androida **8.0 lub nowszego** oraz urządzenia **arm64-v8a**. APK zawiera także **x86_64** dla emulatorów. Telefonem referencyjnym jest Samsung Galaxy S10 z Androidem 12 / One UI 4.1; wyniki wykonanych prób opisuje [TESTING.md](TESTING.md).

### Z pliku APK

1. Otwórz [wydania projektu](https://github.com/slq/skula/releases) i wybierz wydanie Androida z plikiem APK albo [zbuduj aplikację ze źródeł](#budowanie-ze-źródeł).
2. Pobierz APK na telefon i otwórz plik. Jeśli Android poprosi o zgodę na instalowanie z tego źródła, udziel jej dla używanej przeglądarki lub menedżera plików.
3. Uruchom Skulę. Wybierz **Zobacz demo** lub **Połącz konto Synergia**.

Kolejne wersje sprawdzisz przez **Więcej → Ustawienia → Aktualizacje aplikacji**. Aktualizator weryfikuje sumę SHA-256, pakiet, wersję i podpis APK. [Opis aktualizacji](UPDATES.md).

### Przez USB

Włącz **Opcje programisty → Debugowanie USB**, podłącz jeden telefon i zaakceptuj komputer na jego ekranie. Z katalogu `skula-android` uruchom:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\Install-USB.ps1
~~~

Skrypt instaluje APK z katalogu `artifacts` i otwiera aplikację. Możesz wskazać inny pakiet lub SDK:

~~~powershell
.\Install-USB.ps1 -SdkPath 'C:/Android/Sdk' -ApkPath 'C:/Downloads/Skula-android-0.14.0.apk'
~~~

**Aktualizacja zachowuje dane, gdy pakiet i podpis pozostają zgodne.** Przejście z aplikacji sprzed zmiany nazwy wymaga eksportu i importu JSON. Przed taką migracją przeczytaj [MIGRATION.md](MIGRATION.md) oraz [BACKUPS.md](BACKUPS.md).

## Pierwsze kroki

1. Zaloguj się loginem i hasłem **Synergii otrzymanymi ze szkoły**. Zapamiętanie konta jest opcjonalne.
2. Poczekaj na odczyt siedmiu sekcji. Postęp i status połączenia są widoczne u góry ekranu.
3. Na **Starcie** wybierz Dzisiaj lub Jutro. Nowości i lekcje są rozwinięte; dotknięcie wpisu otwiera szczegóły.
4. Korzystaj z dolnego menu. Oceny, Zadania domowe, Terminarz, Frekwencję, Plan lekcji, Przypomnienia i Ustawienia znajdziesz pod **Więcej**.

Pełną treść wiadomości pobierasz osobnym przyciskiem — może to oznaczyć ją jako przeczytaną w dzienniku. **Zrobione** przy zadaniu oznacza Twój lokalny status, a nie oddanie pracy nauczycielowi.

## Dane i prywatność

Dane dziennika są pobierane bezpośrednio przez HTTPS. Skula nie wymaga własnego serwera, nie zawiera analityki ani nie wysyła danych szkolnych do usług AI.

- Kopia danych, przypomnienia i opcjonalnie hasło są szyfrowane **AES-GCM**, z kluczem w **Android Keystore**.
- Cookies i pełna treść wiadomości oraz zadań pobrana na żądanie nie są utrwalane. Metadane pozostają dostępne offline.
- Systemowe kopie zapasowe są wyłączone. Ręczny eksport tworzy **zwykły plik JSON bez hasła i sesji**, ale z danymi szkolnymi — przechowuj go prywatnie.
- Zrzuty ekranu są dostępne w zwykłych widokach; okno logowania pozostaje chronione. W szczegółach wiadomości, ogłoszeń i terminarza można skopiować widoczną treść.
- Usunięcie lokalnych danych usuwa kopię, konto, statusy zadań i przypomnienia z telefonu. Nie zmienia danych w dzienniku szkoły.

Szczegóły: [kopie danych](BACKUPS.md), [powiadomienia](NOTIFICATIONS.md), [archiwum ogłoszeń](ANNOUNCEMENTS.md).

## Jak działa odświeżanie

Automatyczny odczyt po otwarciu lub powrocie do aplikacji odbywa się nie częściej niż **co 5 minut**. Ręczne **Odśwież** omija tę przerwę; blokady nałożone przez serwer nadal obowiązują. Po HTTP 429 aplikacja wstrzymuje żądania na co najmniej godzinę.

Opcjonalne pobieranie w tle ma interwał **15, 30 lub 60 minut** oraz domyślną przerwę nocną **20:00–07:00**. Android może opóźniać pracę w tle. Odczyty po otwarciu aplikacji i lokalne przypomnienia działają niezależnie od przerwy nocnej. [Szczegóły harmonogramu](NOTIFICATIONS.md).

## Budowanie ze źródeł

Interfejs jest napisany natywnie w **Javie**. Integrację z dziennikiem realizuje **CPython 3.13 przez Chaquopy 17.0.0**, ze wspólnymi modułami wersji desktopowej.

### Wymagania

| Narzędzie | Wersja / komponenty |
| --- | --- |
| JDK | 17 lub 21; dostępne dla Gradle |
| Python | 3.13 na komputerze budującym |
| Android SDK | `platform-tools`, `platforms;android-35`, `build-tools;35.0.0` |
| Gradle | Wrapper dołączony do repozytorium |
| Skrypty pomocnicze | PowerShell na Windows |

~~~powershell
git clone --recurse-submodules https://github.com/slq/skula.git
cd skula/skula-android

powershell -ExecutionPolicy Bypass -File .\Build.ps1 -SdkPath 'C:/Android/Sdk' -PythonPath 'C:/Python313/python.exe'
~~~

Podstaw własne ścieżki SDK i Pythona. Skrypt sprawdza wspólne moduły, buduje APK debug, uruchamia testy jednostkowe i Android Lint oraz zapisuje APK i SHA-256 w `artifacts/`.

Dla pakietu release użyj lokalnego SDK w `.tools/android-sdk` i podaj Pythona 3.13:

~~~powershell
powershell -ExecutionPolicy Bypass -File .\Build.ps1 -PythonPath 'C:/Python313/python.exe' -Release
~~~

SDK w tej lokalizacji jest wymagane także przez skrypt przygotowujący metadane wydania. Python może być automatycznie wykryty w `.tools/python-host`. Wynikiem dla obecnej konfiguracji jest `artifacts/Skula-android-0.14.0.apk`, jego suma kontrolna, metadane aktualizacji i archiwum źródeł. Samo budowanie nie publikuje wydania.

Release używa istniejącego lokalnego klucza podpisu. Nowy klucz na innym komputerze nie pozwoli zaktualizować poprzedniej instalacji. Zasady podpisywania i publikacji: [UPDATES.md](UPDATES.md). SDK, środowisko Pythona i narzędzia kompilacji nie są potrzebne na telefonie.

### Testy

Testy Java i Lint są częścią `Build.ps1`. Można uruchomić je osobno po skonfigurowaniu SDK:

~~~powershell
.\gradlew.bat '-PbuildPython=C:/Python313/python.exe' :app:testDebugUnitTest :app:lintDebug
~~~

Testy mobilnej warstwy Python korzystają z zależności projektu desktopowego. Z katalogu `skula-android`:

~~~powershell
py -3.13 -m venv ..\skula-app\.venv
..\skula-app\.venv\Scripts\python.exe -m pip install -r ..\skula-app\requirements-dev.txt
..\skula-app\.venv\Scripts\python.exe -B -m unittest discover -s tests -v
~~~

Testy używają danych syntetycznych. Scenariusze Androida uruchamiaj na pustym emulatorze, bez konta szkolnego. [TESTING.md](TESTING.md) zawiera polecenia, wyniki, wymagania poszczególnych zestawów i ograniczenia weryfikacji.

## Struktura projektu

~~~text
skula-android/
├── app/src/main/
│   ├── java/pl/skula/android/   # Natywny interfejs, repozytorium, szyfrowanie i alarmy
│   ├── python/mobile_bridge.py # Sesja mobilna i obsługa odczytów
│   ├── python/skula_shared/    # Wspólna integracja z wersją desktopową
│   └── res/                    # Ikony, motyw i zasoby Androida
├── app/src/test/               # Testy jednostkowe Java
├── app/src/androidTest/        # Testy na emulatorze
├── tests/                     # Testy mobilnej warstwy Python
├── tools/                     # Synchronizacja źródeł i przygotowanie wydania
├── docs/screenshots/           # Zrzuty aplikacji z danymi demo
├── Build.ps1                   # Budowa i weryfikacja APK
└── Install-USB.ps1             # Instalacja na telefonie przez ADB
~~~

## Dokumentacja

| Temat | Dokument |
| --- | --- |
| Start, nowości i nawigacja | [HOME_SCREEN.md](HOME_SCREEN.md) |
| Kalendarz i wyszukiwanie | [CALENDAR.md](CALENDAR.md) · [SEARCH.md](SEARCH.md) |
| Zadania i archiwum ogłoszeń | [HOMEWORK.md](HOMEWORK.md) · [ANNOUNCEMENTS.md](ANNOUNCEMENTS.md) |
| Przypomnienia i odczyty w tle | [NOTIFICATIONS.md](NOTIFICATIONS.md) |
| Integracja z kalendarzem Google | [GOOGLE_CALENDAR.md](GOOGLE_CALENDAR.md) |
| Kopie i migracja | [BACKUPS.md](BACKUPS.md) · [MIGRATION.md](MIGRATION.md) |
| Wydania i historia zmian | [UPDATES.md](UPDATES.md) · [CHANGELOG.md](CHANGELOG.md) · [RELEASE_NOTES.md](RELEASE_NOTES.md) |
| Zakres i weryfikacja | [MVP_SCOPE.md](MVP_SCOPE.md) · [TESTING.md](TESTING.md) |

## Współpraca

Błędy i propozycje zmian zgłaszaj w [GitHub Issues](https://github.com/slq/skula/issues). W zgłoszeniu podaj wersję aplikacji i Androida, kroki odtworzenia, oczekiwany rezultat oraz faktyczne zachowanie. Zrzuty przygotuj w trybie demo lub usuń z nich dane osobowe.

Pull request powinien opisywać rozwiązywany problem i sposób weryfikacji. Przy zmianach interfejsu dołącz zrzuty demo; przy zmianach logiki uzupełnij odpowiednie testy.

Adapter dziennika i logika porównywania danych mają źródło w `../skula-app/skula_app/`. Po zmianie tych modułów i sprawdzeniu testów odtwórz kopię Androida:

~~~powershell
python tools/sync_shared.py
python tools/sync_shared.py --check
~~~

Nie dodawaj do repozytorium haseł, cookies, kopii kont, eksportów szkolnych ani kluczy podpisu. Wersja Android obsługuje obecnie jedno konto; zgodność integracji może zależeć od konfiguracji szkoły.

## Licencja i podziękowania

Kod Skuli jest dostępny na **[AGPL-3.0-or-later](LICENSE)**. Informacje o autorach integracji, pochodzeniu kodu i licencjach bibliotek znajdują się w [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

Projekt korzysta m.in. z Chaquopy, CPythona, librus-apix oraz integracji opartej na librus_pyapi. Udostępniając APK, zachowaj odpowiadające mu źródła i informacje licencyjne.
