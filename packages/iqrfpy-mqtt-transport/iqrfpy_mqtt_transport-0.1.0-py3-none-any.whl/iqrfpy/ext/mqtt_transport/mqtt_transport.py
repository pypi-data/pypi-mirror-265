import json
import threading

from typing import Callable, List, Optional
from paho.mqtt.client import Client, error_string, CallbackAPIVersion
from iqrfpy.enums.message_types import MessageType
from iqrfpy.exceptions import TransportNotConnectedError, MessageNotReceivedError, DpaRequestTimeoutError, \
    JsonRequestTimeoutError, UnsupportedMessageTypeError, JsonResponseNotSupportedError
from iqrfpy.response_factory import ResponseFactory
from iqrfpy.itransport import ITransport
from iqrfpy.irequest import IRequest
from iqrfpy.iresponse import IResponse
from iqrfpy.confirmation import Confirmation
from iqrfpy.utils.dpa import IQMESH_TEMP_ADDR, BROADCAST_ADDR

from .exceptions import MqttTransportConnectError
from .objects import MqttTransportParams


class MqttTransport(ITransport):
    """MQTT transport class."""

    __slots__ = '_client', '_params', '_callback', '_global_request_timeout', '_cv', '_msg_ids', '_m_type', \
        '_response', '_dpa_timeout', '_received_timeout', '_unsupported'

    def __init__(self, params: MqttTransportParams, callback: Optional[Callable] = None, auto_init: bool = False,
                 global_request_timeout: Optional[float] = 5):
        """MQTT transport constructor.

        Args:
            params (MqttTransportParams): MQTT parameters.
            callback (Callable, optional): Callback to process responses.
            auto_init (bool): Initialize and establish connection automatically.
            global_request_timeout (float, optional): Request timeout, used if timeout is not explicitly
                passed to receive methods.
        """
        self._client: Optional[Client] = None
        self._params: MqttTransportParams = params
        self._callback: Optional[Callable] = callback
        self._global_request_timeout: float = global_request_timeout
        self._cv: threading.Condition = threading.Condition()
        self._con_cv: threading.Condition = threading.Condition()
        self._con_rc: Optional[int] = None
        self._sub_cv: threading.Condition = threading.Condition()
        self._msg_ids: List[str] = []
        self._m_type: Optional[MessageType] = None
        self._response: Optional[IResponse] = None
        self._dpa_timeout: Optional[float] = None
        self._received_timeout: bool = False
        self._unsupported: bool = False
        if auto_init:
            self.initialize()

    def initialize(self) -> None:
        """Initialize and establish MQTT connection.

        The method initializes MQTT client, sets callbacks, connects to broker and subscribes to response topic.
        """
        self._client = Client(client_id=self._params.client_id, callback_api_version=CallbackAPIVersion.VERSION1)
        self._client.on_connect = self._connect_callback
        self._client.on_message = self._message_callback
        self._client.on_subscribe = self._subscribe_callback
        if self._params.user is not None and self._params.password is not None:
            self._client.username_pw_set(self._params.user, self._params.password)
        try:
            self._client.connect(self._params.host, self._params.port)
        except Exception as e:
            raise MqttTransportConnectError(e)
        self._client.loop_start()
        with self._con_cv:
            self._con_cv.wait()
        if self._con_rc != 0:
            raise MqttTransportConnectError(error_string(self._con_rc))
        with self._sub_cv:
            self._sub_cv.wait()

    def terminate(self, force: bool = False) -> None:
        """Terminate MQTT connection.

        Args:
            force (bool): Force terminate connection. (Defaults to False)
        """
        self._client.disconnect()
        self._client.loop_stop(force=force)

    def _connect_callback(self, client, userdata, flags, rc):
        """On connect callback.

        Subscribes to response topic upon establishing connection.
        """
        # pylint: disable=W0613
        self._con_rc = rc
        with self._con_cv:
            self._con_cv.notify()
        if rc == 0:
            self._client.subscribe(self._params.response_topic, self._params.qos)

    def _subscribe_callback(self, client, userdata, mid, granted_qos):
        """On subscribe callback.

        Notifies topic subscription conditional variable.
        """
        # pylint: disable=W0613
        with self._sub_cv:
            self._sub_cv.notify()

    def _message_callback(self, client, userdata, message):
        """On message callback.

        Processes messages published to response topic.
        If a callback has been assigned, then the response is passed to the callback as well.
        """
        # pylint: disable=W0613
        payload = json.loads(message.payload.decode('utf-8'))
        try:
            response = ResponseFactory.get_response_from_json(payload)
        except MessageNotReceivedError as err:
            if err.msgid == self._msg_ids[0]:
                self._received_timeout = True
                with self._cv:
                    self._cv.notify()
            return
        except UnsupportedMessageTypeError as err:
            if err.msgid == self._msg_ids[0]:
                self._unsupported = True
                with self._cv:
                    self._cv.notify()
            return
        if len(self._msg_ids) > 0 and response.msgid == self._msg_ids[0] and response.mtype == self._m_type:
            self._msg_ids.pop(0)
            self._response = response
            with self._cv:
                self._cv.notify()
        if self._callback is not None:
            self._callback(response)

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            bool: True if client is connected to broker, False otherwise
        """
        return self._client.is_connected()

    def send(self, request: IRequest) -> None:
        """Publish message to request topic.

        Args:
            request (IRequest): Request to publish.
        Raises:
            TransportNotConnectedError: If client is not connected to the broker.
        """
        self._response = None
        self._m_type = None
        self._dpa_timeout = None
        self._received_timeout = False
        self._unsupported = False
        if not self._client.is_connected():
            raise TransportNotConnectedError(f'MQTT client {self._params.client_id} not connected to broker.')
        self._client.publish(
            topic=self._params.request_topic,
            payload=json.dumps(request.to_json()),
            qos=self._params.qos
        )
        if request.nadr == 255:
            return
        self._dpa_timeout = request.dpa_rsp_time
        self._msg_ids.append(request.msgid)
        self._m_type = request.mtype

    def confirmation(self) -> Confirmation:
        """Return confirmation message.

        Daemon JSON API does not send confirmation messages separately.

        Raises:
            NotImplementedError: Confirmation not implemented.
        """
        raise NotImplementedError('Method not implemented.')

    def receive(self, timeout: Optional[float] = None) -> Optional[IResponse]:
        """Receive message synchronously.

        Args:
            timeout (float, optional): Time to wait for request to be processed and response sent.
                If not specified, :obj:`global_request_timeout` is used.
        Raises:
            DpaRequestTimeoutError: If DPA request timed out.
            JsonRequestTimeoutError: If JSON API response was received, but DPA request timed out, or if the JSON API
                response was not received within specified timeout.
            JsonResponseNotSupportedError: If JSON API response with expected message ID was received,
                but the response message type is not supported.
        """
        if len(self._msg_ids) == 0:
            return None
        timeout_to_use = timeout if timeout is not None else self._global_request_timeout
        with self._cv:
            self._cv.wait(timeout=timeout_to_use)
        if self._response is None:
            msg_id = self._msg_ids.pop(0)
            if self._received_timeout and self._dpa_timeout is not None:
                self._received_timeout = False
                raise DpaRequestTimeoutError(f'DPA request timed out (timeout {self._dpa_timeout} seconds).')
            else:
                if self._received_timeout:
                    self._received_timeout = False
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} received, but DPA request timed out.'
                    )
                elif self._unsupported:
                    self._unsupported = False
                    raise JsonResponseNotSupportedError(
                        f'Response message to request with ID {msg_id} received, but is not supported.'
                    )
                else:
                    raise JsonRequestTimeoutError(
                        f'Response message to request with ID {msg_id} not received within the specified time of '
                        f'{timeout_to_use} seconds.')
        return self._response

    def send_and_receive(self, request: IRequest, timeout: Optional[float] = None) -> Optional[IResponse]:
        """Publish request to request topic and wait for response.

        If request nadr is :obj:`IQMESH_TEMP_ADDR` (254) or :obj:`BROADCAST_ADDR` (255),
        the method does not wait for a response message and returns :obj:`None`.

        Args:
            request (IRequest): Request to publish.
            timeout (float, optional): Time to wait for request to be processed and response sent.
                If not specified, :obj:`global_request_timeout` is used.
        """
        self.send(request)
        if request.nadr in [IQMESH_TEMP_ADDR, BROADCAST_ADDR]:
            return None
        return self.receive(timeout)

    def set_receive_callback(self, callback: Callable[[IResponse], None]) -> None:
        """Assign callback for messages published to the response topic.

        Args:
            callback (Callable[[IResponse], None]): Callback used to process messages published to response topic.
        """
        self._callback = callback
