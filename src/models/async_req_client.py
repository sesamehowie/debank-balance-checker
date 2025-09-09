from aiohttp import ClientSession
from loguru import logger
from functools import reduce


class AsyncReqClient:
    def __init__(self, config):
        self.retries = config.RETRIES
        self.api_key = config.RAPID_API_KEY
        self._session = ClientSession()
        self.headers = {
            "x-rapidapi-host": "debank-unofficial-api.p.rapidapi.com",
            "x-rapidapi-key": self.api_key,
        }
        self._session.headers.update(self.headers)

    async def get_total_balance(self, account_address: str):
        url = "https://debank-unofficial-api.p.rapidapi.com/user/total_balance"
        params = {"id": account_address.strip()}
        data = None

        for i in range(self.retries):
            try:
                logger.info(
                    f"Trying to get total amount for address {account_address}..."
                )

                async with self._session.get(
                    url, params=params, headers=self.headers
                ) as response:
                    data = await response.json()
                    if data.get("chain_list"):
                        break
            except Exception as e:
                logger.warning(f"Attempt {i+1}/{self.retries}: Error: {str(e)}")
                continue

        if data and (data.get("total_usd_value") or data.get("chain_list")):
            if data.get("total_usd_value"):
                amount = str(data.get("total_usd_value"))
            else:
                amount = str(
                    reduce(
                        lambda acc, chain: acc + chain.get("usd_value", 0),
                        data["chain_list"],
                        0,
                    )
                )
        else:
            amount = "0"

        return [account_address, amount]
