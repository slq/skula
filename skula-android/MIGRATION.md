# Migracja do Skula 0.13.0

Skula ma pakiet Androida pl.skula.android. Android widzi ją jako osobną aplikację. Nazwa w ikonach, powiadomieniach, kluczach prywatnego zapisu, linkach wewnętrznych i nowych kopiach to Skula. Desktop: folder skula-app, moduł skula_app; Android: folder skula-android, adapter skula_shared.

## Telefon

1. W dotychczasowej aplikacji 0.12.1 wyeksportuj kopię JSON poza prywatny katalog aplikacji. Sprawdź podsumowanie, wybierając import i anuluj przed zastąpieniem danych.
2. Jeśli korzystasz z kalendarza Google, wyłącz synchronizację i użyj przycisku usuwania wpisów dodanych przez starą aplikację. Dotyczy to tylko jej eksportowanych wydarzeń. Zmiana pakietu zmienia właściciela wpisów; Skula nie przejmuje automatycznie starych wydarzeń.
3. Zainstaluj Skula obok poprzedniej aplikacji. Wybierz Ustawienia → Kopia danych i ustawień → Importuj kopię JSON.
4. Sprawdź podsumowanie i potwierdź import. Zaloguj się na to samo konto Synergia.
5. Nadaj zgody na powiadomienia i dokładne alarmy. Wybierz ponownie kalendarz Google, jeśli chcesz synchronizacji.
6. Sprawdź archiwum, zadania i przyszłe przypomnienia. Wyłącz stare przypomnienia/pobieranie albo dopiero po sprawdzeniu odinstaluj poprzednią aplikację, aby uniknąć podwójnych alarmów.

Import nie odczytuje prywatnych plików starej aplikacji i nie przenosi hasła ani sesji. Nazwa starego formatu jest zachowana wyłącznie w walidatorze zgodności. Nowe kopie używają Skula-backup. Klucz podpisu nie został zmieniony w ramach zmiany nazwy.

## Windows

Nowe instalacje używają %LOCALAPPDATA%/Skula. Wykrywanie istniejącego starego zaszyfrowanego zapisu jest zachowane, aby nie zgubić konta i archiwum. Dawna nazwa katalogu pojawia się tylko w mechanizmie zgodności; zapis nie jest automatycznie kopiowany ani odszyfrowywany poza DPAPI.

## GitHub

Skula 0.13.1 pobiera kolejne aktualizacje z slq/skula. Dla już zainstalowanej Skuli 0.13.0 wydanie przejściowe udostępniono pod adresem slq/skula-home, którego oczekuje jej aktualizator. Pakiet i podpis 0.13.1 są zgodne ze Skulą 0.13.0, więc można ją zaktualizować bez ponownego importu JSON. Wydania LibrusApp pozostają osobnymi instalacjami.
