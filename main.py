#!/usr/bin/env python3
"
Instagram DM Bulk Automation — Powered by SoClose
https://soclose.co
"

import os
import sys
csv
import time
import random
import logging
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
from rich.logging import RichHandler
from rich.theme import Theme

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
    WebDriverException,
    StaleElementReferenceException,
)

# ─── SoClose Brand Theme ────────────────────────────────────

SOCLOSE_THEME = Theme(
    {
        "info": "#575ECF",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "brand": "bold #575ECF",
        "muted": "#c5c1b9",
    }
)

console = Console(theme=SOCLOSE_THEME)

# ─── Configuration ───────────────────────────────────────────

load_dotenv()

INSTAGRAM_EMAIL = os.getenv("INSTAGRAM_EMAIL", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")
BROWSER = os.getenv("BROWSER", "firefox").lower()
MESSAGE_FILE = os.getenv("MESSAGE_FILE", "message.txt")
PROFILES_FILE = os.getenv("PROFILES_FILE", "profile_links.csv")
SENT_FILE = os.getenv("SENT_FILE", "already_send_message.csv")
MAX_MESSAGES = int(os.getenv("MAX_MESSAGES", "10000"))
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
MIN_DELAY = int(os.getenv("MIN_DELAY", "8"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "15"))

# ─── Logging ─────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)],
)
log = logging.getLogger("soclose")

# ─── Helpers ─────────────────────────────────────────────────

def show_banner():
    """Display the SoClose branded banner."""
    console.print()
    console.print(
        Panel(
            "[bold #575ECF]Instagram DM Bulk Automation[/]\n"
            "[#c5c1b9]Digital Innovation Through Automation & AI[/]\n"
            "[#c5c1b9]https://soclose.co[/]",
            title="[bold #575ECF]SoClose[/]",
            border_style="#575ECF",
            padding=(1, 4),
        )
    )
    console.print()

def extract_username(value: str) -> str:
    """Extract Instagram username from a URL or plain username."""
    value = value.strip().strip("/")

    if "instagram.com" in value:
        parts = value.split("instagram.com/")
        if len(parts) > 1:
            username = parts[1].split("/")[0].split("?")[0]
            return username

    # Already a plain username
    return value

def load_message(filepath: str) -> str:
    """Load the message template from file."""
    path = Path(filepath)
    if not path.exists():
        console.print(f"[error]Message file not found: {filepath}[/]")
        sys.exit(1)
    message = path.read_text(encoding="utf-8").strip()
    if not message:
        console.print("[error]Message file is empty.[/]")
        sys.exit(1)
    log.info(f"Message loaded ({len(message)} chars)")
    return message

def load_profiles(filepath: str) -> list:
    """Load target profile usernames from CSV."""
    path = Path(filepath)
    if not path.exists():
        console.print(f"[error]Profile file not found: {filepath}[/]")
        sys.exit(1)

    profiles = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                raw = row[0].strip()
                if not raw or raw.lower() == "profile link":
                    continue
                username = extract_username(raw)
                if username:
                    profiles.append(username)

    log.info(f"Loaded {len(profiles)} profiles")
    return profiles

def load_sent(filepath: str) -> set:
    """Load the set of already-messaged usernames."""
    path = Path(filepath)
    if not path.exists():
        return set()

    sent = set()
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                raw = row[0].strip()
                if not raw or raw.lower() == "profile link":
                    continue
                username = extract_username(raw)
                if username:
                    sent.add(username)

    log.info(f"Already sent: {len(sent)} profiles")
    return sent

def save_sent(filepath: str, sent: set):
    """Save the set of messaged usernames to CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Profile Link"])
        for username in sorted(sent):
            writer.writerow([username])

def random_delay(min_sec=None, max_sec=None):
    """Sleep for a random duration to mimic human behavior."""
    lo = min_sec if min_sec is not None else MIN_DELAY
    hi = max_sec if max_sec is not None else MAX_DELAY
    time.sleep(random.uniform(lo, hi))

# ─── Browser ─────────────────────────────────────────────────

def create_driver():
    """Initialize and return the browser driver."""
    if BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        if HEADLESS:
            options.add_argument("--headless=new")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        options = webdriver.FirefoxOptions()
        options.set_preference("dom.webnotifications.enabled", False)
        if HEADLESS:
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    driver.maximize_window()
    return driver

# ─── Instagram Actions ───────────────────────────────────────

def dismiss_popup(driver, timeout=5):
    """Try to dismiss common Instagram popups (cookies, notifications)."""
    popup_xpaths = [
        "//button[contains(text(), 'Allow')]",
        "//button[contains(text(), 'Accept')]",
        "//button[contains(text(), 'Autoriser')]",
        "//button[contains(text(), 'Not Now')]",
        "//button[contains(text(), 'Pas maintenant')]",
        "//button[contains(text(), 'Plus tard')]",
        "//button[contains(text(), 'Decline')]",
    ]
    for xpath in popup_xpaths:
        try:
            btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            time.sleep(1)
            return True
        except (TimeoutException, ElementClickInterceptedException):
            continue
    return False

def login(driver):
    """Log in to Instagram."""
    console.print("[info]Navigating to Instagram login...[/]")
    driver.get("https://www.instagram.com/accounts/login/")
    random_delay(5, 8)

    # Dismiss cookie consent if present
    dismiss_popup(driver, timeout=4)

    # Enter credentials
    console.print("[info]Entering credentials...[/]")

    try:
        username_field = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        password_field = driver.find_element(By.NAME, "password")

        username_field.clear()
        username_field.send_keys(INSTAGRAM_EMAIL)
        time.sleep(0.5)
        password_field.clear()
        password_field.send_keys(INSTAGRAM_PASSWORD)
        time.sleep(0.5)

        # Submit login
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        console.print("[info]Login submitted.[/]")

        random_delay(5, 8)

        # Wait for user to handle 2FA or any manual verification
        console.print(
            "[warning]If 2FA or a challenge appears, complete it in the browser now.[/]"
        )
        input("\n  Press ENTER once you are logged in and ready to continue... ")
        console.print()

        random_delay(2, 4)

        # Dismiss "Turn on notifications" popup
        dismiss_popup(driver, timeout=4)

        console.print("[success]Login complete.[/]")
    except Exception as e:
        log.error(f"An error occurred during login: {e}")
        sys.exit(1)

def find_and_click_message_button(driver) -> bool:
    """Find and click the Message button on a profile page."""
    selectors = [
        (By.XPATH, "//div[@role='button'][text()='Message']"),
        (By.XPATH, "//div[text()='Message']/ancestor::*[@role='button']"),
        (By.XPATH, "//div[text()='Message']"),

... (truncated, 196 more lines)