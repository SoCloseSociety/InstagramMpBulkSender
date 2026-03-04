def validate_browser(browser):
    valid_browsers = ["chrome", "firefox"]
    if browser.lower() not in valid_browsers:
        raise ValueError(f'Invalid browser type: {browser}. Must be one of {valid_browsers}')
    return browser.lower()

# ─── Configuration ───────────────────────────────────────────

load_dotenv()

INSTAGRAM_EMAIL = os.getenv("INSTAGRAM_EMAIL", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
BROWSER = validate_browser(os.getenv("BROWSER", "firefox"))
MESSAGE_FILE = os.getenv("MESSAGE_FILE", "message.txt")
PROFILES_FILE = os.getenv("PROFILES_FILE", "profile_links.csv")
SENT_FILE = os.getenv("SENT_FILE", "already_send_message.csv")
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "10000"))
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
MIN_DELAY = int(os.getenv("MIN_DELAY", "8"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "15"))