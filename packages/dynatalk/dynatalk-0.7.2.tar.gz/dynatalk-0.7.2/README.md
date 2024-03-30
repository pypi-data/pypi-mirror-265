# dynatalk-py

This repository is the Python client of [Dynatalk](https://github.com/wwj718/Dynatalk).

> Dynatalk focuses on communication among objects, especially concerning interoperability among different languages/environments. -- [Dynatalk](https://github.com/wwj718/Dynatalk).

To use Dynatalk, you need to:

1. [Run an MQTT broker](https://github.com/wwj718/Dynatalk/blob/main/mqtt/readme.md)
2. Start programming with the dynatalk client.

## Install

```bash
pip install dynatalk
```

## get started

```py
from dynatalk import Supervisor, PyDemoAgent

supervisor = Supervisor()
# The agent object can work as a server (providing services to other agents) or work as a client (requesting services from other agents).
agent = PyDemoAgent("PyDemoAgent") # PyDemoAgent provides two services: add, echo
supervisor.addAgent(agent)

# As a **client**, agent requests PyDemoAgent to execute add, the parameters are [1, 2]
agent.request("PyDemoAgent", "add", [1 ,2])
# agent.request("LivelyDemoAgent", "add", [1, 2])

# Unlike request, sendTo does not require a response
# agent.sendTo...
```

to discover agents on the current network:

```py
agent.broadcastHelp()
time.sleep(1)
print(agent.availableActions)
```

## CLi tools

### dynatalk message monitor

```bash
dynatalk-monitor
```

## FAQ

### Set up MQTT

Use environment variables to set up MQTT.


default is:

```
MQTT_HOST: 127.0.0.1
MQTT_PORT: 1883
MQTT_USERNAME: guest
MQTT_PASSWORD: test
```

[How to set environment variables in Python?](https://stackoverflow.com/questions/5971312/how-to-set-environment-variables-in-python)