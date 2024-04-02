import logging
import os
import uuid

from ...core.logging.utils import LoggingUtils
from ..contracts.telemetry import StoreToolEventCustomDimensions
from ..utils.logging import ToolLoggingUtils


__LOG_LEVEL_ENV_KEY = "PF_LOGGING_LEVEL"
try:
    __LOG_LEVEL_MAPPINGS = logging.getLevelNamesMapping()
except AttributeError:
    # logging.getLevelNamesMapping was only introduced in 3.11; fallback for older versions
    __LOG_LEVEL_MAPPINGS = {
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
log_level = __LOG_LEVEL_MAPPINGS.get(os.getenv(__LOG_LEVEL_ENV_KEY), logging.INFO)

# Initialize promptflow logger
logging_config = ToolLoggingUtils.generate_config(
    tool_name=os.path.basename(__file__), log_level=log_level
)
promptflow_logger = LoggingUtils.sdk_logger(__package__, logging_config)
promptflow_logger.update_telemetry_context(
    {StoreToolEventCustomDimensions.TOOL_INSTANCE_ID: str(uuid.uuid4())}
)

promptflow_logger.telemetry(f"Initialized {os.path.basename(__file__)} logger.")

# TODO: Initialize AzureML RAG logger
