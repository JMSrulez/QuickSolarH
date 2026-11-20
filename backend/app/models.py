from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class SiteMeasurement(Base):
    __tablename__ = "site_measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[str] = mapped_column(String(120), index=True)
    measured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True
    )
    solar_power_w: Mapped[float | None] = mapped_column(Float)
    consumption_power_w: Mapped[float | None] = mapped_column(Float)
    battery_power_w: Mapped[float | None] = mapped_column(Float)
    battery_state_of_charge: Mapped[float | None] = mapped_column(Float)
    grid_power_w: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class CollectorStatus(Base):
    __tablename__ = "collector_status"

    id: Mapped[int] = mapped_column(primary_key=True, default=1)
    state: Mapped[str] = mapped_column(String(40))
    message: Mapped[str] = mapped_column(String(500))
    last_attempt_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_success_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(String(500))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
