# 🌌 REDDIT SPY BOT v1.0.0 (Official Release)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-speed, interactive, and anti-block CLI intelligence tool built for Termux and Linux environments. This bot monitors any targeted Subreddit for specific custom keywords in real-time, stores data locally to prevent duplicate alerts, and routes push notifications directly to your phone via Telegram.

Developed natively to bypass aggressive scraping restrictions without requiring API keys.

---

## ⚡ Core Features

* **Interactive Target Setup:** No code editing required. Input your target Subreddit and custom keywords right from the console.
* **403 Forbidden Immunity:** Uses Reddit's native RSS syndication layer instead of scraping heavy HTML structures or JSON endpoints.
* **429 Rate-Limit Resilience:** Features a smart exponential backoff engine and automated user-agent rotation to keep the bot running uninterrupted.
* **Local Data Persistence:** Saves notified post IDs to a local database (`spy_history.txt`). If the script restarts, it won't spam your phone with old alerts.
* **Dynamic Throttle:** Adjusts sleep cycles dynamically based on subreddit activity to save battery and mobile network data on Termux.
* **Optional Telegram Integration:** Get instant vibration alerts on your phone the exact second a match is found worldwide.

---

## 🛠️ Installation & Setup (Termux / Linux)

Open your terminal and run the following commands sequentially:

### 1. Update the environment and install dependencies
```bash
pkg update && pkg upgrade -y
pkg install python git -y
pip install requests --break-system-packages

