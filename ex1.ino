const int ledPin = 13; 
unsigned long previousMillis = 0; 
const long interval = 500; 

void setup() {
  Serial.begin(9600); 
  pinMode(ledPin, OUTPUT); 
}

void loop() {
  if (Serial.available() == 0) {
    
    for (int i = 32; i < 127; i++) { 
      Serial.print(i); 
      Serial.print(" - ");
      Serial.println((char)i); 
      
      
      digitalWrite(ledPin, HIGH); 
      delay(interval / 2); 
      digitalWrite(ledPin, LOW); 
      delay(interval / 2); 
    }
  }
}