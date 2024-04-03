int potPin = 13;
int ledPins[] = {2, 3, 4, 5, 6, 7}; 
int potValue;

void setup() {
  for (int i = 0; i < 6; i++) {
    pinMode(ledPins[i], OUTPUT); 
  }
}

void loop() {
  potValue = analogRead(potPin); // Lê o valor do potenciômetro
  int delayTime = map(potValue, 0, 1023, 50, 1000); // Mapeia o valor do potenciômetro para o intervalo de tempo desejado

  for (int i = 0; i < 6; i++) {
    digitalWrite(ledPins[i], HIGH); // Acende o LED atual
    delay(delayTime); // Aguarda
    digitalWrite(ledPins[i], LOW); // Apaga o LED atual
  }
}
