import logging
import os
import toml
from typing import Any

logger = logging.getLogger(__name__)

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.toml")

def load_config(path: str = CONFIG_PATH) -> dict[str, Any]:
    logger.info('load config выполняется...')
    try:
        with open(path, "r") as f:
            config = toml.load(f)
    except Exception as Error:
        raise RuntimeError(f"Ошибка загрузки данных toml: {Error}")
    return config