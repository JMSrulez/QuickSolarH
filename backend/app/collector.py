import logging
import time

from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("solar-huawei-collector")


def collect_once() -> None:
    if not settings.huawei_api_base_url or not settings.huawei_api_key:
        logger.warning(
            "Huawei API not configured; waiting for HUAWEI_API_BASE_URL and "
            "HUAWEI_API_KEY."
        )
        return
    if not settings.site_ids:
        logger.warning("No site IDs configured; waiting for HUAWEI_SITE_IDS.")
        return

    # The provider client will be implemented after the official endpoint and
    # authentication format are confirmed.
    logger.info("Huawei provider configuration detected for %d site(s).", len(settings.site_ids))


def main() -> None:
    while True:
        collect_once()
        time.sleep(settings.collect_interval_seconds)


if __name__ == "__main__":
    main()
