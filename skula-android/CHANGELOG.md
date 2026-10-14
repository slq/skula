# Historia zmian — Skula Android

Historia funkcji przeniesiona z README. Opis bieżącego pakietu znajduje się w [RELEASE_NOTES.md](RELEASE_NOTES.md), a zasady aktualizacji w [UPDATES.md](UPDATES.md).

## 0.15.0 — 2026-10-14

- Oceny: przełącznik **Według daty / Według przedmiotów**, rozwijane grupy z licznikami i najnowszymi ocenami na początku.
- Wyszukiwanie i szczegóły działają w obu widokach; wybór i zwinięte grupy są odtwarzane po obrocie ekranu.
- Obsługa przedmiotów w pobieranych ocenach, zapisanej kopii i eksporcie JSON. Import starszych kopii nadal działa.

## 0.14.0 — 2026-10-13

- Nowy natywny interfejs zgodny z zaakceptowanym prototypem: jasne tło, turkusowe akcenty, ikony i uporządkowane listy.
- Pełna lista nowości oraz wszystkie lekcje wybranego dnia na Starcie, bez rozwijania.
- Filtr nieprzeczytanych wiadomości oraz lekcje i przełącznik Miesiąc / Lista we wspólnym kalendarzu.
- Zrzuty aplikacji i uporządkowana dokumentacja projektu.
- Kopiowanie treści z okien szczegółów oraz zrzuty ekranu poza chronionym oknem logowania.

## 0.13.1

- Ręczne odświeżanie działa bez oczekiwania na przerwę 5 minut; automatyczne odczyty nadal respektują limit.
- Aktualizator korzysta z repozytorium slq/skula; dla wersji 0.13.0 przygotowano wydanie przejściowe pod wcześniejszym adresem.

## 0.13.0

Marka, nazwy folderów i pakiety własnego kodu zostały zmienione na Skula. Zachowano rzeczywiste domeny dziennika, nazwy bibliotek oraz identyfikatory zgodności starszych danych. Nowy pakiet Androida wymaga migracji przez eksport i import JSON. [Instrukcja migracji](MIGRATION.md).

## 0.12.1

Eksport i import kopii danych oraz ustawień w JSON, bez hasła i sesji dziennika. [Kopie i migracja](BACKUPS.md).

## 0.12.0

W 0.12.0 dodano **Ustawienia → Aktualizacje aplikacji**: sprawdzenie ręczne albo raz dziennie, opis zmian, pobranie APK na żądanie i instalację z potwierdzeniem Androida. Plik jest sprawdzany pod kątem SHA-256, wersji, pakietu i podpisu. Aktualizacje Skuli zachowują dane, jeśli pakiet i podpis są zgodne. Przejście z poprzedniej aplikacji wymaga importu JSON, ponieważ pakiet został zmieniony. [Instalacja rodzinna, publikacja i historie](UPDATES.md).

## 0.11.0

W 0.11.0 **pobrane ogłoszenia pozostają w lokalnym archiwum**, nawet gdy znikną z listy dziennika i po zmianie roku szkolnego. Ponowne pobranie tego samego wpisu zastępuje treść najnowszą wersją. Kopie są zaszyfrowane, osobne dla kont; istniejąca lista jest automatycznie migrowana. Archiwalne ogłoszenia są dostępne w wyszukiwarce i przypomnieniach. [Zasady, ograniczenie identyfikacji i historie](ANNOUNCEMENTS.md).

## 0.10.1

W 0.10.1 Ogłoszenia są trzecią zakładką dolnego menu, a Zadania domowe znajdziesz pod Więcej. Zadania nadal są dostępne w kalendarzu i na Starcie.

## 0.10.0

W 0.10.0 dodano **wspólne wyszukiwanie** ze Startu i menu Więcej: tytuły, opisy, nadawcy, przedmioty i daty wszystkich siedmiu pobranych sekcji oraz własnych przypomnień. Filtr źródła i dotknięcie wyniku prowadzą do istniejących szczegółów. Wpisy z polskimi znakami znajdziesz także bez ogonków; każde wpisane słowo musi wystąpić. Widok działa offline i nie pobiera automatycznie pełnych treści. [Historie i kryteria](SEARCH.md).

## 0.9.0

W 0.9.0 dodano **Start → Od ostatniego wejścia**. Nowe oceny, wiadomości, ogłoszenia, wydarzenia, frekwencja, lekcje i zadania są od razu widoczne w jednej liście. Możesz wybrać źródło i otworzyć szczegóły. W obecnym układzie wszystkie pozycje są od razu rozwinięte. Lista zbiera zmiany również podczas odczytów w tle i zachowuje je przy kolejnych odczytach bez zmian oraz po zamknięciu procesu. Pierwszy odczyt tworzy punkt odniesienia; wcześniejszych utraconych zmian sprzed aktualizacji nie da się odtworzyć. [Zasady i historie użytkownika](HOME_SCREEN.md#us-home-04--co-zmieniło-się-od-ostatniego-wejścia).

## 0.8.0

W 0.8.0 dodano **Zrobione** na kartach i w szczegółach zadań oraz filtry **Do zrobienia / Zrobione / Wszystkie**. Wykonane zadania znikają z planu dnia; pozostają dostępne w panelu Zadania i kalendarzu. Status działa offline, po zamknięciu aplikacji oraz po kolejnym pobraniu tych samych zadań. To własne oznaczenie na telefonie; przypomnienia i wydarzenia Google pozostają do osobnego zarządzania. [Szczegóły i historie użytkownika](HOMEWORK.md).

## 0.7.0

W 0.7.0 dodano [ekran startowy i dolną nawigację](HOME_SCREEN.md). Przełącznik **Dzisiaj / Jutro** działa na pobranej kopii, pokazuje godziny i status odczytu każdej sekcji; dotknięcie wpisu otwiera jego dotychczasowe szczegóły. Menu pozostaje widoczne podczas przewijania. **Więcej → Ustawienia** prowadzi do wszystkich opcji, w tym integracji Google.

## 0.6.0

W 0.6.0 dodano **Ustawienia → Kalendarz Google**: wybór kalendarza Google na telefonie i źródeł, automatyczne dodawanie oraz aktualizowanie wydarzeń bez duplikatów. Synchronizacja jest domyślnie wyłączona i wymaga dostępu do kalendarza. [Zasady i konfiguracja](GOOGLE_CALENDAR.md).

## 0.5.1

W 0.5.1 poprawiono odnawianie wygasłej sesji przy zapamiętanym koncie: kolejna dozwolona próba pobrania może połączyć konto automatycznie, bez wyłączania pobierania w tle. Odrzucone logowanie lub niedziałająca nowa sesja nadal zatrzymują dalsze próby. Własne przypomnienia nie wymagają sesji dziennika.

## 0.5.0

W 0.5.0 dodano osobną zakładkę **Kalendarz**, obok Przeglądu. Łączy wydarzenia z Terminarza, terminy Zadań domowych oraz własne Przypomnienia. Ma wybór miesiąca i dnia, listę poniżej, wyszukiwanie, filtry źródeł oraz kolory i etykiety rodzajów wpisów. Dotychczasowe panele pozostają dostępne; [wymagania kalendarza](CALENDAR.md).

## 0.4.1

W 0.4.1 dodano wybór interwału pobierania w tle **15 / 30 / 60 minut** (domyślnie 15) oraz domyślnie włączoną **przerwę nocną 20:00–07:00**. Możesz ją wyłączyć w Ustawieniach. Przerwa dotyczy automatycznego pobierania poza focusem; otwarcie aplikacji i własne przypomnienia nadal działają.

## 0.4.0

W 0.4.0 dodano skróty przypomnień **Za 30 minut**, **Dzień wcześniej o 18:00** i **Godzinę wcześniej** (dla wpisów z godziną). Powiadomienie przypomnienia ma akcję **Przypomnij za 30 minut**, działającą offline bez otwierania aplikacji. Automatyczne powiadomienia o zmianach we wszystkich siedmiu sekcjach są wysyłane poza focusem aplikacji. Aby je otrzymywać po zamknięciu, zapamiętaj konto i włącz w Ustawieniach **Pobieraj dane w tle** oraz **Powiadomienia o nowych danych w tle**.

## 0.3.2

W 0.3.2 naprawiono odczyt zadań domowych, których daty dziennik uzupełnia nazwą dnia tygodnia.

## 0.3.1

Od 0.3.1 pobieranie w tle jest możliwe co około 15 minut, a od 0.4.1 można wybrać także 30 lub 60 minut, również po zamknięciu okna lub zakończeniu procesu aplikacji. Połącz konto z zapamiętaniem hasła i włącz **Ustawienia → Pobieraj dane w tle**. Android może opóźniać odczyty; szczegóły w [NOTIFICATIONS.md](NOTIFICATIONS.md).

## 0.3.0

W 0.3.0 dodano [panel Zadania domowe](HOMEWORK.md), licznik i najbliższe terminy w Przeglądzie, przypomnienia oraz powiadomienia o nowych lub zmienionych zadaniach. Kliknięcie powiadomienia o zmianach otwiera Przegląd, a otwarcie przypomnienia wczytuje aktualny status z zaszyfrowanego zapisu.
