int handshaken;

void setup() {
  Serial.begin(115200);
  handshaken = 0;
}
//afdwd
void debugPrint(const char *str) {
  Serial.println(str);
  Serial.flush();
}

void loop() {
  if (!handshaken) {
    handshakenUntilFinish();
  }
  else {
    sendSimpleData();
  }
}

int readSerialByte() {
  return Serial.read();
}


void handshakenUntilFinish() {
  int inByte;
  while (1) {
    if (Serial.available()){
      inByte = Serial.read();
      if (inByte == 48+2) { // receive 2HELO
        debugPrint("!");
        Serial.write(0); // answer 0ACK
        debugPrint("@");
        break;
      }
    } 
  }
  debugPrint("^");
  while (1) {
    inByte = Serial.read();
    if (inByte == 48+0) { //receive 0ACK
      debugPrint("#");
      handshaken = 1;
      break;
    }
  }
}

int sendSimpleData() {
  int inByte;
  while(1) {
    Serial.write(4);
    Serial.write(0);
    Serial.write("data");
    inByte = Serial.read();
    if (inByte == '0') { //receive 0ACK
      debugPrint("$");
      break;
    }
  }
}
