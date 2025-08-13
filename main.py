from src.utils.helpers import async_sleep
from src.utils.file_manager import FileManager
from src.models.async_req_client import AsyncReqClient
from src.models.config import Config
from loguru import logger
import asyncio
import traceback


async def process_account(config, wallet, accumulation_list: list):
    try:
        client = AsyncReqClient(config=config)
        result = await client.get_total_balance(account_address=wallet)
        if not isinstance(result, list):
            result = [wallet, "0.0000"]
        accumulation_list.append(result)
        await async_sleep(1, config)
    except Exception:
        logger.error(traceback.format_exc())
        await async_sleep(2, config)
    finally:
        await client._session.connector.close()
        await client._session.close()


async def main():
    batch_size = 5
    semaphore_limit = 5
    batch_delay = 5

    config = Config()
    file_manager = FileManager(filename=config.WALLETS_FILE)

    wallets = file_manager.open_file()
    wallets_amt = len(wallets)
    del file_manager
    results = []

    logger.debug(f"Loaded {wallets_amt} wallets")

    while wallets:
        current_batch = wallets[:batch_size]
        logger.debug(f"Processing batch of {len(current_batch)} wallets")

        async with asyncio.Semaphore(semaphore_limit):
            tasks = [
                asyncio.create_task(process_account(config, wallet, results))
                for wallet in current_batch
            ]
            await asyncio.gather(*tasks, return_exceptions=True)

        wallets = wallets[batch_size:]

        if wallets:
            logger.debug(f"Waiting {batch_delay} seconds before next batch")
            await asyncio.sleep(batch_delay)

    if results:
        logger.info("Writing results...")

        file_manager = FileManager(
            filename=config.RESULTS_FILE_PATH, csv_header=["account", "usd_value"]
        )

        file_manager.open_file("w", results)


if __name__ == "__main__":
    asyncio.run(main())
