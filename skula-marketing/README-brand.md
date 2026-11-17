# Skula — logo, ikona i favicon

Znak łączy dach domu z otwartą książką. Granat daje spokojny, czytelny fundament; turkus i mięta podkreślają szkolny i domowy charakter. Projekt przygotowano dla nowej marki na podstawie nazwy Skula.

Podgląd całego zestawu: [brand/preview.png](brand/preview.png).

## Pliki do użycia

| Zastosowanie | Plik |
| --- | --- |
| Logo na jasnym tle | `brand/logo.svg` lub `brand/logo.png` |
| Logo na ciemnym tle | `brand/logo-light.svg` lub `brand/logo-light.png` |
| Logo jednokolorowe | `brand/logo-mono.svg` |
| Sam znak | `brand/mark.svg`, `brand/mark-light.svg`, `brand/mark-mono.svg` |
| Ikona aplikacji | `brand/app-icon.svg`, `brand/app-icon.png` (1024 × 1024) |
| Ikona aplikacji Windows | `brand/app-icon.ico` (16, 24, 32, 48, 64, 128, 256 px) |
| Favicon | `public/favicon.svg`, `public/favicon.ico` |
| PNG favicon | `public/favicon-16x16.png`, `public/favicon-32x32.png`, `public/favicon-48x48.png` |
| Ikona Apple | `public/apple-touch-icon.png` (180 × 180, pełne tło) |
| Ikony PWA | `public/icon-192.png`, `public/icon-512.png` |
| Ikony PWA z maską | `public/icon-maskable-192.png`, `public/icon-maskable-512.png` |
| Manifest aplikacji | `public/site.webmanifest` |

Logo SVG ma tekst zamieniony na krzywe: nie wymaga czcionek i skaluje się bez utraty jakości. Logo PNG ma przezroczyste tło. Warianty `*-mono.svg` używają `currentColor`; kolor można zmieniać po osadzeniu SVG bezpośrednio w HTML. W znaczniku `<img>` nie dziedziczą koloru strony.

## Kolory i wielkości

- Granat: `#17354A`.
- Turkus: `#138F88`.
- Mięta: `#66DFCB`.
- Jasne tło podglądu: `#F4F7F8`.

Zalecana minimalna szerokość pełnego logo: 180 px. W mniejszych miejscach używaj samego znaku lub ikony. Zachowuj proporcje SVG. Wokół znaku pozostaw co najmniej 12% jego szerokości wolnej przestrzeni. Logo jasne jest przygotowane do ciemnego tła, a podstawowe do jasnego.

## Podłączenie do strony

Udostępnij zawartość katalogu `public` pod głównym adresem strony. W HTML dodaj:

```html
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#17354A">
```

Jeśli aplikacja działa w podkatalogu, dostosuj adresy powyżej i ścieżki ikon w manifeście. Sam manifest dostarcza nazwę i ikony; obsługa instalacji PWA zależy od aplikacji.

Aby używać logo jako pliku strony, skopiuj wybrany SVG do katalogu publicznego, np. `public/logo.svg`, i użyj:

```html
<img src="/logo.svg" alt="Skula" width="220">
```

## Ponowny eksport

Źródła SVG i litery w krzywych buduje `scripts/build-brand.ps1` w Windows (systemowa czcionka Segoe UI). Eksport PNG/ICO wykonuje `scripts/export-brand.cjs` z Node.js i biblioteką `sharp`:

```powershell
./scripts/build-brand.ps1
node ./scripts/export-brand.cjs
```

Biblioteka `sharp` musi być dostępna dla Node.js; w tej sesji użyto pakietów środowiska Codex, bez instalowania zależności w projekcie. Gotowe pliki nie potrzebują tych narzędzi.