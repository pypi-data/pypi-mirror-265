import random
import string
from typing import Optional

from .exceptions import MqttTransportParamsError


class MqttTransportParams:
    """MQTT transport parameters class."""

    __slots__ = '_host', '_port', '_client_id', '_user', '_password', '_request_topic', '_response_topic', '_qos', \
        '_keepalive'

    def __init__(self, host: str = 'localhost', port: int = 1883, client_id: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None, request_topic: Optional[str] = None,
                 response_topic: Optional[str] = None, qos: int = 1, keepalive: int = 60):
        """MQTT transport parameters constructor.

        Args:
            host (str): Broker hostname. (Defaults to 'localhost')
            port (int): Broker port. (Defaults to 1883)
            client_id (str, optional): Client ID. If no client ID is specified, a randomly generated one will be used.
            user (str, optional): Broker username.
            password (str, optional): Broker password.
            request_topic (str, optional): Topic to publish requests to.
            response_topic (str, optional): Topic to subscribe to for responses.
            qos (int): Quality of service. (Defaults to 1)
            keepalive (int): Keep alive interval. (Defaults to 60)
        """
        self._validate(port=port, qos=qos)
        self._host = host
        self._port = port
        self._client_id = client_id if client_id is not None else \
            ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
        self._user = user
        self._password = password
        self._request_topic = request_topic
        self._response_topic = response_topic
        self._qos = qos
        self._keepalive = keepalive

    def _validate(self, port: int, qos: int):
        """Validate transport parameters.

        Args:
            port (int): Port.
            qos (int): Quality of service.
        """
        self._validate_port(port)
        self._validate_qos(qos)

    @property
    def host(self) -> str:
        """:obj:`str`: Broker hostname.

        Getter and setter.
        """
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @staticmethod
    def _validate_port(port: int):
        """Validate broker port number.

        Args:
            port (int): Broker port number.
        Raises:
            MqttParamsError: If port is less than 1024 and greater than 65535.
        """
        if not (1024 <= port <= 65535):
            raise MqttTransportParamsError('Port value should be between 1024 and 65535.')

    @property
    def port(self) -> int:
        """:obj:`int`: Broker port.

        Getter and setter.
        """
        return self._port

    @port.setter
    def port(self, value: int):
        self._validate_port(value)
        self._port = value

    @property
    def client_id(self) -> str:
        """:obj:`str`: Client ID.

        Getter and setter.
        """
        return self._client_id

    @client_id.setter
    def client_id(self, value: str):
        self._client_id = value

    @property
    def user(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Broker username.

        Getter and setter.
        """
        return self._user

    @user.setter
    def user(self, value: Optional[str]):
        self._user = value

    @property
    def password(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Broker password.

        Getter and setter.
        """
        return self._password

    @password.setter
    def password(self, value: Optional[str]):
        self._password = value

    @property
    def request_topic(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Topic to publish requests to.

        Getter and setter.
        """
        return self._request_topic

    @request_topic.setter
    def request_topic(self, value: str):
        self._request_topic = value

    @property
    def response_topic(self) -> Optional[str]:
        """:obj:`str` or :obj:`None`: Topic to subscribe to for responses.

        Getter and setter.
        """
        return self._response_topic

    @response_topic.setter
    def response_topic(self, value: str):
        self._response_topic = value

    @staticmethod
    def _validate_qos(qos: int):
        """Validate quality of service parameter.

        Args:
            qos (int): Quality of service.
        Raises:
            MqttParamsError: If qos is less than 0 or greater than 2.
        """
        if not (0 <= qos <= 2):
            raise MqttTransportParamsError('QoS value should be between 0 and 2.')

    @property
    def qos(self) -> int:
        """:obj:`int`: Quality of service.

        Getter and setter.
        """
        return self._qos

    @qos.setter
    def qos(self, value: int):
        self._validate_qos(value)
        self._qos = value

    @property
    def keepalive(self) -> int:
        """:obj:`int`: Keep alive interval.

        Getter and setter.
        """
        return self._keepalive

    @keepalive.setter
    def keepalive(self, value: int):
        self._keepalive = value
