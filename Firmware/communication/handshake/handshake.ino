int handshaken;

void setup() {
  Serial.begin(115200);
  Serial1.begin(115200);
  Serial.flush();
  Serial1.flush();
  handshaken = 0;
}
//afdwd
void debugPrint(int chr) {
  Serial.println(chr);
  Serial.flush();
}
void debugPrintStr(const char* str) {
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
      debugPrint(inByte);
      if (inByte == 2) { // receive 2HELO
        debugPrintStr("!");
        break;
      }
    } 
  }
  debugPrintStr("^");
  while (1) {
    inByte = Serial1.read();
    Serial1.write(3); // answer 3HELLOACK
    if (inByte == 0) { //receive 0ACK
      debugPrintStr("#");
      handshaken = 1;sudo
      break;
    }
  }
}

int sendSimpleData() {
  int inByte;
  debugPrintStr("write");
  while(1) {
    Serial1.write(4);
    Serial1.write(0);
    Serial1.write("data");
    Serial1.flush();
    inByte = Serial1.read();
    if (inByte == 0) { //receive 0ACK
      debugPrintStr("$");
      break;
    }
  }
}
