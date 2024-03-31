"""Contains the class User which acts as a user interface with the entire SDK"""

import asyncio

from .apis.login_api import LoginApi
from .apis.service_api import ServiceApi
from .apis.data_api import DataApi
from .utils.access import Access


class User:
    """SDK interface"""

    def __init__(self):
        self._access: Access = Access()
        self._login_api: LoginApi = LoginApi(self._access)
        self.data: DataApi = DataApi(self._access)
        self.service: ServiceApi = ServiceApi(self._access)

    async def login(self, username: str, password: str) -> asyncio.Future[None]:
        """Log in

        Args:
            username (str)
            password (str)

        Returns:
            asyncio.Future[None]
        """
        return await self._login_api.login(username,password)
    