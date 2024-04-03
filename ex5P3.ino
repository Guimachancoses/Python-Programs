int potPin = 13; // Pino analógico onde o potenciômetro está conectado
int buzzerPin = 8; // Pino do buzzer
int potValue; // Valor lido do potenciômetro

void setup() {
  pinMode(buzzerPin, OUTPUT); // Configura o pino do buzzer como saída
}

void loop() {
  potValue = analogRead(potPin); // Lê o valor do potenciômetro
  int frequency = map(potValue, 0, 1023, 50, 5000); // Mapeia o valor do potenciômetro para a frequência desejada

  tone(buzzerPin, frequency); // Gera um tom no buzzer com a frequência atual
}
