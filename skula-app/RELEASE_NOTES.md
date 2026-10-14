Skula Windows 0.2.0

- Jasny motyw zgodny wizualnie ze Skulą na Androida: wspólne kolory, znak aplikacji, ikony, miętowe zaznaczenia i zaokrąglone karty.
- Nowy Start z pełnym planem na Dzisiaj / Jutro, nowościami z ostatniego odczytu, ostatnimi ocenami i nadchodzącymi wydarzeniami.
- Filtr Wszystkie / Nieprzeczytane w wiadomościach, współpracujący z lokalnym wyszukiwaniem.
- Spójny wygląd kalendarza, list, podglądów i ustawień.
- Dokumentacja ze zrzutami działającej aplikacji oraz skrypty do odtworzenia ikon, zrzutów i paczki wydania.

Uruchomienie:
1. Pobierz Skula-windows-0.2.0.zip i rozpakuj do nowego folderu.
2. Uruchom Demo.cmd, aby zobaczyć fikcyjne dane, albo Start.cmd, aby używać konta Synergia.
3. Wymagany jest standardowy Python 3.11+ z pip i tkinter. Pierwsze uruchomienie tworzy .venv i pobiera biblioteki.

Aktualizacja z 0.1.1:
Zamknij poprzednią wersję i uruchom Start.cmd z nowego folderu. Lokalizacja oraz format szyfrowanego zapisu nie zmieniają się; dane konta i przypomnienia pozostają poza folderem aplikacji. Nie przenoś starego katalogu .venv do nowej paczki.

Weryfikacja:
180 testów zaliczonych, 2 pominięte i 16 subtestów zaliczonych na Windows / Python 3.12.10. Sprawdzono okna 1080×720 i 1280×880, długie tytuły, pełne listy, filtry i podgląd danych bez odczytów sieciowych. Testy oraz zrzuty korzystają wyłącznie z danych syntetycznych.

Paczka ZIP zawiera aplikację, odpowiadający kod źródłowy, licencje i dokumentację (AGPL-3.0-or-later). To wydanie desktopowe nie zmienia wersji Androida ani jego kanału aktualizacji.
