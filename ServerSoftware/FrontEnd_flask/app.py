# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.# SPDX-License-Identifier: MIT-0

from flask import Flask, render_template, request

app = Flask(__name__)

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json

# change this before running the code ==================
# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2jx2mgo671gkv-ats.iot.us-east-2.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "../AWS_key/JULIA_KEY/certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "../AWS_key/JULIA_KEY/private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../AWS_key/JULIA_KEY/root.pem"
MESSAGE = "Hello World"
PUB_TOPIC = "esp32/sub"
SUB_TOPIC = "esp32/pub"
RANGE = 20
# ======================================================


event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
connect_future = mqtt_connection.connect()
connect_future.result()
print("Connected!")
print('Begin Publish')


@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template('index.html')

COFFEE_PRESSURE = [0, 0, 3, 4, 6, 9, 3]
COFFEE_ANGLE = [180, 180, 135, 120, 90, 45, 135]
@app.route("/keeppub", methods=['GET', 'POST'])
def keeppub():
    del COFFEE_ANGLE[0]
    del COFFEE_PRESSURE[0]
    if 0 < len(COFFEE_ANGLE):
        a = COFFEE_ANGLE[0]
        b = COFFEE_PRESSURE[0]
        mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps({"message": str(a)}), qos=mqtt.QoS.AT_LEAST_ONCE)
        return """
<meta http-equiv="refresh" content="2" />The current pressure is {}.""".format(b)
    return render_template('index.html')

@app.route("/pub", methods=['GET', 'POST'])
def pub():
    if request.method == 'POST':
        value = request.form['publish']
        message = {"message": value}
        mqtt_connection.publish(topic=PUB_TOPIC, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
        return render_template('index.html', value=value)
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)


