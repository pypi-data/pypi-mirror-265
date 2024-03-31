"""Contains the data api"""
import asyncio
import logging

import requests

from ..utils.access import Access


class LoginApi:
    """The login api provides the login mechanism"""

    _url:str = "https://api.dev.be-intelli.com/cms/api/auth/local"

    def __init__(self, acc: Access):
        self._access = acc

    async def login(self, username:str, password:str) -> asyncio.Future[None]:
        """Sends an HTTP request for an access token

        Args:
            username (str)
            password (str)

        Returns:
            asyncio.Future[None]
        """
        future:asyncio.Future[None] = asyncio.Future()

        #the real login wrapped in an extra function to execute async
        async def task()->None:

            #login data
            data:dict[str,str] = {
                "identifier": username,
                "password": password
            }

            #send http request
            logging.debug(f"Execute requests.post(url={self._url}, json={data})")
            response = requests.post(url=self._url, json=data)
            logging.debug(f"Received response: {response}")

            #check response
            if response.status_code == 200:
                self._access.set_access_token(response.json().get("jwt"))
                future.set_result(None)
                logging.debug("Login successful")
            else:
                logging.debug("Login failed")
                future.set_exception(Exception("Login failed"))

        await asyncio.create_task(task())
        return future
