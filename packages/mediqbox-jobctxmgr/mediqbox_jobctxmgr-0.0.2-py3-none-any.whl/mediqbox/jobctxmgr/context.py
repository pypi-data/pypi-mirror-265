import time
import logging

from pydantic import BaseModel, ConfigDict
from types import TracebackType
from typing_extensions import Callable, Literal, Optional, Protocol, runtime_checkable

from mediqbox.jobctxmgr.serialize import write_to_influxdb

BaseModelMeta = type(BaseModel)
ProtocolMeta = type(Protocol)

# Config default logger
logging.basicConfig(
  level=logging.INFO,
  format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s"
)
default_logger = logging.getLogger("mediqbox.job_context")

class CombinedMeta(BaseModelMeta, ProtocolMeta):...

@runtime_checkable
class JobContextProtocol(Protocol, metaclass=ProtocolMeta):
  @property
  def id(self) -> str:...

  def setup(self) -> None:...
  def teardown(
      self,
      exc_type: type[BaseException] | None,
      exc_val: BaseException | None,
      traceback: TracebackType | None,
  ) -> None:...

class BaseContext(BaseModel, JobContextProtocol, metaclass=CombinedMeta):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  name: str
  status: Literal["started", "done", "failed"] = "started"
  start_time: float = time.perf_counter()
  time_elapsed: float = 0.0
  desc: Optional[str] = None
  result: Optional[str] = None
  error: Optional[str] = None
  logger: logging.Logger = default_logger

  write_to_db: Optional[Callable] = None

  def setup(self) -> None:
    self.logger.info(f"{self.name.capitalize()} {self.id} is {self.status}.")
    self.start_time = time.perf_counter()

  def teardown(self, exc_type, exc_val, traceback) -> None:
    self.time_elapsed = time.perf_counter() - self.start_time

    self.status = "failed" if exc_type else "done"
    self.error = str(exc_val) if exc_type else None

    if exc_type:
      self.logger.exception(traceback)

    self.logger.info(f"{self.name.capitalize()} {self.id} is {self.status}. Elapsed time: {self.time_elapsed} seconds.")

    if self.write_to_db:
      self.write_to_db()

class ServiceContext(BaseContext):
  message_id: str
  from_: str
  work_units: float = 0.0

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    if not self.write_to_db:
      def _write_to_db() -> None:
        tags = [
          ("name", self.name),
          ("status", self.status),]
        fields = [
          ("message_id", self.id),
          ("from", self.from_),
          ("work_units", self.work_units),
          ("time_elapsed", self.time_elapsed),
          ("desc", self.desc or ""),
          ("result", self.result or ""),
          ("error", self.error or ""),]
        write_to_influxdb("services", tags, fields)
        return
      
      self.write_to_db = _write_to_db

    return

  @property
  def id(self) -> str:
    return self.message_id
  
  @property
  def from_(self) -> str:
    return self.from_

class PipelineContext(BaseContext):
  service_context: Optional[ServiceContext] = None

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    if not self.write_to_db:
      def _write_to_db() -> None:
        tags = [
          ("name", self.name),
          ("status", self.status),
          ("service_name", self.service_name),]
        fields = [
          ("message_id", self.id),
          ("from", self.from_),
          ("time_elapsed", self.time_elapsed),
          ("desc", self.desc or ""),
          ("result", self.result or ""),
          ("error", self.error or ""),]
        write_to_influxdb("pipelines", tags, fields)
        return
      
      self.write_to_db = _write_to_db

    return

  @property
  def service_name(self) -> str:
    return self.service_context.name if self.service_context else ""
  
  @property
  def id(self) -> str:
    return self.service_context.id if self.service_context else ""
  
  @property
  def from_(self) -> str:
    return self.service_context.from_ if self.service_context else ""

class TaskContext(BaseContext):
  service_context: Optional[ServiceContext] = None
  pipeline_context: Optional[PipelineContext] = None

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

    if not self.write_to_db:
      def _write_to_db() -> None:
        tags = [
          ("name", self.name),
          ("status", self.status),
          ("pipeline_name", self.pipeline_name),
          ("service_name", self.service_name),]
        fields = [
          ("message_id", self.id),
          ("from", self.from_),
          ("time_elapsed", self.time_elapsed),
          ("desc", self.desc or ""),
          ("result", self.result or ""),
          ("error", self.error or ""),]
        write_to_influxdb("tasks", tags, fields)
        return
      
      self.write_to_db = _write_to_db

    return
  
  @property
  def pipeline_name(self) -> str:
    return self.pipeline_context.name if self.pipeline_context else ""
  
  @property
  def service_name(self) -> str:
    return self.pipeline_context.service_name if self.pipeline_context else (
      self.service_context.name if self.service_context else "")
  
  @property
  def id(self) -> str:
    return self.pipeline_context.id if self.pipeline_context else (
      self.service_context.id if self.service_context else "")
  
  @property
  def from_(self) -> str:
    return self.pipeline_context.from_ if self.pipeline_context else (
      self.service_context.from_ if self.service_context else "")