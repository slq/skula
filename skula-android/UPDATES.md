# Aktualizacje bez Play Store — Android 0.12.0

## US-UPD-01 — sprawdzenie nowej wersji

Jako użytkownik chcę otrzymywać informację o nowej wersji bez kabla USB i ręcznego szukania APK.

- Ustawienia → Aktualizacje aplikacji pokazuje zainstalowaną wersję, stan sprawdzenia, opis zmian i rozmiar APK. „Sprawdź aktualizacje” działa ręcznie.
- Opcja „Sprawdzaj nową wersję raz dziennie” jest domyślnie włączona. Osobny, trwały JobScheduler 1703 sprawdza mały plik metadanych przy dostępnej sieci; otwarcie aplikacji również sprawdza, jeżeli minęła doba. Harmonogram nie resetuje się przy każdym wejściu; system może opóźnić pracę w tle.
- Sprawdzenie nie wymaga logowania do dziennika, nie zmienia interwału jego odczytów i nie wysyła danych szkoły lub konta. Wyłączenie sprawdzania w tle pozostawia przycisk ręczny.
- Nowe wydanie daje powiadomienie z osobnego kanału „Aktualizacje Skula”, najwyżej raz dla danej wersji. Dotknięcie otwiera Ustawienia. Gdy powiadomienia są zablokowane, informacja pozostaje w aplikacji.
- Stałe źródło to `https://github.com/slq/skula/releases/latest/download/skula-android-update.json`. Brak wydania (404) i błąd połączenia mają osobne komunikaty. Opublikowane wydanie musi zawierać ten plik; wydanie desktopu oznaczone jako latest bez tego pliku przerwie odnajdywanie aktualizacji Androida.

## US-UPD-02 — pobieranie i bezpieczna instalacja

Jako użytkownik chcę świadomie wybrać aktualizację i zachować lokalne dane.

- Pobranie APK zaczyna się po „Pobierz aktualizację”, z paskiem postępu i anulowaniem. Plik trafia do prywatnego cache, bez uprawnienia do pamięci telefonu.
- Metadane mają ścisły format: schema, packageName, versionCode, versionName, apkUrl, sha256, size, notes. Dozwolone są wyłącznie wersjonowane APK z repozytorium slq/skula; przekierowania wyłącznie HTTPS na GitHub i hosty jego plików. Brak cookies lub nagłówków konta. Limit metadanych 64 KiB, APK 150 MiB; niepełny lub uszkodzony plik nie trafia do instalatora.
- Przed instalacją sprawdzamy ponownie SHA-256, rozmiar, nazwę pakietu, rzeczywistą wyższą wersję, minimalny SDK, brak debuggable i zgodność aktualnego certyfikatu. Przekierowanie na dowolny serwer, obcy pakiet/podpis, downgrade i niepodpisany APK są odrzucane.
- „Zainstaluj aktualizację” wyjaśnia wymaganą zgodę Androida dla Skula. Użytkownik włącza ją w ustawieniach i wraca do przycisku; nie instalujemy automatycznie po powrocie.
- PackageInstaller dostaje wyłącznie sprawdzony APK i wymaga potwierdzenia aktualizacji. Anulowanie lub błąd nie usuwa aplikacji, archiwum, konta, statusów zadań czy przypomnień. Zapisana informacja o pobranej wersji pozwala wrócić do instalacji po ponownym otwarciu. Po udanej aktualizacji plik starej wersji jest sprzątany.

## Pierwsza instalacja na telefonie rodziny

1. Udostępnij **Skula-android-0.14.0.apk** przez link do wydania albo inną usługę plikową.
2. Na telefonie pobierz i otwórz APK. Zezwól źródłu (np. przeglądarce) na instalowanie, jeśli Android o to poprosi.
3. Zaloguj szkolne konto. Dane, własne przypomnienia i archiwum są lokalne dla każdego telefonu.
4. Kolejne wersje sprawdzisz w Ustawieniach. Zgoda na aktualizacje wewnątrz Skula jest osobną zgodą dla tego źródła.

## Budowanie i publikowanie

```powershell
powershell -ExecutionPolicy Bypass -File .\Build.ps1 -Release
# Dopiero po sprawdzeniu wydania, z GITHUB_TOKEN w środowisku procesu:
powershell -ExecutionPolicy Bypass -File .\Publish-Release.ps1 -Version 0.14.0
# Opcjonalnie przygotuj wyłącznie draft: dodaj -Draft.
```

Skrypt budowania tworzy w artifacts:

- `Skula-android-0.14.0.apk` oraz `.sha256`;
- `skula-android-update.json` — metadane wskazujące ten konkretny APK;
- `Skula-android-0.14.0-source.zip` — odpowiadające źródła, bez SDK, kluczy, stanów konta i lokalnych konfiguracji.

Skrypt publikacji potrzebuje tokenu GitHub z prawem Contents: write wyłącznie do slq/skula. Nie wpisuj tokenu do pliku repozytorium ani czatu. Wydanie najpierw powstaje jako draft, otrzymuje wszystkie trzy pliki i dopiero potem jest publikowane jako latest. Alternatywnie utwórz wydanie `android-v0.14.0` w interfejsie GitHub, dodaj te trzy pliki i oznacz jako latest. Publikacja nie następuje przy samym budowaniu APK.

Przy nowej wersji zwiększ versionCode, versionName, nazwę artefaktu w Build.ps1 i opis RELEASE_NOTES.md. Nie zmieniaj podpisu. Dla testów Gradle obsługuje nadpisanie `-PskulaVersionCode` i `-PskulaVersionName`; testowe wydania nie są publikowane.

## Podpis i zachowanie danych

APK release ma wyłączone debuggable, ale **celowo używa istniejącego lokalnego certyfikatu**, którym podpisano dotychczasowe wersje. Nie tworzono nowego klucza ani pliku hasła. To umożliwia aktualizację między wydaniami Skuli z tym samym pakietem. Przejście z poprzedniej aplikacji wymaga importu JSON.

Publiczny SHA-256 certyfikatu: `0b022decbecb6f36fa5279f98d4451165f3ade0b3dca2d50019e5039a10217fe`.

Zabezpiecz prywatną kopię dotychczasowego magazynu `%USERPROFILE%/.android/debug.keystore`; nie publikuj go. Po przeniesieniu budowania na inny komputer trzeba użyć tego samego magazynu — automatycznie wygenerowany nowy klucz nie zaktualizuje istniejących instalacji. Ewentualne przejście na inny klucz wymaga osobnego planu migracji.

## Skula 0.13.0 — nowy pakiet i repozytorium

Nowy pakiet: pl.skula.android. Poprzednia aplikacja nie może otrzymać tego APK jako aktualizacji — weryfikacja pakietu celowo to blokuje. Pierwszą Skulę instaluje się osobno i importuje JSON. Kolejne wydania Skuli używają tego samego pakietu i podpisu.

Repozytorium to slq/skula. Skula 0.13.1 używa jego adresu dla skula-android-update.json oraz wersjonowanych APK. Skula 0.13.0 wskazywała nieistniejące slq/skula-home; dla tej wersji przygotowano repozytorium zgodności z wydaniem przejściowym 0.13.1. Po instalacji dalsze aktualizacje trafiają już do slq/skula. Starsze załączniki wydań LibrusApp zachowują dawne nazwy i pakiet.
