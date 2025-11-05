// Define pinos do sensor ultrassônico
const int trigPin = 9;
const int echoPin = 10;

// Define pinos dos CI CD4511
const int dataPins[] = {2, 3, 4};
const int latchPins[] = {5, 6, 7};
const int clockPins[] = {8, 11, 12};

void setup() {
  // Configura os pinos do sensor ultrassônico
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Configura os pinos dos CI CD4511 como saída
  for (int i = 0; i < 3; i++) {
    pinMode(dataPins[i], OUTPUT);
    pinMode(latchPins[i], OUTPUT);
    pinMode(clockPins[i], OUTPUT);
  }

  Serial.begin(9600); // Inicializa a comunicação serial
}

void loop() {
  long duration;
  float distance;

  // Gera um pulso no pino trig do sensor ultrassônico
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Calcula a duração do pulso no pino echo
  duration = pulseIn(echoPin, HIGH);

  // Calcula a distância em cm
  distance = (duration / 2) / 29.1;

  // Calcula as unidades e dezenas da distância
  int valor = distance * 10;  
  int dig4 = valor % 10;
  int dig3 = (valor % 100 - dig4) / 10;
  int dig2 = (valor % 1000 - dig4 - dig3 * 10) / 100;

  // Exibe os valores nos displays
  displayDigit(dig2, latchPins[0], dataPins[0], clockPins[0]);
  displayDigit(dig3, latchPins[1], dataPins[1], clockPins[1]);
  displayDigit(dig4, latchPins[2], dataPins[2], clockPins[2]);

  // Espera um pouco antes de realizar a próxima leitura
  delay(500);
}

void displayDigit(int digit, int latchPin, int dataPin, int clockPin) {
  digitalWrite(latchPin, LOW);
  shiftOut(dataPin, clockPin, LSBFIRST, digitToSegment(digit));
  digitalWrite(latchPin, HIGH);
}

byte digitToSegment(int digit) {
  switch (digit) {
    case 0: return 0b00111111;
    case 1: return 0b00000110;
    case 2: return 0b01011011;
    case 3: return 0b01001111;
    case 4: return 0b01100110;
    case 5: return 0b01101101;
    case 6: return 0b01111101;
    case 7: return 0b00000111;
    case 8: return 0b01111111;
    case 9: return 0b01101111;
    default: return 0b00000000;
  }
}
