from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Sports Media Guardian AI"
    app_env: str = "development"
    database_url: str = "sqlite:///./sports_media_guardian.db"
    upload_dir: str = "./data/uploads"
    watermark_dir: str = "./data/watermarked"
    temp_dir: str = "./data/temp"
    embedding_backend: str = "clip-fallback"
    default_visible_watermark: str = "OFFICIAL SPORTS MEDIA"
    similarity_threshold: float = 0.68
    incident_threshold: float = 0.72
    enable_provenance: bool = True
    enable_watermark_anything_adapter: bool = False
    enable_meta_seal_adapter: bool = False
    enable_video_seal_adapter: bool = False
    enable_audio_seal_adapter: bool = False
    enable_discovery_mock: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

for folder in [settings.upload_dir, settings.watermark_dir, settings.temp_dir]:
    Path(folder).mkdir(parents=True, exist_ok=True)
