import requests
import base64
import aiohttp
import asyncio


class ApiCredentials:
    def __init__(self, username: str, password: str) -> None:
        """
        Initializes an instance of ApiCredentials.

        Args:
            username (str): The username for API authentication.
            password (str): The password for API authentication.
        """
        self.username = username
        self.password = password

    def get_encoded_credentials(self) -> str:
        """
        Returns the Base64 encoded username and password for API authentication.
        """
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()


class Client:
    def __init__(self, base_url: str, api_credentials: ApiCredentials) -> None:
        """
        Initializes a new instance of the Internal class.

        Args:
            base_url (str): The base URL of the API.
            api_credentials (ApiCredentials): The API credentials.

        Returns:
            None
        """
        self.base_url = base_url
        self.api_credentials = api_credentials
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_credentials.get_encoded_credentials()}",
        }

    def req(self, payload: dict, method: str, config: dict) -> dict:
        """
        Sends a HTTP request to the specified URL with the given payload and method.

        Args:
            payload (dict): The payload to be sent with the request.
            method (str): The HTTP method to be used for the request (e.g., "POST", "GET").
            config (dict): Additional configuration options for the request.

        Returns:
            dict: The JSON response from the server, if the request is successful.
                  None, if an error occurs during the request.

        Raises:
            requests.exceptions.Timeout: If the request times out.
            requests.exceptions.HTTPError: If an HTTP error occurs.
            requests.exceptions.RequestException: If a general request error occurs.
        """
        try:
            if method == "POST":
                response = requests.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload,
                    timeout=config["timeout"],
                )
            elif method == "GET":
                response = requests.get(
                    self.base_url, headers=self.headers, timeout=config["timeout"]
                )
            else:
                print(f"Unsupported method: {method}")
                return None

            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error occurred: {response.status_code}")
                return None

        except requests.exceptions.Timeout:
            print(
                f"Timeout error. The request to {self.base_url} with method {method} has timed out."
            )
            return None
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            print(response.text)
            return None
        except requests.exceptions.RequestException as err:
            print(f"Error occurred: {err}")
            return None


class ClientAsync:

    def __init__(self, base_url: str, api_credentials: ApiCredentials) -> None:
        """
        Initializes a new instance of the Internal class.

        Args:
            base_url (str): The base URL of the API.
            api_credentials (ApiCredentials): The API credentials used for authorization.

        Returns:
            None
        """
        self.base_url = base_url
        self.api_credentials = api_credentials
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.api_credentials.get_encoded_credentials()}",
        }

    async def get_job_id(
        self, payload: dict, user_session: aiohttp.ClientSession
    ) -> str:
        """
        Sends a POST request to the specified base URL with the given payload and headers.
        Returns the job ID from the response data.

        Args:
            payload (dict): The payload to be sent in the request body.
            user_session (aiohttp.ClientSession): The client session to use for the request.

        Returns:
            str: The job ID extracted from the response data.

        Raises:
            aiohttp.ClientResponseError: If an HTTP error occurs.
            aiohttp.ClientConnectionError: If a connection error occurs.
            asyncio.TimeoutError: If the request times out.
            Exception: If any other error occurs.
        """
        try:
            async with user_session.post(
                self.base_url, headers=self.headers, json=payload
            ) as response:
                data = await response.json()
                response.raise_for_status()
                return data["id"]
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message} - {data['message']}")
        except aiohttp.ClientConnectionError as e:
            print(f"Connection error occurred: {e}")
        except asyncio.TimeoutError:
            print(f"Timeout error. The request to {self.base_url} has timed out.")
        except Exception as e:
            print(f"An error occurred: {e} - {data['message']}")
        return None

    async def poll_job_status(
        self, job_id: str, poll_interval: int, user_session: aiohttp.ClientSession
    ) -> bool:
        """
        Polls the status of a job with the given job_id.

        Args:
            job_id (str): The ID of the job to poll.
            poll_interval (int): The interval (in seconds) between each poll request.
            user_session (aiohttp.ClientSession): The client session to use for making HTTP requests.

        Returns:
            bool: True if the job status is 'done', False otherwise.

        Raises:
            Exception: If the job status is 'faulted'.
        """
        job_status_url = f"{self.base_url}/{job_id}"
        while True:
            try:
                async with user_session.get(
                    job_status_url, headers=self.headers
                ) as response:
                    data = await response.json()
                    response.raise_for_status()
                    if data["status"] == "done":
                        return True
                    elif data["status"] == "faulted":
                        raise Exception("Job faulted")
            except aiohttp.ClientResponseError as e:
                print(
                    f"HTTP error occurred: {e.status} - {e.message} - {data['message']}"
                )
                return None
            except aiohttp.ClientConnectionError as e:
                print(f"Connection error occurred: {e}")
                return None
            except asyncio.TimeoutError:
                print(f"Timeout error. The request to {job_status_url} has timed out.")
                return None
            except Exception as e:
                print(f"Unexpected error processing your query: {e}")
                return None
            await asyncio.sleep(poll_interval)

    async def get_http_resp(
        self, job_id: str, user_session: aiohttp.ClientSession
    ) -> dict:
        """
        Retrieves the HTTP response for a given job ID.

        Args:
            job_id (str): The ID of the job.
            user_session (aiohttp.ClientSession): The client session used for making the request.

        Returns:
            dict: The JSON response data.

        Raises:
            aiohttp.ClientResponseError: If a client response error occurs.
            aiohttp.ClientConnectionError: If a client connection error occurs.
            asyncio.TimeoutError: If the request times out.
            Exception: If any other error occurs.
        """
        result_url = f"{self.base_url}/{job_id}/results"
        try:
            async with user_session.get(result_url, headers=self.headers) as response:
                data = await response.json()
                response.raise_for_status()
                return data
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message} - {data['message']}")
        except aiohttp.ClientConnectionError as e:
            print(f"Connection error occurred: {e}")
        except asyncio.TimeoutError:
            print(f"Timeout error. The request to {result_url} has timed out.")
        except Exception as e:
            print(f"An error occurred: {e} - {data['message']}")
        return None

    async def execute_with_timeout(
        self, payload: dict, config: dict, user_session: aiohttp.ClientSession
    ) -> dict:
        """
        Executes a request with a timeout.

        Args:
            payload (dict): The payload for the request.
            config (dict): The configuration settings.
            user_session (aiohttp.ClientSession): The user session.

        Returns:
            dict: The result of the request execution.
        """

        job_id = await self.get_job_id(payload, user_session)

        await self.poll_job_status(job_id, config["poll_interval"], user_session)

        result = await self.get_http_resp(job_id, user_session)
        return result
