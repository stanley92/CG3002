int handshaken;

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
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
  return Serial1.read();
}


void handshakenUntilFinish() {
  int inByte;
  while (1) {
    if (Serial1.available()){
      inByte = Serial1.read();
      if (inByte == 2) { // receive 2HELO
        debugPrint("!");
        Serial1.write(0); // answer 0ACK
        debugPrint("@");
        break;
      }
    } 
  }
  debugPrint("^");
  while (1) {
    inByte = Serial1.read();
    if (inByte == 0) { //receive 0ACK
      debugPrint("#");
      handshaken = 1;
      break;
    }
  }
}

int sendSimpleData() {
  int inByte;
  while(1) {
    Serial1.write(4);
    Serial1.write(0);
    Serial1.write("data");
    inByte = Serial1.read();
    if (inByte == '0') { //receive 0ACK
      debugPrint("$");
      break;
    }
  }
}
