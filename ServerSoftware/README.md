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


## LeverCoffee_LLM Setup

# Before running flask server:
1. Create a .env file and define the variable:
```
OPENAI_KEY = <YOUR_KEY>
```

2. Run ```npm install``` to install required library

3. Run ```node openai_llm.js```