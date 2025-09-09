from src.utils.helpers import async_sleep
from src.utils.file_manager import FileManager
from src.models.async_req_client import AsyncReqClient
from src.models.config import Config
from loguru import logger
import asyncio
import traceback


async def process_account(config, wallet, accumulation_list: list):
    try:
        spl_symbol = ""
        splitters = [",", ".", ":", "-", ";"]

        for splitter in splitters:
            if splitter in wallet:
                spl_symbol = splitter
                break

        session_id, address = wallet.split(spl_symbol)
        client = AsyncReqClient(config=config)
        result = await client.get_total_balance(account_address=address)
        if not isinstance(result, list):
            res = [session_id, address, "0.0000"]
        else:
            res = [session_id, address, result[len(result) - 1]]
        accumulation_list.append(res)
        await async_sleep(1, config)
    except Exception:
        logger.error(traceback.format_exc())
        await async_sleep(2, config)
    finally:
        await client._session.connector.close()
        await client._session.close()


async def main():
    config = Config()
    file_manager = FileManager(filename=config.WALLETS_FILE)

    wallets = file_manager.open_file()
    wallets_amt = len(wallets)
    del file_manager
    results = []

    logger.debug(f"Loaded {wallets_amt} wallets")

    for wallet in wallets:
        task = asyncio.create_task(process_account(config, wallet, results))
        await task

    if results:
        logger.info("Writing results...")

        file_manager = FileManager(
            filename=config.RESULTS_FILE_PATH,
            csv_header=["session_id", "account", "usd_value"],
        )

        file_manager.open_file("w", results)


if __name__ == "__main__":
    asyncio.run(main())
