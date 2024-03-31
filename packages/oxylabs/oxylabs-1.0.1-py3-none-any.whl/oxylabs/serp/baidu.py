from .baidu_base import BaiduBase
from .serp import InitSerp, InitSerpAsync
from oxylabs.utils.utils import prepare_config
from typing import Optional, Dict, Any


class Baidu(BaiduBase):
    def __init__(self, client: InitSerp):
        """
        Initializes a Baidu object.

        Args:
            client (Serp): An instance of the Serp class.

        Raises:
            TypeError: If the client parameter is not an instance of the Serp class.
        """
        if not isinstance(client, InitSerp):
            raise TypeError("Baidu requires a Serp instance")
        self.client = client

    def scrape_baidu_search(
        self,
        query: str,
        opts: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Scrapes Baidu search results for a given query.

        Args:
            query (str): The search query.
            opts (BaiduSearchOpts, optional): Configuration options for the search. Defaults to:
                {
                    "domain": com,
                    "start_page": 1,
                    "pages": 1,
                    "limit": 10,
                    "user_agent_type": desktop,
                    "callback_url": None,
                    "parsing_instructions": None,
                }
                This parameter allows customization of the search request.
            timeout (int | 50, optional): The interval in seconds for the request to time out if no response is returned. Defaults to 50.

        Returns:
            dict: The response from the server after the job is completed.
        """

        config = prepare_config(timeout=timeout)
        payload = self._prepare_baidu_search_payload(query, opts)
        response = self.client.get_resp(payload, config)
        return response

    def scrape_baidu_url(
        self,
        url: str,
        opts: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Scrapes Baidu search results for a given URL.

        Args:
            url (str): The URL to be scraped.
            opts (BaiduUrlOpts, optional): Configuration options for the search. Defaults to:
                {
                    "user_agent_type": desktop,
                    "callback_url": None,
                    "parsing_instructions": None,
                }
                This parameter allows customization of the search request.
            timeout (int | 50, optional): The interval in seconds for the request to time out if no response is returned. Defaults to 50.

        Returns:
            dict: The response from the server after the job is completed.
        """

        config = prepare_config(timeout=timeout)
        payload = self._prepare_baidu_url_payload(url, opts)
        response = self.client.get_resp(payload, config)
        return response


class BaiduAsync(BaiduBase):
    def __init__(self, client):
        """
        Initializes a BaiduAsync object.

        Args:
            client (SerpAsync): An instance of SerpAsync.

        Raises:
            TypeError: If the client is not an instance of SerpAsync.
        """
        if not isinstance(client, InitSerpAsync):
            raise TypeError("BaiduAsync requires a SerpAsync instance")
        self.client = client

    async def scrape_baidu_search(
        self,
        query: str,
        opts: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        poll_interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously scrapes Baidu search results for a given query.

        Args:
            query (str): The search query.
            opts (BaiduSearchOpts, optional): Configuration options for the search. Defaults to:
                {
                    "domain": com,
                    "start_page": 1,
                    "pages": 1,
                    "limit": 10,
                    "user_agent_type": desktop,
                    "callback_url": None,
                    "parsing_instructions": None,
                }
                This parameter allows customization of the search request.
            timeout (int | 50, optional): The interval in seconds for the request to time out if no response is returned. Defaults to 50.
            poll_interval (int | 2, optional): The interval in seconds for the request to poll the server for a response. Defaults to 2.

        Returns:
            dict: The response from the server after the job is completed.
        """

        config = prepare_config(timeout=timeout, poll_interval=poll_interval)
        payload = self._prepare_baidu_search_payload(query, opts)
        response = await self.client.get_resp(payload, config)
        return response

    async def scrape_baidu_url(
        self,
        url: str,
        opts: Optional[Dict[str, Any]] = None,
        timeout: Optional[int] = None,
        poll_interval: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Asynchronously scrapes Baidu search results for a given URL.

        Args:
            url (str): The URL to be scraped.
            opts (BaiduUrlOpts, optional): Configuration options for the search. Defaults to:
                {
                    "user_agent_type": desktop,
                    "callback_url": None,
                    "parsing_instructions": None,
                }
                This parameter allows customization of the search request.
            timeout (int | 50, optional): The interval in seconds for the request to time out if no response is returned. Defaults to 50.
            poll_interval (int | 2, optional): The interval in seconds for the request to poll the server for a response. Defaults to 2.

        Returns:
            dict: The response from the server after the job is completed.
        """

        config = prepare_config(timeout=timeout, poll_interval=poll_interval)
        payload = self._prepare_baidu_url_payload(url, opts)
        response = await self.client.get_resp(payload, config)
        return response
