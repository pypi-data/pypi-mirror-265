from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
  INFLUXDB_TOKEN: Optional[str] = None
  INFLUXDB_HOST: Optional[str] = None
  INFLUXDB_ORG: Optional[str] = None
  INFLUXDB_DB: Optional[str]  = None

settings = Settings()