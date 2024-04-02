from dotenv import load_dotenv
load_dotenv()

from mediqbox.jobctxmgr import *

def dummy_service(raise_exception: bool = False) -> None:
  if raise_exception:
    raise Exception("Dummy service error")
  return

def test_dummy() -> None:
  service_context = ServiceContext(
    name="dummy_service",
    from_="jiamin@gmail.com",
    message_id="dummy_service_1",
    desc="This is a dummy service"
  )
  with JobContextManager(service_context):
    dummy_service()
    print(f"Done with {service_context.message_id}")

  service_context.message_id = "dummy_service_2"
  try:
    with JobContextManager(service_context):
      dummy_service(True)
      print(f"Done with {service_context.message_id}")
  except Exception:
    print(f"Error with {service_context.message_id}")

  return

if __name__ == "__main__":
  test_dummy()