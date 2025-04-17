#include <Servo.h>

Servo myServo;
int servoPin = 4;   // Servo control pin
int potPin = A0;    // Potentiometer signal pin
float feedback = 0;

void setup() {
  myServo.attach(servoPin);  // Attach servo
  Serial.begin(9600);        // Start serial monitor
  delay(2000);
}

void loop() {

  for (int angle = 0; angle <= 180; angle += 1) {
    myServo.write(angle);  // Move servo to the current angle
    delay(500);            // Wait for the servo to move

    int potValue = analogRead(potPin);  // Read the potentiometer value
    feedback = 0.3678*potValue - 22.8739;
    Serial.print("Set Angle: ");
    Serial.print(angle);
    Serial.print(" | Analog Read: ");
    Serial.print(potValue);
    Serial.print("| Angle Measured: ");
    Serial.print(feedback);
    // Serial.print(",");
    Serial.println("");

    delay(100);  // Small delay before the next step
  }
  Serial.println("");
  

  delay(2000);  // Pause before restarting the loop
}
