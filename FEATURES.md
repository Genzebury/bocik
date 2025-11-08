# Bocik Bot - Features Overview

## 1. Slash Command: /mute

**Purpose:** Wycisza użytkownika poprzez nadanie roli "Muted"

**Usage:**
```
/mute @użytkownik [opcjonalny powód]
```

**Example:**
```
/mute @JanKowalski Spam
```

**Features:**
- ✅ Automatycznie tworzy rolę "Muted" jeśli nie istnieje
- ✅ Ustawia odpowiednie uprawnienia w kanałach (brak wysyłania wiadomości, mówienia, reakcji)
- ✅ Wysyła embed z potwierdzeniem
- ✅ Próbuje powiadomić użytkownika o wyciszeniu przez DM
- ✅ Wymaga uprawnień "Manage Roles" dla moderatora i bota

**Permission Checks:**
- Moderator musi mieć uprawnienie `manage_roles`
- Bot musi mieć uprawnienie `manage_roles`
- Rola bota musi być wyżej w hierarchii niż rola "Muted"

---

## 2. Automatic Message Responses

**Purpose:** Automatyczne odpowiedzi na określone słowa kluczowe

**Default Triggers:**
| Trigger Word | Bot Response |
|--------------|--------------|
| cześć | Witaj! 👋 |
| hello | Hello! 👋 |
| siema | Siema! 😊 |
| pomocy | Jak mogę pomóc? 🤔 |
| help | How can I help you? 🤔 |

**How it works:**
- Bot nasłuchuje wiadomości na serwerze
- Jeśli wiadomość zawiera słowo kluczowe, bot odpowiada
- Można konfigurować własne triggery w `config.json`
- Bot odpowiada tylko raz na wiadomość (pierwszy znaleziony trigger)

**Example:**
```
User: cześć jak się masz?
Bot: Witaj! 👋
```

---

## 3. DM Logging & Webhook Forwarding

**Purpose:** Zapisuje wiadomości prywatne i wysyła je jako webhoki

**What happens when a user sends a DM to the bot:**

1. **Local Logging** - Wiadomość jest zapisywana do `dm_logs.json`:
```json
{
  "timestamp": "2024-11-08T19:00:00.000000",
  "author": "User#1234",
  "author_id": 123456789,
  "content": "Treść wiadomości",
  "attachments": ["https://cdn.discord.com/..."]
}
```

2. **Webhook Forwarding** - Wiadomość jest wysyłana jako embed przez webhook:
   - Title: "📨 Nowa wiadomość prywatna"
   - Author: Nazwa i avatar użytkownika
   - Content: Treść wiadomości
   - Footer: ID użytkownika
   - Attachments: Lista załączników (jeśli są)

3. **User Confirmation** - Bot odpowiada użytkownikowi:
```
✅ Twoja wiadomość została zapisana i przekazana!
```

**Configuration:**
- Webhook URL jest opcjonalny
- Jeśli nie skonfigurowany, wiadomości są tylko zapisywane lokalnie
- Lokalny log zawsze działa (zapisuje do `dm_logs.json`)

---

## 4. Security Features

**Configuration Protection:**
- `config.json` jest w `.gitignore` - nie zostanie commitowany
- `dm_logs.json` jest w `.gitignore` - prywatność użytkowników
- Token bota nigdy nie jest logowany ani wyświetlany

**Dependency Security:**
- ✅ All dependencies scanned for vulnerabilities
- ✅ Using aiohttp >= 3.9.4 (patched versions)
- ✅ discord.py >= 2.3.0 (latest stable)

**Permission Model:**
- Bot wymaga tylko niezbędnych uprawnień
- Slash commands wymagają odpowiednich ról
- Sprawdzanie uprawnień przed wykonaniem akcji

---

## 5. Error Handling

**Bot gracefully handles:**
- Missing permissions (informuje użytkownika)
- User not found (walidacja)
- Role already assigned (informuje że użytkownik już jest wyciszony)
- DM disabled users (próbuje wysłać DM, ale nie crashuje jeśli się nie uda)
- Invalid configuration (wyświetla jasny komunikat błędu)
- Webhook errors (loguje błąd ale nie przerywa działania)

---

## 6. Setup and Configuration

**Quick Start:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup wizard
python setup.py

# 3. Start the bot
python bot.py
```

**Testing:**
```bash
# Run tests to verify setup
python test_bot.py
```

**Expected output when bot starts:**
```
Synced slash commands
Bot zalogowany jako BocikBot#1234 (ID: 123456789)
------
```

---

## Technical Details

**Discord.py Version:** 2.3.0+
**Python Version:** 3.8+

**Required Intents:**
- `message_content` - To read message content for triggers
- `members` - To manage roles
- `dm_messages` - To receive DMs

**Bot Architecture:**
- Event-driven design using discord.py
- Async/await for non-blocking operations
- JSON-based configuration
- Modular command structure with error handlers

**File Structure:**
```
bot.py              - Main bot code (~260 lines)
config.json         - Bot configuration (created by user)
config.example.json - Template configuration
setup.py            - Interactive setup wizard
test_bot.py         - Automated tests
requirements.txt    - Python dependencies
dm_logs.json        - DM message log (generated at runtime)
```
