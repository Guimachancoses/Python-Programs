const int ledPin = 13; 
const int numIncomodam = 4; 
unsigned long previousMillis = 0; 
const long interval = 500; 
int numLoops = 1;

void setup() {
  Serial.begin(9600); 
  pinMode(ledPin, OUTPUT); 
}

void loop() {
  
  for (int i = 1; i <= numLoops; i++) {
    Serial.print(i);
    Serial.print(" elefante");
    if (i > 1) {
      Serial.print("s");
    }
    Serial.print(" incomodam");
    for (int j = 0; j < i; j++) {
      Serial.print(" incomodam");
    }
    Serial.println(" muito mais!");
    
   
    for (int k = 0; k < i * numIncomodam; k++) {
      digitalWrite(ledPin, HIGH); 
      delay(interval / 2); 
      digitalWrite(ledPin, LOW); 
      delay(interval / 2); 
    }
  }
  
  
  numLoops++;
  delay(1000); 
}
