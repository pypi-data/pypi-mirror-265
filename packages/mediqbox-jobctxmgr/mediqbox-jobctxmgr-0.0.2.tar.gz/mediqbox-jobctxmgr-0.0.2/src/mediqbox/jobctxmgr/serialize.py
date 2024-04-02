from influxdb_client_3 import InfluxDBClient3, Point
from typing import Any

from mediqbox.jobctxmgr.settings import settings

def write_to_influxdb(
    measurement: str,
    tags: list[tuple[str, Any]],
    fields: list[tuple[str, Any]]
) -> None:
  if not (
    settings.INFLUXDB_TOKEN and
    settings.INFLUXDB_HOST and
    settings.INFLUXDB_ORG and
    settings.INFLUXDB_DB
  ):
    return
  
  point = Point(measurement)
  for tag in tags:
    point.tag(*tag)
  for field in fields:
    point.field(*field)
    
  with InfluxDBClient3(
    host=settings.INFLUXDB_HOST,
    token=settings.INFLUXDB_TOKEN,
    org=settings.INFLUXDB_ORG
  ) as client:
    client.write(database=settings.INFLUXDB_DB, record=point)