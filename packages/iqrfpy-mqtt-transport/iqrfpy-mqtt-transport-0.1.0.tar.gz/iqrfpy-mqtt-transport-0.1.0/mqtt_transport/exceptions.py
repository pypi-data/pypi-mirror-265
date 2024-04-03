class MqttTransportParamsError(ValueError):
    """MQTT parameters error.

    Raised if MQTT parameter does not validate.
    """


class MqttTransportConnectError(ConnectionError):
    """MQTT connect error.

    Raised if MQTT client cannot connect.
    """
