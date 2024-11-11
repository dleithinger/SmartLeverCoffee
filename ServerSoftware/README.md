## FrontEnd_flask Setup

# Before running flask server:
1. Define the following variables:
```
ENDPOINT = ""
CLIENT_ID = ""
PATH_TO_CERTIFICATE = ""
PATH_TO_PRIVATE_KEY = ""
PATH_TO_AMAZON_ROOT_CA_1 = ""
PUB_TOPIC = "esp32/sub"
SUB_TOPIC = "esp32/pub"
```
(The default MQTT topics are esp32/sub for publishing and esp32/pub for subscribing.)

2. Start the server by running: ```flask run```
