Skula Windows 0.3.0

- Oceny można przeglądać według daty albo grupować według przedmiotów. Domyślnie najnowsze oceny są na górze.
- Grupy przedmiotów mają liczniki i można je zwijać. Wyszukiwanie oraz szczegóły ocen działają w obu widokach.
- Wybrany widok i zwinięte grupy są zachowywane podczas nawigacji i odświeżania w bieżącej sesji.
- Starsze zapisane oceny bez osobnego pola przedmiotu nadal są obsługiwane; widok działa na lokalnej kopii bez dodatkowego odczytu dziennika.
- Dokumentacja zawiera zrzuty obu widoków ocen.

Uruchomienie:
1. Pobierz Skula-windows-0.3.0.zip i rozpakuj do nowego folderu.
2. Uruchom Demo.cmd, aby zobaczyć fikcyjne dane, albo Start.cmd, aby używać konta Synergia.
3. Wymagany jest standardowy Python 3.11+ z pip i tkinter. Pierwsze uruchomienie tworzy .venv i pobiera biblioteki.

Aktualizacja z 0.2.0:
Zamknij poprzednią wersję i uruchom Start.cmd z nowego folderu. Lokalizacja oraz format szyfrowanego zapisu nie zmieniają się; dane konta i przypomnienia pozostają poza folderem aplikacji. Nie przenoś starego katalogu .venv do nowej paczki.

Weryfikacja:
194 testy zaliczone, 2 pominięte i 16 subtestów zaliczonych na Windows / Python 3.12.10. Sprawdzono oba widoki, sortowanie, wyszukiwanie, szczegóły, starsze kopie, brak fałszywych powiadomień oraz okna 1080×720 i 1280×880. Testy i zrzuty korzystają wyłącznie z danych syntetycznych.

Paczka ZIP zawiera aplikację, odpowiadający kod źródłowy, licencje i dokumentację (AGPL-3.0-or-later). Python nie jest dołączony do paczki.
