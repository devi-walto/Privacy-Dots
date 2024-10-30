// Define pin numbers
const int ledPin = D6;          // Pin for the LED
const int motionSensorPin = D1; // Pin for the PIR motion sensor

void setup() {
  // Start Serial communication at 9600 baud
  Serial.begin(115200);
  Serial.println("Setup starting...");

  // Set the LED pin as OUTPUT
  pinMode(ledPin, OUTPUT);
  Serial.println("LED pin set as OUTPUT.");

  // Set the motion sensor pin as INPUT
  pinMode(motionSensorPin, INPUT);
  Serial.println("Motion sensor pin set as INPUT.");

  // Initial LED state
  digitalWrite(ledPin, LOW);
  Serial.println("LED is initially OFF. Waiting for motion...");
}

void loop() {
  // Blink the LED to confirm it's working
  Serial.println("Blinking LED...");
  digitalWrite(ledPin, LOW);  // Turn LED OFF
  delay(500);                 // Wait for 500 milliseconds

  // Read the motion sensor
  int motionState = digitalRead(motionSensorPin);
  
  if (motionState == LOW) {
    Serial.println("Motion detected! Turning LED ON.");
    digitalWrite(ledPin, HIGH); // Turn LED ON if motion is detected
    delay(5000);
  } else if (motionState == HIGH) {
    Serial.println("No motion detected. LED OFF.");
    digitalWrite(ledPin, LOW); // Ensure LED is OFF if no motion
    delay(5000);
  }
}
