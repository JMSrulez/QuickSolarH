from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import httpx


class HuaweiApiError(RuntimeError):
    pass


class HuaweiClient:
    def __init__(self, base_url: str, username: str, system_code: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.system_code = system_code
        self._client = httpx.Client(timeout=30.0)
        self._xsrf_token: str | None = None

    def close(self) -> None:
        self._client.close()

    def login(self) -> None:
        response = self._client.post(
            f"{self.base_url}/thirdData/login",
            json={"userName": self.username, "systemCode": self.system_code},
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("failCode") not in (None, 0) or payload.get("success") is False:
            raise HuaweiApiError(
                f"Login Huawei refusé (failCode={payload.get('failCode')})."
            )

        self._xsrf_token = response.headers.get("XSRF-TOKEN")
        if not self._xsrf_token:
            raise HuaweiApiError("Login Huawei réussi mais XSRF-TOKEN absent.")

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not self._xsrf_token:
            self.login()
        response = self._client.post(
            f"{self.base_url}{path}",
            json=payload,
            headers={"XSRF-TOKEN": self._xsrf_token or ""},
        )
        response.raise_for_status()
        result = response.json()
        if result.get("failCode") not in (None, 0) or result.get("success") is False:
            raise HuaweiApiError(
                f"API Huawei refusée pour {path} (failCode={result.get('failCode')})."
            )
        return result

    def list_stations(self) -> list[dict[str, Any]]:
        result = self._post("/thirdData/stations", {"pageNo": 1, "pageSize": 100})
        data = result.get("data") or {}
        stations = data.get("list") if isinstance(data, dict) else None
        if not isinstance(stations, list):
            raise HuaweiApiError("Réponse Huawei stations sans liste de fermes.")
        return [station for station in stations if isinstance(station, dict)]

    def get_real_kpi(self, site_ids: Iterable[str]) -> dict[str, Any]:
        return self._post(
            "/thirdData/getStationRealKpi",
            {"stationCodes": ",".join(site_ids)},
        )
