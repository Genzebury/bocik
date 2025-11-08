# Bocik - Discord Bot

Prosty bot Discord w discord.py z podstawowymi funkcjami moderacji i logowania wiadomości prywatnych.

## Funkcje

- ✅ **Komenda `/mute`** - Wycisza użytkownika poprzez nadanie roli "Muted"
- ✅ **Automatyczne odpowiedzi** - Bot odpowiada na określone słowa kluczowe
- ✅ **Logowanie wiadomości prywatnych** - Zapisuje otrzymane DM i przesyła je przez webhook

## Wymagania

- Python 3.8 lub nowszy
- discord.py 2.3.0 lub nowszy
- Konto Discord Bot z odpowiednimi uprawnieniami

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone https://github.com/Genzebury/bocik.git
cd bocik
```

2. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

3. Utwórz plik konfiguracyjny:
```bash
cp config.example.json config.json
```

4. Edytuj `config.json` i uzupełnij wymagane dane:
   - `token` - Token bota Discord (z Discord Developer Portal)
   - `webhook_url` - URL webhooka do przesyłania logów DM (opcjonalne)
   - `muted_role_name` - Nazwa roli dla wyciszonych użytkowników (domyślnie "Muted")
   - `response_triggers` - Słowniczek wyzwalaczy i odpowiedzi

## Konfiguracja bota Discord

1. Przejdź do [Discord Developer Portal](https://discord.com/developers/applications)
2. Utwórz nową aplikację i dodaj bota
3. W sekcji "Bot":
   - Skopiuj token bota
   - Włącz "Message Content Intent"
   - Włącz "Server Members Intent"
4. W sekcji "OAuth2" → "URL Generator":
   - Wybierz scope: `bot` i `applications.commands`
   - Wybierz uprawnienia: `Manage Roles`, `Send Messages`, `Read Messages/View Channels`, `Use Slash Commands`
   - Użyj wygenerowanego URL do dodania bota na serwer

## Konfiguracja Webhooka (opcjonalne)

Aby bot mógł przesyłać logi DM przez webhook:

1. Na swoim serwerze Discord, przejdź do ustawień kanału gdzie chcesz otrzymywać logi
2. Przejdź do "Integracje" → "Webhooki"
3. Utwórz nowy webhook
4. Skopiuj URL webhooka do `config.json`

## Uruchomienie

```bash
python bot.py
```

Bot powinien się zalogować i wyświetlić komunikat:
```
Bot zalogowany jako BocikBot#1234 (ID: ...)
```

## Użycie

### Komenda `/mute`

Wycisza użytkownika poprzez nadanie roli "Muted":

```
/mute @użytkownik [powód]
```

**Wymagania:**
- Moderator musi mieć uprawnienie "Manage Roles"
- Bot musi mieć uprawnienie "Manage Roles"
- Rola bota musi być wyżej niż rola "Muted" w hierarchii

### Automatyczne odpowiedzi

Bot automatycznie odpowiada na wiadomości zawierające skonfigurowane słowa kluczowe. Domyślne wyzwalacze:
- `cześć` → "Witaj! 👋"
- `hello` → "Hello! 👋"
- `siema` → "Siema! 😊"
- `pomocy` → "Jak mogę pomóc? 🤔"
- `help` → "How can I help you? 🤔"

Możesz dodać własne w pliku `config.json`.

### Logowanie wiadomości prywatnych

Gdy użytkownik wyśle wiadomość prywatną do bota:
1. Wiadomość zostanie zapisana w pliku `dm_logs.json`
2. Jeśli skonfigurowany, zostanie wysłana przez webhook jako embed
3. Użytkownik otrzyma potwierdzenie: "✅ Twoja wiadomość została zapisana i przekazana!"

## Struktura plików

```
bocik/
├── bot.py                    # Główny plik bota
├── config.json               # Konfiguracja (nie commitować!)
├── config.example.json       # Przykładowa konfiguracja
├── requirements.txt          # Zależności Python
├── dm_logs.json             # Logi wiadomości prywatnych (generowane automatycznie)
├── .gitignore               # Pliki ignorowane przez git
└── README.md                # Ten plik
```

## Bezpieczeństwo

⚠️ **Ważne:** Nigdy nie udostępniaj publicznie pliku `config.json` zawierającego token bota lub URL webhooka!

Plik `config.json` jest automatycznie ignorowany przez git (sprawdź `.gitignore`).

## Rozwiązywanie problemów

### Bot się nie loguje
- Sprawdź czy token w `config.json` jest poprawny
- Upewnij się, że bot ma włączone wymagane intenty w Discord Developer Portal

### Komenda `/mute` nie działa
- Sprawdź czy bot ma uprawnienie "Manage Roles"
- Upewnij się, że rola bota jest wyżej w hierarchii niż rola "Muted"
- Sprawdź czy użytkownik wykonujący komendę ma uprawnienie "Manage Roles"

### Bot nie odpowiada na wiadomości
- Sprawdź czy "Message Content Intent" jest włączony w ustawieniach bota
- Upewnij się, że bot ma uprawnienie "Send Messages" w kanale

### Webhook nie działa
- Sprawdź czy URL webhooka w `config.json` jest poprawny
- Upewnij się, że webhook nie został usunięty z serwera

## Licencja

MIT