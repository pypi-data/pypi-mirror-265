import contextlib
from time import perf_counter
from typing import Callable

from ..common_index_lookup_utils.logger import promptflow_logger


@contextlib.contextmanager
def measure_execution_time(activity_name: str, callback: Callable = None):
    try:
        start_time = perf_counter()
        yield
    except Exception:
        promptflow_logger._telemetry_logger.exception(
            f"Exception occured in {activity_name}."
        )
        raise
    finally:
        end_time = perf_counter()
        log_message = f"`{activity_name}` completed in {end_time - start_time} seconds."
        if callback:
            callback(log_message)
        else:
            promptflow_logger.telemetry(msg=log_message, event_name=activity_name)
