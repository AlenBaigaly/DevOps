import psutil
import yaml
import requests
from datetime import datetime

# Загружаем конфиг с порогами
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


CPU_THRESHOLD = config.get("cpu_threshold", 80)
MEM_THRESHOLD = config.get("mem_threshold", 80)
DISK_THRESHOLD = config.get("disk_threshold", 90)

TELEGRAM_TOKEN = config.get("telegram_token")
TELEGRAM_CHAT_ID = config.get("telegram_chat_id")

LOG_FILE = "metrics.log"

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        log_message(f"Error sending Telegram message: {e}")

def log_message(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def check_system():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    log_message(f"CPU: {cpu}%\nRAM: {mem}%\nDisk: {disk}%")

    alert_messages = []

    if cpu > CPU_THRESHOLD:
        msg = f"WARNING: CPU usage {cpu}% > {CPU_THRESHOLD}%"
        log_message(msg)
        alert_messages.append(msg)
    if mem > MEM_THRESHOLD:
        msg = f"WARNING: RAM usage {mem}% > {MEM_THRESHOLD}%"
        log_message(msg)
        alert_messages.append(msg)
    if disk > DISK_THRESHOLD:
        msg = f"WARNING: Disk usage {disk}% > {DISK_THRESHOLD}%"
        log_message(msg)
        alert_messages.append(msg)

    if not alert_messages:
        log_message("ALL GOOD")
    else:
        send_message("\n".join(alert_messages))

if __name__ == "__main__":
    check_system()

