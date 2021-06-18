/*
  Demo code to connect to our mqtt server with tls and fingerprint checking.
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>
#include <credentials.h>

#define SENSOR_PIN A0

#define BUFFER_SIZE 100

void callback(const MQTT::Publish& pub) {
  Serial.print(pub.topic());
  Serial.print(" => ");
  if (pub.has_stream()) {
    uint8_t buf[BUFFER_SIZE];
    int read;
    while (read = pub.payload_stream()->read(buf, BUFFER_SIZE)) {
      Serial.write(buf, read);
    }
    pub.payload_stream()->stop();
    Serial.println("");
  } else
    Serial.println(pub.payload_string());

}

WiFiClient wclient;
PubSubClient client(wclient, host, port);

void setup() {
  Serial.begin(115200);
  delay(100);
  Serial.println();
  Serial.println();
  client.set_callback(callback);
}

void loop() {

  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    Serial.println("...");
    WiFi.begin(ssid, pass);

    if (WiFi.waitForConnectResult() != WL_CONNECTED)
      return;
    Serial.println("WiFi connected");
  }
  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      Serial.println("Connecting to MQTT server");
      // .set_auth("test", "test");
      if (client.connect("FloodSensor01")) {
        Serial.println("Connected to MQTT server, checking cert");
        /*
        if (wclient.verify(fingerprint, host)) {
          Serial.println("certificate matches");
        } else {
          Serial.println("certificate doesn't match");
          delay(60000);
          return;
        }
        */
        int analog_sensor_value = analogRead(SENSOR_PIN);
        printf("Analog reading: %i \r\n", analog_sensor_value);
        client.publish("/test/floodsensor/01", String(analog_sensor_value));
        client.subscribe("/test/time/60sec");
      } else {
        Serial.println("Could not connect to MQTT server");
        delay(5000);
      }
    }

    if (client.connected())
      client.loop();
  }
}