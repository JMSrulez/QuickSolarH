import logging
import time
from datetime import datetime, timezone

from .config import settings
from .db import Base, SessionLocal, engine
from .models import CollectorStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("solar-huawei-collector")


def update_status(state: str, message: str, error_message: str | None = None) -> None:
    now = datetime.now(timezone.utc)
    with SessionLocal() as session:
        status = session.get(CollectorStatus, 1)
        if status is None:
            status = CollectorStatus(id=1, state=state, message=message)
            session.add(status)
        status.state = state
        status.message = message
        status.last_attempt_at = now
        status.error_message = error_message
        session.commit()


def collect_once() -> None:
    update_status("checking_configuration", "Vérification de la configuration Huawei.")
    if not settings.huawei_api_base_url or not settings.huawei_api_username or not settings.huawei_system_code:
        update_status(
            "waiting_configuration",
            "Configuration Huawei incomplète : URL, utilisateur ou systemCode manquant.",
        )
        logger.warning(
            "Huawei API not configured; waiting for HUAWEI_API_BASE_URL, "
            "HUAWEI_API_USERNAME, and HUAWEI_SYSTEM_CODE."
        )
        return
    if not settings.site_ids:
        update_status(
            "waiting_sites",
            "Identifiants de fermes absents : attente de HUAWEI_SITE_IDS.",
        )
        logger.warning("No site IDs configured; waiting for HUAWEI_SITE_IDS.")
        return

    update_status(
        "provider_pending",
        "Configuration détectée. Le client Huawei sera activé dans la prochaine étape.",
    )
    logger.info("Huawei provider configuration detected for %d site(s).", len(settings.site_ids))


def main() -> None:
    Base.metadata.create_all(bind=engine)
    update_status("starting", "Worker de collecte démarré.")
    while True:
        collect_once()
        time.sleep(settings.collect_interval_seconds)


if __name__ == "__main__":
    main()
