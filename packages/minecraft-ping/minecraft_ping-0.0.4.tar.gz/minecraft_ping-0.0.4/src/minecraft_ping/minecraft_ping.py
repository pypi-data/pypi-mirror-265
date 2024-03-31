import asyncio
import logging
import pathlib
from typing import Callable, Coroutine

from mcstatus import JavaServer


class MinecraftPing:
    """
    This class, `MinecraftPing`, is designed to check the connectivity status of one or more Minecraft servers,
    determining whether they are online or offline. It includes an asynchronous method to perform this check on
    multiple servers concurrently. However, you must await all methods.
    """

    def __init__(
            self,
            timeout: float,
            callback: Callable[[str, int, bool], Coroutine[None, None, None]] = None,
            callback_filepath_out: str = 'online.txt',
    ):
        """
        Initializes the MinecraftPing instance.
        :param timeout: Time in seconds to wait for each server response before closing the connection.
        :param callback: Function that will be called for each server response.
        :param callback_filepath_out: If no callback function is provided, the default is to write online to this file.
        """

        self.timeout: float = timeout
        self.callback: Callable[[str, int, bool], Coroutine[None, None, None]] =\
            callback if callback is not None else self._default_callback

        self.callback_filepath_out: str = callback_filepath_out

        if callback is None:
            pathlib.Path(self.callback_filepath_out).touch(exist_ok=True)

    async def get_state_bulk(self, servers: set[tuple[str, int]]) -> None:
        """
        Ping servers asynchronously and callback each server state to `self.callback_ip`
        :param servers: set of tuples (address, port) of the servers to ping
        :return: None
        """
        tasks = [asyncio.create_task(self._state_to_callback(ip, port)) for ip, port in servers]
        await asyncio.wait(tasks)

    async def get_state(self, addr: str, port: int) -> bool:
        """
        Get state of the server: online is True and offline is False.
        :param addr: Address of the server to ping.
        :param port: Port of the server to ping.
        :return: State of the server.
        """
        try:
            await (await JavaServer.async_lookup(f'{addr}:{port}', self.timeout)).async_status()
            return True
        except OSError as e:
            logging.debug(f"Socket exception for {addr}:{port} - {e}")
        except Exception as e:
            logging.debug(f"General exception for {addr}:{port} - {e}")
        return False

    async def _state_to_callback(self, addr: str, port: int) -> None:
        state: bool = await self.get_state(addr, port)
        if asyncio.iscoroutinefunction(self.callback):
            await self.callback(addr, port, state)
        else:
            logging.warning(f'Consider making the callback function {self.callback.__name__} asynchronous.')
            self.callback(addr, port, state)

    async def _default_callback(self, addr: str, port: int, state: bool) -> None:
        """
        Default callback function for pinging servers. Appends addr:port to `self.callback_filepath_out`.
        :param addr: Address of the Minecraft server
        :param port: Port of the Minecraft server
        :param state: Boolean to indicate if the server is Online or Offline
        :return: None
        """
        if not state:
            return
        try:
            with open(self.callback_filepath_out, 'a', encoding='utf-8') as f:
                f.write(f'{addr}:{port}\n')
        except FileNotFoundError:
            logging.error(f"File not found: {self.callback_filepath_out}")
        except PermissionError:
            logging.error(f"Permission denied: Unable to write to {self.callback_filepath_out}")
        except IOError as e:
            logging.error(f"IOError occurred: {e}")
