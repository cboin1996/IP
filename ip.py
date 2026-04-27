import os
import time
import logging
import requests

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

DUCKDNS_TOKEN = os.environ["DUCKDNS_TOKEN"]
DUCKDNS_DOMAIN = os.environ["DUCKDNS_DOMAIN"]
CHECK_INTERVAL = float(os.environ.get("CHECK_INTERVAL_HOURS", "1"))
FAULT_INTERVAL = float(os.environ.get("FAULT_INTERVAL_HOURS", str(1 / 6)))


def get_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=10).text.strip()
    except Exception as e:
        logger.warning("Failed to get IP: %s", e)
        return None


def update_duckdns(ip):
    url = (
        f"https://www.duckdns.org/update"
        f"?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip={ip}&verbose=true"
    )
    resp = requests.get(url, timeout=10)
    if resp.text.startswith("OK"):
        logger.info("DuckDNS updated: %s -> %s.duckdns.org", ip, DUCKDNS_DOMAIN)
    else:
        logger.error("DuckDNS update failed: %s", resp.text)


def main():
    current_interval = CHECK_INTERVAL
    last_ip = get_ip()

    if last_ip:
        logger.info("Starting. Current IP: %s", last_ip)
        update_duckdns(last_ip)
    else:
        logger.warning("No connectivity on start, retrying every %.0f min", FAULT_INTERVAL * 60)
        current_interval = FAULT_INTERVAL

    while True:
        logger.info("Next check in %.0f min", current_interval * 60)
        time.sleep(current_interval * 3600)

        current_ip = get_ip()

        if current_ip is None:
            current_interval = FAULT_INTERVAL
            continue

        current_interval = CHECK_INTERVAL

        if current_ip != last_ip:
            logger.info("IP changed: %s -> %s", last_ip, current_ip)
            update_duckdns(current_ip)
            last_ip = current_ip
        else:
            logger.info("No change: %s", current_ip)


if __name__ == "__main__":
    main()
