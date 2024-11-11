## ESP32_wifi Setup

# Before uploading the code to your ESP32:

1. Make sure you are in a location with WiFi access.
2. If you are connecting to WiFi at school or any location that requires login, use the following code:
```
// Connecting to WiFi that requires login with email and password
WiFi.begin(WIFI_SSID, WPA2_AUTH_PEAP, WIFI_ID, WIFI_ID, WIFI_PASSWORD);
```
3. Create a secret.h file with your credentials:
```
#include <pgmspace.h>
 
#define SECRET
#define THINGNAME ""
 
const char WIFI_SSID[] = ""; 
const char WIFI_PASSWORD[] = "";
const char WIFI_ID[] = "";
const char AWS_IOT_ENDPOINT[] = "";
 
// Amazon Root CA 1
static const char AWS_CERT_CA[] PROGMEM = R"EOF(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
)EOF";
 
// Device Certificate
static const char AWS_CERT_CRT[] PROGMEM = R"KEY(
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
 
 
)KEY";
 
// Device Private Key
static const char AWS_CERT_PRIVATE[] PROGMEM = R"KEY(
-----BEGIN RSA PRIVATE KEY-----
-----END RSA PRIVATE KEY-----
 
)KEY";
```