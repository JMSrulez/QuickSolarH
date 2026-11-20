from datetime import datetime, timezone

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select, text
from sqlalchemy.orm import Session

from .db import Base, engine, get_session
from .models import SiteMeasurement

app = FastAPI(title="Solar Huawei Dashboard API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/dashboard")
def dashboard(session: Session = Depends(get_session)) -> dict:
    measurements = session.scalars(
        select(SiteMeasurement)
        .order_by(desc(SiteMeasurement.measured_at))
        .limit(100)
    ).all()
    latest_by_site: dict[str, SiteMeasurement] = {}
    for measurement in measurements:
        latest_by_site.setdefault(measurement.site_id, measurement)

    return {
        "updated_at": datetime.now(timezone.utc),
        "sites": [
            {
                "site_id": measurement.site_id,
                "measured_at": measurement.measured_at,
                "solar_power_w": measurement.solar_power_w,
                "consumption_power_w": measurement.consumption_power_w,
                "battery_power_w": measurement.battery_power_w,
                "battery_state_of_charge": measurement.battery_state_of_charge,
                "grid_power_w": measurement.grid_power_w,
            }
            for measurement in latest_by_site.values()
        ],
    }
