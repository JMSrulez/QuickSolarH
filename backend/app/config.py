from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://solar_huawei:change-me@postgres:5432/solar_huawei"
    )
    huawei_api_base_url: str = ""
    huawei_api_key: str = ""
    huawei_site_ids: str = ""
    collect_interval_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def site_ids(self) -> list[str]:
        return [site.strip() for site in self.huawei_site_ids.split(",") if site.strip()]


settings = Settings()
