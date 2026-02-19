<div align="center">

# Instagram DM Bulk Automation

### Powered by [SoClose](https://soclose.co) — Digital Innovation Agency

Automate your Instagram outreach with intelligent bulk DM sending.

[![License: MIT](https://img.shields.io/badge/License-MIT-575ECF.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-575ECF.svg)](https://python.org)
[![Powered by SoClose](https://img.shields.io/badge/Powered%20by-SoClose-575ECF.svg)](https://soclose.co)

</div>

---

## Features

- **Bulk DM Sending** — Automated Instagram direct messages to multiple profiles
- **Progress Tracking** — Tracks sent messages, resume where you left off
- **Secure Credentials** — Environment variables via `.env` file (never hardcoded)
- **Multi-Browser** — Firefox & Chrome support with automatic driver management
- **Human-Like Delays** — Randomized timing between actions
- **Auto-Save** — Progress saved after each message
- **Branded CLI** — Beautiful terminal interface powered by Rich

---

## Quick Start

### Prerequisites

- Python 3.9+
- Firefox or Chrome browser installed

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/InstagramMpBulk.git
cd InstagramMpBulk
pip install -r requirements.txt
```

### Configuration

```bash
cp .env.example .env
```

Edit `.env` with your Instagram credentials:

```env
INSTAGRAM_EMAIL=your_email@example.com
INSTAGRAM_PASSWORD=your_password
```

### Set Up Your Campaign

1. Add target usernames to `profile_links.csv` (one per line):

```csv
username1
username2
username3
```

> Both plain usernames and full Instagram URLs are supported.

2. Write your message in `message.txt`:

```
Hello!
I'd love to connect with you.
```

### Run

```bash
python main.py
```

The bot will open a browser, log in, and start sending messages. If 2FA is required, complete it manually in the browser then press ENTER to continue.

---

## Configuration Options

| Variable | Default | Description |
|---|---|---|
| `INSTAGRAM_EMAIL` | — | Instagram login email |
| `INSTAGRAM_PASSWORD` | — | Instagram login password |
| `BROWSER` | `firefox` | Browser to use (`firefox` or `chrome`) |
| `HEADLESS` | `false` | Run browser without visible window |
| `MESSAGE_FILE` | `message.txt` | Path to message template |
| `PROFILES_FILE` | `profile_links.csv` | Path to target profiles CSV |
| `SENT_FILE` | `already_send_message.csv` | Sent messages tracking file |
| `MAX_MESSAGES` | `10000` | Maximum messages per session |
| `MIN_DELAY` | `8` | Minimum delay between actions (seconds) |
| `MAX_DELAY` | `15` | Maximum delay between actions (seconds) |

---

## How It Works

```
profile_links.csv          message.txt
       │                        │
       ▼                        ▼
┌─────────────────────────────────────┐
│         SoClose DM Engine           │
│                                     │
│  1. Launch browser                  │
│  2. Login to Instagram              │
│  3. For each profile:               │
│     → Navigate to profile           │
│     → Click "Message"               │
│     → Type & send message           │
│     → Save progress                 │
│  4. Report results                  │
└─────────────────────────────────────┘
       │
       ▼
already_send_message.csv
```

---

## Disclaimer

This tool is provided for **educational and informational purposes only**. Automated messaging may violate Instagram's Terms of Service. Use responsibly and at your own risk. The authors are not responsible for any consequences resulting from the use of this tool.

---

<div align="center">

**Built by [SoClose](https://soclose.co)**

*Digital Innovation Through Automation & AI*

</div>
