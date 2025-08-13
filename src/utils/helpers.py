import random
import asyncio
from loguru import logger


async def async_sleep(mode: int, config) -> None:
    match mode:
        case 1:
            srange = config.SLEEP_BETWEEN_ACCS
        case 2:
            srange = config.SLEEP_ON_ERRORS
        case _:
            srange = config.SLEEP_BETWEEN_ACCS

    t = random.randint(*srange)
    logger.info(f"Sleeping for {t} seconds...")
    await asyncio.sleep(t)
