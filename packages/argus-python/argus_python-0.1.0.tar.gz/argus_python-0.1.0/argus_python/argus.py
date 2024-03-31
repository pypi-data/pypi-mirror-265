"""Main Argus module."""

import json
import socket
from typing import Dict, Optional

from event_bus import EventBus
from helpers import Helpers


class Argus:
    BUFFER_SIZE = 1024
    DEFAULT_PORT = 1337

    def __init__(
        self,
        username: Optional[str] = "",
        password: Optional[str] = "",
        host: Optional[str] = "127.0.0.1",
        port: Optional[int] = DEFAULT_PORT,
    ) -> None:
        """
        Initialize the class with a username and password if you have set authentication
        on your running Argus Engine.
        Also set the host and port if you have modified it on the Argus Engine, it will
        default to the localhost and default port.

        Args:
            username (Optional[str], optional): the username. Defaults to "".
            password (Optional[str], optional): the password. Defaults to "".
            host (Optional[str], optional): the set host. Defaults to "127.0.0.1".
            port (Optional[int], optional): the set port. Defaults to DEFAULT_PORT.
        """
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.event_bus = EventBus()

    def send_authentication_data(self) -> None:
        """
        Sends authentication data to the Argus engine to validate a connection.
        """
        connection_string = f"<ArgusAuth>{self.username}:{self.password}</ArgusAuth>"
        self.socket.send(connection_string.encode())

    def connect(self, timeout: float = None) -> None:
        """
        This method connects to the Argus engine and sends authentication data based on how the
        the class has been instantiated. It will connect to the engine and await data. You can set
        a timeout to specify how long you want to wait for data from the engine.

        Args:
            timeout (float, optional): the timeout value in seconds. Defaults to None.
        """
        try:
            self.socket.connect((self.host, self.port))

            if self.username:
                self.send_authentication_data()

            while True:
                if timeout:
                    self.socket.settimeout(timeout)

                data = self.socket.recv(self.BUFFER_SIZE)
                if data:
                    data_str = data.decode("utf-8")

                    if Helpers.is_json_string(data_str):
                        self._publish_argus_data(data_str)
                    else:
                        print(f"Received: {data_str}")
                else:
                    break

        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")

        except ConnectionError as err:
            print(f"Connection error: {err}")

        except EOFError as err:
            print(f"Connection closed by server: {err}")

        except Exception as err:
            print(f"Error receiving data: {err}")

        finally:
            self.close()

    def close(self) -> None:
        print("socket closed")
        self._close_socket()

    def subscribe(self, subscriber: str, method_name: str) -> None:
        self.event_bus.subscribe(subscriber=subscriber, method_name=method_name)

    def _publish_argus_data(self, data: Dict[str, str]) -> None:
        argus_event = json.loads(data)
        self.event_bus.publish(argus_event)

    def _close_socket(self):
        if self.socket:
            self.socket.close()
