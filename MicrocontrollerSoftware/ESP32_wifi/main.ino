#include "secrets.h"
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "WiFi.h"

#define LEDPIN 2
#define BTNPIN 14
#define BTNTYPE INPUT
 
#define AWS_IOT_PUBLISH_TOPIC   "esp32/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "esp32/sub"
 
WiFiClientSecure net = WiFiClientSecure();
PubSubClient client(net);

int f;

void ledOn(int lightOn)
{
  digitalWrite(LEDPIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(lightOn);                      // wait for a second
  digitalWrite(LEDPIN, LOW);   // turn the LED off by making the voltage LOW
  delay(1000);
}
 
void connectAWS()
{

  // Start Wi-Fi scan
  Serial.println("Scanning for Wi-Fi networks...");
  int numberOfNetworks = WiFi.scanNetworks();
  
  if (numberOfNetworks == 0) {
    Serial.println("No networks found.");
  } else {
    Serial.println("Networks found:");
    for (int i = 0; i < numberOfNetworks; ++i) {
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(" dBm)");
      Serial.println();
      delay(10);
    }
  }
  
  Serial.println("Scan complete.");

  WiFi.mode(WIFI_STA);
  // WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  WiFi.begin(WIFI_SSID, WPA2_AUTH_PEAP, WIFI_ID, WIFI_ID, WIFI_PASSWORD);
  
  ledOn(500);
  ledOn(500);
  ledOn(500);
  Serial.println("Connecting to Wi-Fi");
  

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    ledOn(1000);
  }
 
  // Configure WiFiClientSecure to use the AWS IoT device credentials
  net.setCACert(AWS_CERT_CA);
  net.setCertificate(AWS_CERT_CRT);
  net.setPrivateKey(AWS_CERT_PRIVATE);
 
  // Connect to the MQTT broker on the AWS endpoint we defined earlier
  client.setServer(AWS_IOT_ENDPOINT, 8883);
 
  // Create a message handler
  client.setCallback(messageHandler);
 
  Serial.println("Connecting to AWS IOT");
 
  while (!client.connect(THINGNAME))
  {
    Serial.print(".");
    delay(100);
  }
 
  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }
 
  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);
 
  Serial.println("AWS IoT Connected!");
}
 
void publishMessage()
{
  StaticJsonDocument<200> doc;
  doc["Button"] = f;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client
 
  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}
 
void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);
 
  StaticJsonDocument<200> doc;
  deserializeJson(doc, payload);
  const char* message = doc["message"];
  Serial.println(message);
  digitalWrite(LEDPIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(1000);                      // wait for a second
  digitalWrite(LEDPIN, LOW);   // turn the LED off by making the voltage LOW
  delay(100);

}
 
void setup()
{
  pinMode(LEDPIN, OUTPUT);
  Serial.begin(115200);
  connectAWS();
  pinMode(BTNPIN, BTNTYPE);
}
 
void loop()
{
  // if (digitalRead(BTNPIN) == HIGH) {
  //   // turn LED on:
  //   // digitalWrite(ledPin, HIGH);
  //   f = 1;
  // } else {
  //   // turn LED off:
  //   // digitalWrite(ledPin, LOW);
  //   f = 0;
  // }
 
  // Serial.println(F("LOOP"));
 
  publishMessage();
  client.loop();
  delay(1000);
}
