#include <XBee.h>
#include <SoftwareSerial.h>

XBee xbee = XBee();

uint8_t entryText[] = {'K','A','0','5','M','J','1','7','2','1',' ', 'E','N'};
uint8_t exitText[] = {'K','A','0','5','M','J','1','7','2','1',' ', 'E','X'};

XBeeAddress64 addr64 = XBeeAddress64(0x0013a200, 0x41f19cc4);

ZBTxRequest zbTx1 = ZBTxRequest(addr64, entryText, sizeof(entryText));
ZBTxStatusResponse txStatus1 = ZBTxStatusResponse();

ZBTxRequest zbTx2 = ZBTxRequest(addr64, exitText, sizeof(exitText));
ZBTxStatusResponse txStatus2 = ZBTxStatusResponse();

SoftwareSerial sserial(12, 13);

byte inputPin = A0;
float sourceVoltage = 5;
const byte BIT_RESOLUTION = 10;

void readPushButtons() {
  float measuredValue = analogRead(inputPin);
  float measuredVoltage = measuredValue * ((float)sourceVoltage / (pow(2, BIT_RESOLUTION) - 1));
  if (measuredVoltage > 1.5 && measuredVoltage < 3.0) {
    transmitExitRequest();
  } else if (measuredVoltage > 3.0) {
    transmitEntryRequest();
  }
}

void transmitEntryRequest() {
  do {
    xbee.send(zbTx1);
    Serial.println("Transmitting Entry Request");

    if (xbee.readPacket(500)) {
      Serial.println("Received Response");

      if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
        xbee.getResponse().getZBTxStatusResponse(txStatus1);
        if (txStatus1.getDeliveryStatus() == SUCCESS) {
          Serial.println("SUCCESS");
        }
      } else if (xbee.getResponse().isError()) {
        Serial.print("Error reading packet.  Error code: ");  
        Serial.println(xbee.getResponse().getErrorCode());
      } else {
        Serial.println("This should not happen");
      }
      delay(1000);
    }
    //Serial.print("Delivery status: ");
    //Serial.println(txStatus1.getDeliveryStatus());
  } while(txStatus1.getDeliveryStatus() != 0);
}

void transmitExitRequest() {
  do {
    xbee.send(zbTx2);
    Serial.println("Transmitting Exit request");

    if (xbee.readPacket(500)) {
      Serial.println("Received Response");

      if (xbee.getResponse().getApiId() == ZB_TX_STATUS_RESPONSE) {
        xbee.getResponse().getZBTxStatusResponse(txStatus2);
        if (txStatus1.getDeliveryStatus() == SUCCESS) {
          Serial.println("SUCCESS");
        }
        Serial.print("Delivery status: ");
        Serial.println(txStatus2.getDeliveryStatus());
      } else if (xbee.getResponse().isError()) {
        Serial.print("Error reading packet.  Error code: ");  
        Serial.println(xbee.getResponse().getErrorCode());
      } else {
        Serial.println("This should not happen");
      }
      delay(1000);
    }
    //Serial.print("Delivery status: ");
    //Serial.println(txStatus2.getDeliveryStatus());
  } while(txStatus2.getDeliveryStatus() != 0);
}

void setup() {
  Serial.begin(9600);
  sserial.begin(9600);
  xbee.setSerial(sserial);
}


void loop() {
  readPushButtons();
}