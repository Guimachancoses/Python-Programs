int potPin = 13; // Pino analógico onde o potenciômetro está conectado
int ledPins[] = {2, 3, 4}; // Pinos dos LEDs
int potValue; // Valor lido do potenciômetro

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(ledPins[i], OUTPUT); 
  }
}

void loop() {
  potValue = analogRead(potPin); // Lê o valor do potenciômetro
  int delayTime = map(potValue, 0, 1023, 50, 1000); // Mapeia o valor do potenciômetro para o intervalo de tempo desejado

  for (int i = 0; i < 3; i++) {
    digitalWrite(ledPins[i], HIGH); // Acende o LED atual
    delay(delayTime); // Aguarda
    digitalWrite(ledPins[i], LOW); // Apaga o LED atual
  }
}
