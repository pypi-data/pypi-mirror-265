import json
from typing import Dict, Any

import aiohttp
from bot_station_client.model.config import BotStationClientConfig


class BotStationClient:
    config: BotStationClientConfig = ""

    def __init__(self, config: BotStationClientConfig):
        self.config = config

    async def create(self,
                     name: str,
                     description: str,
                     prompt_intro: str,
                     add_external_context_to_prompt: bool = False,
                     add_messages_history_to_prompt: bool = False,
                     temperature: float = 0.6
                     ) -> str:
        """
        :param name:
        :param description:
        :param prompt_intro:
        :param add_external_context_to_prompt:
        :param add_messages_history_to_prompt:
        :param temperature:
        :return: new bot's ID
        """
        response_json = await self.__post(
            method="create",
            content={
                "name": name,
                "description": description,
                "prompt_intro": prompt_intro,
                "add_external_context_to_prompt": str(add_external_context_to_prompt).lower(),
                "add_messages_history_to_prompt": str(add_messages_history_to_prompt).lower(),
                "temperature": temperature,
            }
        )
        return response_json["id"]

    async def train(self,
                    bot_id: str,
                    text: str
                    ):
        await self.__post(
            method="create",
            content={
                "id": bot_id,
                "data": text,
            }
        )

    async def call(self,
                   bot_id: str,
                   chat_id: int | str,
                   text: str
                   ) -> str:
        """
        :param bot_id:
        :param chat_id:
        :param text:
        :return: bot's response
        """
        response_json = await self.__post(
            method="call",
            content={
                "bot_id": bot_id,
                "chat_id": chat_id,
                "data": text
            }
        )
        return response_json["text"]

    async def __post(self,
                     method: str,
                     content: Dict[str, str | int],
                     ) -> Any:
        """
        Returns response json body
        """
        headers: Dict[str, str] = {'content-type': 'application/json'}
        session = aiohttp.ClientSession(headers=headers)
        url = f'{self.config.base_uri}/{method}'
        response = await session.post(url=url, data=json.dumps(content))
        data = await response.json()
        return data
