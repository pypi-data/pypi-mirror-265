import logging
import asyncio
import os
import tempfile
from passlib.apps import custom_app_context

from amqtt.broker import Broker

# logger = logging.getLogger(__name__)


def generate_passwordfile():
    username = os.environ.get("MQTT_USERNAME", "guest")
    password = os.environ.get("MQTT_PASSWORD", "test")
    password_hash = custom_app_context.hash(password)

    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # Write content to the temporary file
    with open(temp_file.name, "w") as file:
        file.write(f"{username}:{password_hash}")

    # Get the path of the temporary file
    temp_file_path = temp_file.name

    temp_file.close()

    return temp_file_path


config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": "0.0.0.0:1883",
        },
        "ws-mqtt": {
            "bind": "0.0.0.0:15675",
            "type": "ws",
            # "max_connections": 10,
        },
    },
    # "sys_interval": 10,
    "auth": {
        "allow-anonymous": False,
        "password-file": generate_passwordfile(),
        "plugins": ["auth_file", "auth_anonymous"],
    },
    "topic-check": {"enabled": False},
}

broker = Broker(config)

def main():
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    formatter = "%(asctime)s :: %(levelname)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    # loop = asyncio.new_event_loop() # to support thread
    # asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(broker.start())
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()