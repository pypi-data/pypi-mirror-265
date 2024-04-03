## iqrf-mqtt-transport

An extension for [iqrfpy](https://gitlab.iqrf.org/open-source/iqrf-sdk/iqrfpy/iqrfpy/) for MQTT communication with IQRF Gateway daemon.

## Quick start

Before installing the library, it is recommended to first create a virtual environment.
Virtual environments help isolate python installations as well as pip packages independent of the operating system.

A virtual environment can be created and launched using the following commands:

```bash
python3 -m venv <dir>
source <dir>/bin/activate
```

iqrfpy can be installed using the pip utility:

```bash
python3 -m pip install -U iqrfpy-mqtt-transport
```

Example use:
```python
from iqrfpy.ext.mqtt_sync_transport import MqttTransport, MqttTransportParams
from iqrfpy.peripherals.coordinator.requests.bonded_devices import BondedDevicesRequest
from iqrfpy.peripherals.coordinator.responses.bonded_devices import BondedDevicesResponse

params = MqttTransportParams(
    host=..., # MQTT broker host
    port=..., # MQTT broker port
    client_id=..., # MQTT client ID
    request_topic=..., # Request topic that Daemon subscribes to
    response_topic=..., # Response topic that Daemon publishes responses to
    qos=1,
    keepalive=25
)
transport = MqttTransport(params=params, auto_init=True)

request = BondedDevicesRequest()
response: BondedDevicesResponse = transport.send_and_receive(request=request, timeout=10)

print(response.bonded)
```

## Documentation

For more information, check out our [API reference](https://apidocs.iqrf.org/iqrfpy/latest/iqrfpy.html).
