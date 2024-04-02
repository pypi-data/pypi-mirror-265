from mediqbox.jobctxmgr.context import *

class JobContextManager:
  def __init__(self, context: JobContextProtocol) -> None:
    self.context = context

  def __enter__(self) -> 'JobContextManager':
    self.context.setup()
    return self

  def __exit__(self, exc_type, exc_val, traceback) -> None:
    self.context.teardown(exc_type, exc_val, traceback)

class AsyncJobContextManager:
  def __init__(self, context: JobContextProtocol) -> None:
    self.context = context

  async def __aenter__(self) -> 'AsyncJobContextManager':
    self.context.setup()
    return self

  async def __aexit__(self, exc_type, exc_val, traceback) -> None:
    self.context.teardown(exc_type, exc_val, traceback)